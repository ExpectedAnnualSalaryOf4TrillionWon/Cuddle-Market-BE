from django.urls import path

from .views import (
    KakaoAuthView,
    TokenRefreshView, SocialProfileRegistrationView, LogoutView,

)

urlpatterns = [
    path("token-refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("kakao-auth/", KakaoAuthView.as_view(), name="kakao-auth"),
    path("profile-complete/", SocialProfileRegistrationView.as_view(), name="profile-complete"),
    path("logout/", LogoutView.as_view(), name="logout"),
]