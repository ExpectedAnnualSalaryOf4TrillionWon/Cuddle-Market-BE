from rest_framework import serializers
from .models import Product, ProductImage, ProductLike


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image_url", "image_order", "created_at"]


class ProductLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLike
        fields = ["id", "user", "product", "created_at"]
        read_only_fields = ["id", "created_at"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(
        many=True, source="productimage_set", read_only=True
    )
    like_count = serializers.IntegerField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)  # 유저 닉네임 등 표시용

    class Meta:
        model = Product
        fields = [
            "id",
            "user",
            "title",
            "description",
            "price",
            "category",
            "condition_status",
            "trade_method",
            "location",
            "status",
            "view_count",
            "like_count",
            "images",
            "created_at",
            "updated_at",
        ]

    def validate_title(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("제목은 50자 이내여야 합니다.")
        return value

    def validate_description(self, value):
        if len(value) > 1000:
            raise serializers.ValidationError("설명은 1000자 이내여야 합니다.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("가격은 0 이상의 숫자여야 합니다.")
        return value

    def validate_category(self, value):
        allowed = ["food", "toy", "clothing", "supplies", "health", "etc"]
        if value not in allowed:
            raise serializers.ValidationError(
                f"카테고리는 {allowed} 중 하나여야 합니다."
            )
        return value

    def validate_condition_status(self, value):
        allowed = ["new", "like_new", "used", "damaged"]
        if value not in allowed:
            raise serializers.ValidationError(
                f"상품 상태는 {allowed} 중 하나여야 합니다."
            )
        return value

    def validate_trade_method(self, value):
        # trade_method가 SET('direct','delivery')로 여러개 선택 가능하면
        # 여기는 단일 문자열로 받으니, 복수 선택 지원하려면 커스텀 처리 필요
        allowed = ["direct", "delivery"]
        for method in value.split(","):
            if method not in allowed:
                raise serializers.ValidationError(
                    f"거래 방식은 {allowed} 중 하나 이상이어야 합니다."
                )
        return value
