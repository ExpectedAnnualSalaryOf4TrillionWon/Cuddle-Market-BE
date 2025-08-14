from rest_framework import serializers
from apps.likes.models import Like
from apps.products.models import Product

class LikeCreateSerializer(serializers.ModelSerializer):
    # 찜 등록용 시리얼라이저

    class Meta:
        model = Like
        fields = ['Product_id']

    def validate_product_id(self, value):
        # 상품 존재 여부 확인
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("존재하지 않는 상품입니다.")
        return value
    
    def validate(self, attrs):
        # 중복 찜 방지
        user = self.context['request'].user
        product_id = attrs['product_id']

        if Like.objects.filter(user=user, Product_id=product_id).exists():
            raise serializers.ValidationError("이미 관심 목록에 등록된 상품입니다.")
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class LikeListSerializer(serializers.ModelSerializer):
    # 찜 목록 조회용 시리얼라이저
    Product_title = serializers.CharField(source='product.post.title', read_only = True)
    Product_price = serializers.IntegerField(source='product.price', read_only = True)
    product_status = serializers.CharField(source='product.status', read_only = True)

    class Meta:
        model = Like
        fields = [
            'id',
            'product_id',
            'product_title',
            'product_price',
            'product_status',
            'product_image',
            'create_at'
        ]
    
    def get_product_image(self, obj):
        # 상품의 첫 번쩨 이미지 URL 반환
        first_image = obj.product.images.first()
        if first_image:
            return first_image.image_url
        return None
    
class SimpleLikeSerializer(serializers.ModelSerializer):
    # API 문서 응답 형십에 맞춘 간단한 시리얼라이저

    class Mata:
        model = Like
        fields = ['product_id', 'create_at']