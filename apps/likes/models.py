from django.db import models
from django.conf import settings
from apps.products.models import Product


# 상품 찜(Like) 테이블
class ProductLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=False,   # PK는 따로 지정하지 않음 (아래에서 복합키로 처리)
    )
    # → 찜한 사용자 (회원 삭제되면 찜 기록도 삭제됨)

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        primary_key=False,   # 동일
    )
    # → 찜한 상품 (상품 삭제되면 찜 기록도 삭제됨)

    created_at = models.DateTimeField(auto_now_add=True)
    # → 찜한 시간 기록

    class Meta:
        # ERD처럼 user_id + product_id = PK (중복 방지)
        unique_together = ("user", "product")
        db_table = "product_like"  # 테이블명 명시 (snake_case)

    def __str__(self):
        return f"{self.user} liked {self.product}"
