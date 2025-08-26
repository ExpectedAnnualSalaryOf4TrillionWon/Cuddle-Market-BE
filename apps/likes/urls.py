from django.urls import path
from .views import ProductLikeAPIView

urlpatterns = [
    path("", ProductLikeAPIView.as_view(), name="likes"),
]
