# from django.contrib import admin
# from .models import Product, ProductImage  # ProductLike 제거

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'get_post_title', 'user', 'price', 'category', 'status', 'created_at')
#     list_filter = ('category', 'status')
#     search_fields = ('post__title', 'post__content')

#     @admin.display(description='제목')
#     def get_post_title(self, obj):
#         return obj.post.title

# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ('id', 'product', 'get_image_url')

#     @admin.display(description='이미지 URL')
#     def get_image_url(self, obj):
#         return obj.image_url

from django.contrib import admin

from .models import Product, ProductImage, ProductLike


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "post_title", "price", "status", "type", "created_at"]
    list_filter = ["status", "type", "category"]
    search_fields = ["post__title", "user__username"]

    def post_title(self, obj):
        return obj.post.title

    post_title.short_description = "게시글 제목"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ["id", "product_id", "image_url"]

    def product_id(self, obj):
        return obj.product.id

    product_id.short_description = "상품 ID"


@admin.register(ProductLike)
class ProductLikeAdmin(admin.ModelAdmin):
    list_display = ["id", "product", "user", "created_at"]
    search_fields = ["product__post__title", "user__username"]
