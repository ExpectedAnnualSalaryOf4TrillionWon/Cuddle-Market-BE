from django.db import models
from django.conf import settings   # AUTH_USER_MODEL (커스텀 유저) 참조할 때 필요


# 반려동물 종류 테이블 (예: 포유류, 조류 등)
class PetType(models.Model):
    code = models.CharField(max_length=50, unique=True, null=False)  # 고유 코드 (예: "MAMMAL01")
    name = models.CharField(max_length=100, null=False)  # 종류명 (예: 포유류)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일 (자동 기록)
    updated_at = models.DateTimeField(auto_now=True)      # 수정일 (자동 기록)

    def __str__(self):
        return self.name   # admin 등에서 표시될 때 이름 반환


# 반려동물 상세 종류 테이블 (예: 강아지, 고양이 등)
class PetTypeDetail(models.Model):
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE, related_name="details")  
    # → PetType과 1:N 관계 (예: 포유류 → 강아지/고양이)
    code = models.CharField(max_length=50, unique=True, null=False)  # 상세 코드 (예: "DOG01")
    name = models.CharField(max_length=100, null=False)  # 상세명 (예: 강아지)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)      # 수정일

    def __str__(self):
        return f"{self.pet_type.name} - {self.name}"  # 예: "포유류 - 강아지"


# 상품 테이블
class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")  
    # → 상품 작성자 (User)와 연결, 유저 삭제 시 상품도 같이 삭제됨

    # ERD에서 code 값으로만 저장하는 필드들 (FK 아님, 문자열 그대로 저장)
    state_code = models.CharField(max_length=50, null=True, blank=True)       # 등록 지역 (시/도) 코드
    city_code = models.CharField(max_length=50, null=True, blank=True)        # 등록 지역 (시/군/구) 코드
    category_code = models.CharField(max_length=50, null=True, blank=True)    # 카테고리 코드
    pet_type_code = models.CharField(max_length=50, null=True, blank=True)    # 반려동물 종류 코드
    pet_type_detail_code = models.CharField(max_length=50, null=True, blank=True)  # 반려동물 상세 종류 코드

    # 상품 정보
    title = models.CharField(max_length=50, null=False)  # 상품 제목
    description = models.TextField(max_length=500, blank=True, null=True)  # 상품 설명 (선택)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)  # 상품 가격 (최대 99999999.99)

    # 거래 상태 (enum 대응)
    TRANSACTION_CHOICES = [
        ("SELLING", "판매중"),
        ("RESERVED", "예약중"),
        ("SOLD", "판매완료"),
    ]
    transaction_status = models.CharField(
        max_length=10, choices=TRANSACTION_CHOICES, default="SELLING"
    )  # 기본값은 판매중

    # 상품 상태 
    CONDITION_CHOICES = [
        ("NEW", "새상품"),
        ("LIKE_NEW", "거의 새것"),
        ("USED", "사용감 있음"),
        ("NEEDS_REPAIR", "수리 필요"),
    ]
    condition_status = models.CharField(
        max_length=15, choices=CONDITION_CHOICES, null=True, blank=True
    )  # 상품 상태 (선택)

    # 조회수
    view_count = models.BigIntegerField(default=0)  # 기본 0회

    # 생성/수정 시간
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)      # 수정일

    def __str__(self):
        return f"[{self.id}] {self.title} - {self.price}원"  # admin 등에서 보기 좋게 출력


# 상품 이미지 테이블
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")  
    # → 하나의 상품에 여러 이미지 연결 가능
    url = models.URLField(max_length=255)  # 이미지 경로 (URL 저장)
    is_main = models.BooleanField(default=False)  # 대표 이미지 여부 (True/False)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)  
    # → 업로더 유저 (삭제되면 null 처리)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 업로드 시각

    def __str__(self):
        return f"Image for {self.product.title}"  # admin 표시용
