from django.contrib import admin
from .models import Product, ProductImage


# 상품 이미지 Inline (Product 상세 화면에서 이미지 여러 개 등록 가능)
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # 기본으로 보여줄 빈 폼 개수
    fields = ("url", "is_main", "uploaded_by", "uploaded_at")
    readonly_fields = ("uploaded_at",)


# 상품 Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "transaction_status",
        "condition_status",
        "view_count",
        "created_at",
        "updated_at",
        "user",
    )  # 목록에서 보이는 필드
    list_filter = ("transaction_status", "condition_status", "created_at")  # 필터 사이드바
    search_fields = ("title", "description", "user__nickname")  # 검색 기능
    ordering = ("-created_at",)  # 최신순 정렬
    inlines = [ProductImageInline]  # 상품 상세에 이미지 inline 추가


# 상품 이미지 Admin
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "url",
        "is_main",
        "uploaded_by",
        "uploaded_at",
    )
    list_filter = ("is_main", "uploaded_at")
    search_fields = ("product__title", "url")
