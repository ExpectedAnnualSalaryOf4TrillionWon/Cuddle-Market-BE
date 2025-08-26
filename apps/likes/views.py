from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ProductLike
from apps.likes.serializers import (
    LikeListSerializer,
    ProductLikeSerializer,
    ProductLikeDeleteSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse


class ProductLikeAPIView(APIView):
    """
    관심 목록 (찜) 추가 / 삭제 / 조회
    - GET    : 내 관심목록 전체 조회
    - POST   : 관심 등록 추가
    - DELETE : 관심 등록 삭제
    """

    @extend_schema(
        summary="내 관심 목록 조회",
        description="현재 로그인한 사용자의 관심 상품 목록 전체를 조회합니다.",
        responses={200: LikeListSerializer(many=True)},
    )
    def get(self, request):
        # GET /api/v1/likes/ - 내 관심목록 전체 조회
        likes = (
            ProductLike.objects.filter(user=request.user)
            .select_related("product", "product__user")
            .prefetch_related("product__images")
        )

        serializer = LikeListSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="관심 상품 추가",
        description="특정 상품을 현재 로그인한 사용자의 관심 목록에 추가합니다.",
        request=ProductLikeSerializer,
        responses={
            201: ProductLikeSerializer,
            400: OpenApiResponse(description="잘못된 요청 또는 이미 관심 목록에 있음"),
        },
    )
    def post(self, request):
        # POST /api/v1/likes/ - 관심 등록 추가
        serializer = ProductLikeSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(
            raise_exception=True
        )  # 유효성 검사 실패 시 자동으로 400 반환

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="관심 상품 삭제",
        description="특정 상품을 현재 로그인한 사용자의 관심 목록에서 삭제합니다.",
        request={
            "application/json": ProductLikeDeleteSerializer,
        },
        responses={
            200: ProductLikeDeleteSerializer,
            400: OpenApiResponse(description="잘못된 요청 또는 삭제할 상품이 없음"),
        },
    )
    def delete(self, request):
        serializer = ProductLikeDeleteSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        like_to_delete = serializer.validated_data["like_instance"]
        product_id = like_to_delete.product.id

        like_to_delete.delete()
        return Response(
            {
                "message": "관심 목록에서 삭제되었습니다.",
                "product_id": product_id,
            },
            status=status.HTTP_200_OK,
        )
