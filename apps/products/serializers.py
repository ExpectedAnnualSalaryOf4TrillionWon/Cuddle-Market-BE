from rest_framework import serializers
from django.db import transaction
from .models import Product, ProductImage
import uuid, boto3
from apps.s3_utils import upload_to_s3_and_get_url
from django.conf import settings
from apps.likes.models import ProductLike
from django.db.models import Count
import os, uuid

# ---------------------------------------------------------
# 상품 이미지 Serializer
# ---------------------------------------------------------
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "url", "is_main"]   # 이미지 PK, URL, 대표 여부


# ---------------------------------------------------------
# 상품 생성 Serializer (대표 이미지 + 서브 이미지 업로드 처리)
# ---------------------------------------------------------
class ProductCreateSerializer(serializers.ModelSerializer):
    # 대표 이미지(필수): 여러 장 올릴 수 있음
    main_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=True
    )
    # 서브 이미지(선택): 여러 장 가능
    sub_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            "title", "description", "price",
            "state_code", "city_code", "category_code",
            "pet_type_code", "pet_type_detail_code", "condition_status",
            "main_images", "sub_images",
        ]

    def create(self, validated_data):
        user = self.context["request"].user   # 요청 보낸 사용자
        main_files = validated_data.pop("main_images", [])
        sub_files = validated_data.pop("sub_images", [])

        # 트랜잭션 시작 (상품+이미지 생성 중 하나라도 실패하면 롤백)
        with transaction.atomic():
            # 상품 생성
            product = Product.objects.create(user=user, **validated_data)

            #  대표 이미지 필수 조건 체크
            if not main_files:
                raise serializers.ValidationError({"main_images": "대표 이미지는 최소 1장이 필요합니다."})

            # 대표 이미지 업로드 처리
            for idx, file in enumerate(main_files):
                object_name = f"products/{user.id}/{uuid.uuid4()}_{file.name}"  # S3에 저장될 경로
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                url = upload_to_s3_and_get_url(file, bucket_name, object_name) # 업로드 후 URL 반환
                if not url:
                    raise serializers.ValidationError({"main_images": "대표 이미지 업로드 실패"})

                # DB에 이미지 저장 (첫 번째 이미지는 대표 이미지로 설정)
                ProductImage.objects.create(
                    product=product,
                    url=url,
                    is_main=(idx == 0),
                    uploaded_by=user
                )

            # 서브 이미지 업로드 처리
            for file in sub_files:
                object_name = f"products/{user.id}/{uuid.uuid4()}_{file.name}"
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                url = upload_to_s3_and_get_url(file, bucket_name, object_name)
                if not url:
                    raise serializers.ValidationError({"sub_images": "서브 이미지 업로드 실패"})

                ProductImage.objects.create(
                    product=product,
                    url=url,
                    is_main=False,
                    uploaded_by=user
                )

        return product

    #  필요할 때 직접 boto3로 업로드할 수 있는 함수 (utils 안쓰고 바로 업로드)
    def upload_to_s3(self, file, user):
        """S3 업로드 후 URL 반환"""
        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
        )
        bucket = settings.AWS_STORAGE_BUCKET_NAME

        filename = f"products/{user.id}/{uuid.uuid4()}_{file.name}"

        s3.upload_fileobj(
            file,
            bucket,
            filename,
            ExtraArgs={"ACL": "public-read", "ContentType": file.content_type},
        )

        return f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
    

# ---------------------------------------------------------
# 상품 카드용 Serializer (목록 조회에서 사용)
# ---------------------------------------------------------
class ProductCardSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()   # 대표 이미지
    like_count = serializers.SerializerMethodField()  # 좋아요 수
    elapsed_time = serializers.SerializerMethodField() # 등록 후 경과 시간

    class Meta:
        model = Product
        fields = [
            "id", "thumbnail", "title", "price",
            "pet_type_code", "condition_status",
            "transaction_status", "elapsed_time",
            "like_count",
        ]

    # 대표 이미지 가져오기
    def get_thumbnail(self, obj):
        main_image = obj.images.filter(is_main=True).first()
        return main_image.url if main_image else None

    # 좋아요 수 카운트
    def get_like_count(self, obj):
        return obj.likes.count()

    # 등록 후 경과 시간 계산
    def get_elapsed_time(self, obj):
        from django.utils.timesince import timesince
        from django.utils import timezone
        return timesince(obj.created_at, timezone.now()) + " 전"
    

# ---------------------------------------------------------
# 판매자의 다른 상품 Serializer (상품 상세 조회 시 같이 제공)
# ---------------------------------------------------------
class SellerProductSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    elapsed_time = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "thumbnail", "title", "price", "condition_status", "transaction_status", "elapsed_time", "like_count"]

    # 대표 이미지
    def get_thumbnail(self, obj):
        main_img = obj.images.filter(is_main=True).first()
        return main_img.url if main_img else None

    # 등록 후 경과 시간
    def get_elapsed_time(self, obj):
        from django.utils.timesince import timesince
        return timesince(obj.created_at) + " 전"

    # 좋아요 수
    def get_like_count(self, obj):
        return ProductLike.objects.filter(product=obj).count()


# ---------------------------------------------------------
# 상품 상세 페이지 Serializer
# ---------------------------------------------------------
class ProductDetailSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)   # 상품 이미지 전체
    like_count = serializers.SerializerMethodField()             # 좋아요 수
    seller_info = serializers.SerializerMethodField()            # 판매자 정보
    seller_products = serializers.SerializerMethodField()        # 판매자의 다른 상품들

    class Meta:
        model = Product
        fields = [
            "id", "title", "description", "price",
            "state_code", "city_code", "category_code",
            "pet_type_code", "pet_type_detail_code",
            "transaction_status", "condition_status",
            "view_count", "like_count", "images",
            "seller_info", "seller_products",
        ]

    # 좋아요 수
    def get_like_count(self, obj):
        return ProductLike.objects.filter(product=obj).count()

    # 판매자 정보 반환
    def get_seller_info(self, obj):
        user = obj.user
        return {
            "id": user.id,
            "seller_images": user.profile_image,
            "nickname": user.nickname,
            "state": user.state_id,
            "city": user.city_id,
        }

    # 판매자의 다른 상품 (최대 5개)
    def get_seller_products(self, obj):
        products = Product.objects.filter(user=obj.user).exclude(id=obj.id)[:5]
        return SellerProductSerializer(products, many=True).data
