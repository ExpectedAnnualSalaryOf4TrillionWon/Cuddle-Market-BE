from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import Product
from .serializers import (
    ProductCreateSerializer,
    ProductCardSerializer,
    ProductDetailSerializer,
)

class ProductAPIView(APIView):
    """
    /api/v1/products
    - GET  : 상품 목록 조회
    - POST : 상품 등록 (로그인 필요)
    """

    def get(self, request):
        last_id = request.query_params.get("last_id")
        size = int(request.query_params.get("size", 20))

        queryset = Product.objects.prefetch_related("images").order_by("-id")
        if last_id:
            queryset = queryset.filter(id__lt=last_id)

        products = queryset[:size]
        serializer = ProductCardSerializer(products, many=True)

        return Response({"product_list": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()

        return Response({"message": "상품 등록 완료"}, status=status.HTTP_201_CREATED)


class ProductDetailAPIView(APIView):
    """
    상품 상세 조회 API
    GET /api/v1/products/{product_id}/
    """
    authentication_classes = []  # 인증 불필요
    permission_classes = []

    def get(self, request, product_id):
        # 상품 + 이미지 같이 가져오기
        product = get_object_or_404(
            Product.objects.prefetch_related("images"), id=product_id
        )

        # 조회수 증가 (동시성 안전)
        product.view_count = F("view_count") + 1
        product.save(update_fields=["view_count"])
        product.refresh_from_db(fields=["view_count"])

        serializer = ProductDetailSerializer(product, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
