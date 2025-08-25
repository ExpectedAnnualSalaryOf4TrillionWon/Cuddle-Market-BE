from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.db import IntegrityError

from .models import ProductLike
from apps.products.models import Product
from apps.likes.serializers import (
    LikeListSerializer,
    ProductLikeCountSerializer,
    ProductLikeSerializer,
)


class ProductLikeToggleAPIView(APIView):
    """
    관심 목록 (찜) 추가 / 삭제 / 조회
    - GET    : 내 관심목록 전체 조회
    - POST   : 관심 등록 추가
    - DELETE : 관심 등록 삭제
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # GET /api/v1/likes/ - 내 관심목록 전체 조회
        likes = (
            ProductLike.objects.filter(user=request.user)
            .select_related("product", "product__user")
            .prefetch_related("product__images")
        )

        serializer = LikeListSerializer(likes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # POST /api/v1/likes/ - 관심 등록 추가
        serializer = ProductLikeSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            try:
                like = serializer.save()
                return Response(
                    {
                        "message": "관심 목록에 추가되었습니다.",
                        "product_id": like.product.id,
                        "is_liked": True,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                return Response(
                    {"error": "이미 관심 상품으로 추가된 상품입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        # DELETE /api/v1/likes/ - 관심 등록 삭제
        product_id = request.data.get("product_id") or request.query_params.get(
            "product_id"
        )

        if not product_id:
            return Response(
                {"error": "product_id가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            like = ProductLike.objects.get(user=request.user, product_id=product_id)
            like.delete()
            return Response(
                {
                    "message": "관심 목록에서 삭제되었습니다.",
                    "product_id": int(product_id),
                    "is_liked": False,
                },
                status=status.HTTP_200_OK,
            )

        except ProductLike.DoesNotExist:
            return Response(
                {"error": "관심 등록되지 않은 상품입니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Product.DoesNotExist:
            return Response(
                {"error": "존재하지 않는 상품입니다."}, status=status.HTTP_404_NOT_FOUND
            )


class ProductLikeCountView(generics.RetrieveAPIView):  # 특정 상품의 찜 개수
    serializer_class = ProductLikeCountSerializer
    queryset = Product.objects.annotate(like_count=Count("likes"))
