from django.urls import path
from django.conf import settings
from .views.auth import (
    KakaoAuthView,
    TokenRefreshView,
    SocialProfileRegistrationView,
    LogoutView,
    DevLoginView,
    WithdrawalView,
)

urlpatterns = [
    path("token-refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("kakao-auth/", KakaoAuthView.as_view(), name="kakao-auth"),
    path(
        "profile-complete/",
        SocialProfileRegistrationView.as_view(),
        name="profile-complete",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("withdrawal/", WithdrawalView.as_view(), name="withdrawal"),
]

if settings.DEBUG:
    urlpatterns += (
        path(
            "dev-login/",
            DevLoginView.as_view(),
            name="swagger-ui",
        ),
    )
