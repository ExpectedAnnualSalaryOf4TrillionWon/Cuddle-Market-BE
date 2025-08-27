from django.urls import path
from .views import ProductListAPIView, ProductCreateAPIView, ProductDetailAPIView

urlpatterns = [
    path("", ProductListAPIView.as_view(), name="product-list"),
    path("create/", ProductCreateAPIView.as_view(), name="product-create"),
    path("<int:product_id>/", ProductDetailAPIView.as_view(), name="product-detail"),
]
