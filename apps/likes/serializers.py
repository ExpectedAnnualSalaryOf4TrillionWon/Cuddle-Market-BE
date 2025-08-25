from rest_framework import serializers
from apps.likes.models import ProductLike
from apps.products.models import Product
from django.db import IntegrityError


class ProductLikeSerializer(serializers.ModelSerializer):
    # 요청에서는 product_id 사용
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = ProductLike
        fields = ["product_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        product = validated_data["product"]

        # 중복 방지
        if ProductLike.objects.filter(user=user, product=product).exists():
            raise IntegrityError("이미 관심 상품으로 추가된 상품입니다.")

        return ProductLike.objects.create(user=user, product=product)

    def to_representation(self, instance):
        """
        응답을 명세서 형식에 맞게 변경
        """
        return {
            "message": "관심 목록에 추가되었습니다.",
            "product_id": instance.product.id,
            "is_liked": True,
        }


class LikeListSerializer(serializers.ModelSerializer):
    # 찜 목록 조회용 시리얼라이저
    product_id = serializers.IntegerField(source="product.id")
    title = serializers.CharField(source="product.title")
    price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2
    )
    view_count = serializers.IntegerField(source="product.view_count")
    transaction_status = serializers.CharField(source="product.transaction_status")
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = ProductLike
        fields = (
            "product_id",
            "title",
            "price",
            "thumbnail",
            "view_count",
            "transaction_status",
        )

    def get_thumbnail(self, obj):
        # 대표 이미지(is_main=True)가 있으면 그 URL 반환, 없으면 첫 번째 이미지
        main_image = obj.product.images.filter(is_main=True).first()
        if main_image:
            return main_image.url
        first_image = obj.product.images.first()
        return first_image.url if first_image else None


class LikeToggleSerializer(serializers.Serializer):
    # 찜 토글용 시리얼라이저
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 상품입니다.")
        return value

    # 찜 당한 상품게시글의 찜 갯수 시리얼라이저


class ProductLikeCountSerializer(serializers.ModelSerializer):
    like_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ["like_count"]
