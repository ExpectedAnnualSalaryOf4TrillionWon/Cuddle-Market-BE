from django.conf import settings
from django.db import models


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name="사용자",
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="likes",
        verbose_name="찜한 상품",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="찜한 날짜")

    class Meta:
        unique_together = ("user", "product")  # 중복 찜 방지
        verbose_name = "찜"
        verbose_name_plural = "찜 목록"

    def __str__(self):
        return f"{self.user.nickname} → {self.product.post.title}"
