# apps/likes/admin.py
from django.contrib import admin
from .models import ProductLike


@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "product",
        "created_at",
    )  # 어드민 리스트에서 보이는 필드
    list_filter = ("created_at", "user")  # 필터 사이드바
    search_fields = (
        "user__email",  # 유저 이메일 기준 검색
        "product__title",  # 상품 제목 기준 검색
    )
    ordering = ("-created_at",)  # 최신순 정렬
