from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ProductLike
from apps.likes.serializers import (
    LikeListSerializer,
    ProductLikeSerializer,
    ProductLikeDeleteSerializer,
)

class ProductLikeToggleAPIView(APIView):
    """
    관심 목록 (찜) 추가 / 삭제 / 조회
    - GET    : 내 관심목록 전체 조회
    - POST   : 관심 등록 추가
    - DELETE : 관심 등록 삭제
    """
    def get(self, request):
        # GET /api/v1/likes/ - 내 관심목록 전체 조회
        likes = ProductLike.objects.filter(
            user=request.user
        ).select_related(
            "product", "product__user"
        ).prefetch_related("product__images")

        serializer = LikeListSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
    # POST /api/v1/likes/ - 관심 등록 추가
        serializer = ProductLikeSerializer(
        data=request.data,
        context={"request": request}
    )
        serializer.is_valid(raise_exception=True)  # 유효성 검사 실패 시 자동으로 400 반환

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def delete(self, request):
        serializer = ProductLikeDeleteSerializer(
            data=request.data or request.query_params,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        result = serializer.delete()
        return Response(result, status=status.HTTP_200_OK)

