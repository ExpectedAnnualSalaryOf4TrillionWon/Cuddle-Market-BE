from django.urls import path
from .views import ProductLikeToggleAPIView, ProductLikeCountView

urlpatterns = [
    path("", ProductLikeToggleAPIView.as_view(), name="likes"),
    path("<int:pk>/count/", ProductLikeCountView.as_view(), name="product-like-count"),
]
