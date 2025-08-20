import uuid
from django.utils import timezone
import requests
from django.conf import settings
from django.db import transaction
from django.db.utils import IntegrityError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from apps.users.serializers import (
    UserSerializer,
    SocialProfileRegistrationSerializer,
    DevLoginSerializer,
)
from config.settings.base import KAKAO_CLIENT_ID, KAKAO_REDIRECT_URI, REDIS_CLIENT

from django.contrib.auth import get_user_model, authenticate

User = get_user_model()


class RedisKeys:
    """
    KAKAO_ACCESS_TOKEN: 카카오에서 발급받은 엑세스 토큰 cache
    KAKAO_REFRESH_TOKEN: 카카오에서 발급받은 리프레시 토큰 cache
    """

    KAKAO_ACCESS_TOKEN = "kakao_access_token_{provider_id}"

    @staticmethod
    def get_kakao_access_token_key(provider_id):
        return RedisKeys.KAKAO_ACCESS_TOKEN.format(provider_id=provider_id)


class TokenRefreshView(APIView):
    """
    refresh 토큰을 받으면 기존의 refresh token은 blacklist 처리하고
    access와 refresh token을 발급해주는 API
    """

    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"Refresh token이 제공되지 않았습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            # 기존 리프레쉬 토큰 검증
            old_refresh = RefreshToken(refresh_token)
            user_id = old_refresh.payload.get("user_id")
            user = User.objects.get(id=user_id)

            # 기존 refresh token 블랙리스트 처리
            old_refresh.blacklist()

            # 새 refresh token 생성
            new_refresh = RefreshToken.for_user(user)
            new_access_token = str(new_refresh.access_token)

            # body 에 access token 만 포함한 응답 생성
            response = Response({"access": new_access_token}, status=status.HTTP_200_OK)

            # 새 refresh token 을 쿠키에 설정
            response.set_cookie(
                key="refresh_token",
                value=str(new_refresh),
                httponly=True,
                secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
                samesite="Lax",
            )
            return response

        except TokenError:
            return Response(
                {"detail": "토큰이 유효하지 않거나 만료되었습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )
        except User.DoesNotExist:
            return Response(
                {"detail": "유저를 찾을 수 없습니다."}, status=status.HTTP_403_FORBIDDEN
            )
        except Exception:
            # 추후 logger에 저장할 것
            return Response(
                {"detail": "예상치 못한 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class KakaoAuthView(APIView):
    """소셜 로그인 API
    1. 카카오 인가 코드를 받아 액세스 토큰 요청
    2. 액세스 토큰으로 사용자 정보 조회
    3. 기존 가입된 유저인지 확인 후 JWT 발급 or 추가 정보 요청
    """

    authentication_classes = ()
    permission_classes = (AllowAny,)

    @extend_schema(
        summary="소셜 로그인",
        description="소셜 로그인을 위한 API입니다",
        request={
            "application/json": {
                "properties": {"code": {"type": "string"}},
                "requrired": ["code"],
            }
        },
        tags=["User"],
    )
    def post(self, request):
        kakao_code = request.data.get("code")  # 프론트엔드에서 받은 인가 코드

        if not kakao_code:
            return Response(
                {"error": "인가 코드가 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 인가 코드로 카카오 액세스 토큰 요청
        kakao_token_url = "https://kauth.kakao.com/oauth/token"

        data = {
            "grant_type": "authorization_code",
            "client_id": KAKAO_CLIENT_ID,
            "redirect_uri": KAKAO_REDIRECT_URI,
            "code": kakao_code,
        }

        token_response = requests.post(kakao_token_url, data=data, timeout=5)
        if token_response.status_code != 200:
            return Response(
                {"error": "카카오 토큰 요청 실패"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            kakao_access_token = token_response.json().get("access_token")

        except Exception:
            return Response(
                {"error": "토큰 요청은 성공했으나 토큰을 받아오지 못했습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 액세스 토큰으로 카카오 사용자 정보 요청
        kakao_user_info_url = "https://kapi.kakao.com/v2/user/me"
        headers = {"Authorization": f"Bearer {kakao_access_token}"}
        user_info_response = requests.get(kakao_user_info_url, headers=headers)

        if user_info_response.status_code != 200:
            return Response(
                {"error": "카카오 사용자 정보 요청 실패"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        kakao_user_info = user_info_response.json()
        kakao_id = kakao_user_info.get("id")
        kakao_email = (
            kakao_account := kakao_user_info.get("kakao_account")
        ) and kakao_account.get("email")
        # X and Y / X가 Falsy하면 Y는 쳐다도 안봄, X가 Truthy면 Y도 평가

        if not kakao_id:
            return Response(
                {"error": "provider_id가 없습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if not kakao_email:
            return Response(
                {"error": "kakao email을 가져오지 못했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        with transaction.atomic():
            try:
                user = User.objects.get(provider="KAKAO", provider_id=kakao_id)
            except User.DoesNotExist:
                if User.objects.filter(email=kakao_email).exists():
                    return Response(
                        {
                            "error": "해당 이메일은 이미 다른 계정으로 가입되어 있습니다."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user = User.objects.create(
                    email=kakao_email,
                    provider="KAKAO",
                    provider_id=kakao_id,
                    profile_completed=False,
                    nickname=uuid.uuid4().hex[:7],
                )

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        # Redis에 카카오 토큰 저장
        REDIS_CLIENT.setex(
            RedisKeys.get_kakao_access_token_key(user.provider_id),
            5 * 60 * 60,
            kakao_access_token,
        )

        serializer = UserSerializer(user)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response(
            {
                "access": access_token,
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
            "refresh_token",
            value=str(refresh),
            httponly=True,
            secure=settings.REFRESH_TOKEN_COOKIE_SECURE,
            samesite="Lax",
        )

        return response


class SocialProfileRegistrationView(APIView):
    """
    소셜로그인 추가 정보 받는 API
    """

    @extend_schema(
        summary="소셜 로그인 후 추가 정보 입력",
        description="소셜 로그인 후 부족한 정보를 입력하여 계정을 활성화합니다.",
        request=SocialProfileRegistrationSerializer,
        tags=["User"],
    )
    def post(self, request):
        user = request.user

        if user.profile_completed:
            return Response({"error": "이미 가입이 완료된 유저입니다."})

        registration_serializer = SocialProfileRegistrationSerializer(
            user, data=request.data
        )

        if not registration_serializer.is_valid():
            return Response(
                registration_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                user = registration_serializer.save()

        except IntegrityError:
            return Response(
                {"error": "이미 사용 중인 정보 입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"error": "추가 정보 입력 중 알 수 없는 오류 발생"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        response_serializer = UserSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    로그아웃 API
    """

    @extend_schema(
        summary="로그아웃",
        description="refresh token을 blacklist에 등록 후 로그아웃하는 API입니다",
        tags=["User"],
    )
    def post(self, request):
        # refresh token 블랙리스트 등록
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "Refresh token 이 제공되지 않았습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            # 유효하지 않은 토큰 (이미 블랙리스트에 있거나, 만료되었거나 등) -> 어차피 로그아웃된 상태와 같으므로 그냥 성공 처리.
            pass
        except Exception:
            return Response(
                {"error": "로그아웃 처리 중 서버 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if getattr(request.user, "provider", None) == "KAKAO" and getattr(
            request.user, "provider_id", None
        ):
            self._logout_kakao(request.user.provider_id)

        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("refresh_token")

        try:
            REDIS_CLIENT.delete(
                RedisKeys.get_kakao_access_token_key(request.user.provider_id)
            )
        except Exception:
            pass

        return response

    @staticmethod
    def _logout_kakao(provider_id: str):
        """
        Redis에 저장된 토큰으로 카카오 로그아웃 요청
        액세스 토큰이 만료되었거나 없으면 그냥 넘어감
        :param provider_id:
        :return:
        """

        kakao_access_token = REDIS_CLIENT.get(
            RedisKeys.get_kakao_access_token_key(provider_id)
        )

        if not kakao_access_token:
            return

        # Redis에서 가져온 값은 bytes일 수 있으므로 디코딩
        if isinstance(kakao_access_token, bytes):
            kakao_access_token = kakao_access_token.decode("utf-8")

        kakao_logout_url = "https://kapi.kakao.com/v1/user/logout"
        headers = {"Authorization": f"Bearer {kakao_access_token}"}

        try:
            requests.post(url=kakao_logout_url, headers=headers, timeout=5)
            # 카카오 로그아웃 API는 성공 시 200, 토큰 만료 시 401을 반환함.
            # 어떤 경우든 우리 입장에선 "더 이상 이 토큰은 유효하지 않다"는 의미이므로,
            # 200이 아닌 경우를 굳이 실패로 간주하고 재시도할 필요가 없음.

        except requests.RequestException as e:
            # 네트워크 에러 등
            raise RuntimeError(f"Kakao logout network error: {e}")


class DevLoginView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    @extend_schema(
        request=DevLoginSerializer,
        responses={
            200: dict,
            401: dict,
        },
        summary="로그인",
        description="이메일과 비밀번호로 사용자를 인증하여 JWT 토큰을 발급합니다.",
    )
    def post(self, request) -> Response:
        email = request.data.get("email")
        if not email:
            return Response(
                {"detail": "이메일을 입력하세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        password = request.data.get("password")
        if not password:
            return Response(
                {"detail": "비밀번호를 입력하세요"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = authenticate(email=email, password=password)

        if not User.objects.filter(email=email).exists():
            return Response(
                {"detail": "존재하지 않는 이메일입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user is None:
            return Response(
                {"detail": "잘못된 비밀번호입니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        refresh = RefreshToken.for_user(user)  # JWT token 생성
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        user_data = User.objects.get(email=email)
        serializer = UserSerializer(user_data)

        # access token 은 JSON 응답으로 반환
        response = Response(
            {"access_token": access_token, "user": serializer.data},
            status=status.HTTP_200_OK,
        )
        # refresh token 은 httpOnly, secure cookie 에 저장
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,  # 자바스크립트에서 접근 불가능하게 설정
            secure=settings.REFRESH_TOKEN_COOKIE_SECURE,  # True: HTTPS 환경에서만 쿠키가 전송되도록 함
            samesite="Strict",  # 같은 사이트에서만 쿠키 전송
        )
        return response
