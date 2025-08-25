from django.urls import path
from .views import ProductLikeToggleAPIView

urlpatterns = [
    path("", ProductLikeToggleAPIView.as_view(), name="likes"),
]