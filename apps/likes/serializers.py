from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import ProductLike
from apps.products.models import Product
from django.db import transaction


class ProductLikeSerializer(serializers.ModelSerializer):
    # 요청: product_id (BIGINT 범위 검증)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ProductLike
        fields = ["product_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        product_id = validated_data["product_id"]

        # 트랜잭션으로 동시성 문제 방지
        with transaction.atomic():
            try:
                # Product 객체를 직접 가져오기 (FK 무결성 보장)
                product = Product.objects.select_for_update().get(id=product_id)
            except Product.DoesNotExist:
                raise ValidationError("존재하지 않는 상품입니다.")
        # race condition 방지를 위해 get_or_create 사용
        like, created = ProductLike.objects.get_or_create(user=user, product=product)

        if not created:
            raise ValidationError("이미 관심 상품으로 추가된 상품입니다.")

        return like

    def to_representation(self, instance):
        return {
            "message": "관심 목록에 추가되었습니다.",
            "product_id": instance.product_id,  # FK → _id 자동 제공
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


class ProductLikeDeleteSerializer(serializers.Serializer):
    # 이 필드는 오직 쓰기(입력)용입니다.
    product_id = serializers.IntegerField(write_only=True)

    # Meta 클래스는 ModelSerializer가 아니므로 필요 없습니다.

    def validate(self, attrs):
        user = self.context["request"].user
        product_id = attrs.get("product_id")

        if product_id is None:
            raise serializers.ValidationError({"product_id": "이 필드는 필수입니다."})

        # 1. 상품 존재 여부 확인
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError(
                {"product_id": "존재하지 않는 상품입니다."}
            )

        # 2. 현재 유저가 해당 상품을 '좋아요' 했는지 확인
        try:
            like_instance = ProductLike.objects.get(user=user, product=product)
        except ProductLike.DoesNotExist:
            raise serializers.ValidationError(
                {"product_id": "관심 등록되지 않은 상품입니다."}
            )

        # 3. 검증이 끝난 인스턴스를 attrs에 추가하여 View에서 사용
        attrs["like_instance"] = like_instance
        return attrs
