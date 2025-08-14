from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, ProductImage
from .serializers import (
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_deleted=False).order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "status", "method", "location"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "price", "like_count"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        # 소프트 삭제 처리
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save()

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        product = self.get_object()
        user = request.user
        liked, created = ProductLike.objects.get_or_create(user=user, product=product)
        if not created:
            liked.delete()
            return Response({"detail": "Like removed"}, status=status.HTTP_200_OK)
        return Response({"detail": "Product liked"}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def upload_images(self, request, pk=None):
        product = self.get_object()
        files = request.FILES.getlist("images")
        # 이미지 검증 (형식, 크기) 로직 필요
        # 이미지 업로드 및 순서 지정 처리 필요
        # 예시로 기존 이미지 삭제 후 재등록 로직 작성 가능
        product.productimage_set.all().delete()
        for idx, file in enumerate(files):
            ProductImage.objects.create(
                product=product, image_url=file, image_order=idx
            )
        return Response({"detail": "Images uploaded"}, status=status.HTTP_201_CREATED)
