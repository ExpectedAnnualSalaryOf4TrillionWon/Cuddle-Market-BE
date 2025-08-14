from django.urls import path
from .views import LikeAPIView

urlspatterns = [
    path('', LikeAPIView.as_view(), name='likes'),
]