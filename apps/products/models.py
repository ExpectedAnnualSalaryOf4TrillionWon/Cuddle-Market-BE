# from django.db import models
# from django.conf import settings


# class Product(models.Model):
#     class StatusChoices(models.TextChoices):
#         SELLING = '판매중', '판매중'
#         RESERVED = '예약중', '예약중'
#         SOLD = '판매완료', '판매완료'

#     class TypeChoices(models.TextChoices):
#         SELL = 'sell', '판매'
#         BUY = 'buy', '구매'

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='products',
#         verbose_name='등록한 사용자'
#     )
#     post = models.ForeignKey(
#         'posts.Post',
#         on_delete=models.CASCADE,
#         related_name='products',
#         verbose_name='연결된 게시글'
#     )
#     category = models.ForeignKey(
#         'categories.Category',
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='products',
#         verbose_name='카테고리'
#     )
#     price = models.PositiveIntegerField(verbose_name='가격')
#     status = models.CharField(
#         max_length=10,
#         choices=StatusChoices.choices,
#         default=StatusChoices.SELLING,
#         verbose_name='거래 상태'
#     )
#     type = models.CharField(
#         max_length=10,
#         choices=TypeChoices.choices,
#         verbose_name='게시글 유형'
#     )
#     location = models.CharField(
#         max_length=100,
#         blank=True,
#         verbose_name='지역 필터용'
#     )
#     method = models.CharField(
#         max_length=20,
#         choices=[('직거래', '직거래'), ('택배', '택배')],
#         blank=True,
#         verbose_name='거래 방식'
#     )
#     is_deleted = models.BooleanField(default=False, verbose_name='삭제 여부')
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')

#     def __str__(self):
#         return f"{self.post.title} - {self.price}원"


# class ProductImage(models.Model):
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='images',
#         verbose_name='상품'
#     )
#     image_url = models.URLField(verbose_name='이미지 URL')

#     def __str__(self):
#         return f"Product {self.product.id}의 이미지"


# class ProductLike(models.Model):
#     product = models.ForeignKey(
#         Product,
#         on_delete=models.CASCADE,
#         related_name='product_likes',  # 충돌 방지를 위해 변경됨
#         verbose_name='좋아요 상품'
#     )
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='liked_products',
#         verbose_name='좋아요 누른 사용자'
#     )
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name='좋아요 누른 시각')

#     class Meta:
#         unique_together = ('product', 'user')
#         verbose_name = '상품 좋아요'
#         verbose_name_plural = '상품 좋아요 목록'

#     def __str__(self):
#         return f"{self.user} likes {self.product}"


"""
구분선

"""

from django.conf import settings
from django.db import models


class Product(models.Model):
    class StatusChoices(models.TextChoices):
        SELLING = "판매중", "판매중"
        RESERVED = "예약중", "예약중"
        SOLD = "판매완료", "판매완료"

    class TypeChoices(models.TextChoices):
        SELL = "sell", "판매"
        BUY = "buy", "구매"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # 사용자 모델 유지
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="등록한 사용자",
    )
    # post 필드 임시 주석 처리
    # post = models.ForeignKey(
    #     'posts.Post',
    #     on_delete=models.CASCADE,
    #     related_name='products',
    #     verbose_name='연결된 게시글'
    # )

    # category FK 대신 CharField 로 변경
    category = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="카테고리"
    )

    price = models.PositiveIntegerField(verbose_name="가격")
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.SELLING,
        verbose_name="거래 상태",
    )
    type = models.CharField(
        max_length=10, choices=TypeChoices.choices, verbose_name="게시글 유형"
    )
    location = models.CharField(max_length=100, blank=True, verbose_name="지역 필터용")
    method = models.CharField(
        max_length=20,
        choices=[("직거래", "직거래"), ("택배", "택배")],
        blank=True,
        verbose_name="거래 방식",
    )
    is_deleted = models.BooleanField(default=False, verbose_name="삭제 여부")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일")

    def __str__(self):
        return f"{self.category} - {self.price}원"  # post.title 대신 category 로 대체


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images", verbose_name="상품"
    )
    image_url = models.URLField(verbose_name="이미지 URL")

    def __str__(self):
        return f"Product {self.product.id}의 이미지"


class ProductLike(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_likes",
        verbose_name="좋아요 상품",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="liked_products",
        verbose_name="좋아요 누른 사용자",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="좋아요 누른 시각"
    )

    class Meta:
        unique_together = ("product", "user")
        verbose_name = "상품 좋아요"
        verbose_name_plural = "상품 좋아요 목록"

    def __str__(self):
        return f"{self.user} likes {self.product}"
