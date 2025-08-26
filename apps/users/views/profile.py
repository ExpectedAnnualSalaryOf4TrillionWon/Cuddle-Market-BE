from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.users.serializers import UserSerializer, UpdateMyPageSerializer
from rest_framework.parsers import MultiPartParser

User = get_user_model()


class MyProfileView(APIView):
    """
    마이 페이지 API
    """
    parser_classes = (MultiPartParser,)

    @extend_schema(
        summary="회원 정보 조회",
        description="회원 정보를 조회하는 API입니다",
        responses={200, UserSerializer},
        tags=["User"],
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="회원 정보 수정",
        description="회원 정보를 수정하는 API입니다",
        request=UpdateMyPageSerializer,
        tags=["User"],
    )
    def patch(self, request, *args, **kwargs):
        user = request.user
        # PATCH 요청 시에는, Serializer가 update 메서드를 통해 파일 업로드 및 URL 변환을 처리
        serializer = UpdateMyPageSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()
        return Response(UpdateMyPageSerializer(instance).data, status=status.HTTP_200_OK)
