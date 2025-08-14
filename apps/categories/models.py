from django.db import models


class Category(models.Model):
    class CategoryName(models.TextChoices):
        TOY = "장난감", "장난감"
        FOOD = "사료", "사료"
        CLOTHES = "의류", "의류"
        SUPPLIES = "용품", "용품"

    class CategoryType(models.TextChoices):
        PRODUCT = "product", "상품"
        POST = "post", "게시글"

    name = models.CharField(
        max_length=50, choices=CategoryName.choices, verbose_name="카테고리명"
    )
    type = models.CharField(
        max_length=20, choices=CategoryType.choices, verbose_name="카테고리 유형"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
        verbose_name="상위 카테고리",
    )

    def __str__(self):
        return f"{self.get_type_display()} - {self.get_name_display()}"
