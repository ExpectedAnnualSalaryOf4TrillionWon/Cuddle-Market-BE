# users/views.py
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import IsAuthenticated
from .Serializer import MyPageSerializer, ProfileUpdateSerializer
from .Serializer import UserWithdrawSerializer
from apps.users.Serializer import UserSignupSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveAPIView

from .Serializer import PublicUserProfileSerializer

# 회원가입을 처리하는 APIView 클래스 정의
class SignupView(APIView):
    def post(self, request):  # POST 요청이 들어오면 실행되는 메서드
        serializer = UserSignupSerializer(
            data=request.data
        )  # 요청 데이터를 시리얼라이저에 담음
        if serializer.is_valid():  # 데이터 유효성 검사 통과하면(이직렬화가 유효한지!!?)
            serializer.save()  # 사용자 생성 (User 모델에 저장)
            return Response(
                {"message": "회원가입이 완료되었습니다."},
                status=status.HTTP_201_CREATED,
            )  # 성공 응답 반환
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # 유효성 검사 실패 시 에러 반환


# 로그아웃 동시에 쿠키가 블랙리스트에 들어간다음 삭제까지 로직 ~
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 요청 가능

    def post(self, request):
        try:
            #  쿠키에서 refresh 토큰 가져오기
            refresh_token = request.COOKIES.get("refresh")

            #  refresh 토큰이 없으면 에러 반환
            if refresh_token is None:
                return Response(
                    {"detail": "Refresh 토큰이 없습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            #  토큰 객체로 변환 후 블랙리스트에 등록
            token = RefreshToken(refresh_token)
            token.blacklist()  # DB에 저장됨 (유효한 토큰이지만 사용 불가 처리)

            #  쿠키 삭제 및 성공 응답
            response = Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
            response.delete_cookie("access")  # access 쿠키 제거
            response.delete_cookie("refresh")  # refresh 쿠키 제거

            return response  # 최종 응답 반환

        except TokenError:
            #  토큰이 유효하지 않은 경우 예외 처리
            return Response(
                {"detail": "유효하지 않은 토큰입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 회원 탈퇴 뷰 (로그인된 사용자만 요청 가능)
class UserWithdrawView(APIView):
    permission_classes = [IsAuthenticated]  # JWT 인증 필요

    def delete(self, request):
        user = request.user  # 현재 로그인된 사용자
        serializer = UserWithdrawSerializer(user, data={}, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()  # is_active=False 처리
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )  # 응답: 탈퇴 완료 (내용 없음)


class MyPageView(APIView):
    permission_classes = [IsAuthenticated]  # JWT 인증된 사용자만 접근 가능

    def get(self, request):
        # 현재 로그인된 사용자 정보를 직렬화
        serializer = MyPageSerializer(request.user)
        # JSON 형식으로 응답 반환
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]  # JWT 인증된 사용자만 접근 가능

    def put(self, request):
        # 현재 사용자 + 전달받은 데이터로 시리얼라이저 초기화
        serializer = ProfileUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()  # nickname, profile_img, region 필드 수정 반영
            return Response(serializer.data, status=status.HTTP_200_OK)
        # 유효하지 않으면 오류 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveAPIView):
    User = get_user_model()  # 기억상 유저 정의
    queryset = User.objects.filter(is_active=True)  # 탈퇴한 유저는 제외
    serializer_class = PublicUserProfileSerializer
    lookup_field = "pk"  # URL의 <user_id> 부분을 기준으로 조회

    def get(self, request, *args, **kwargs):
        # pk로 유저 조회
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
