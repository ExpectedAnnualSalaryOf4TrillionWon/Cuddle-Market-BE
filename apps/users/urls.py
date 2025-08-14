# users/urls.py
from django.urls import path

from .views import (
    LoginTokenView,
    LogoutView,
    MyPageView,
    ProfileUpdateView,
    SignupView,
    UserProfileView,
    UserWithdrawView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="user-signup"),  # 회원가입
    path("login/", LoginTokenView.as_view(), name="login"),  # 로그인
    path("logout/", LogoutView.as_view(), name="logout"),  # 로그아웃
    path("withdraw/", UserWithdrawView.as_view(), name="user-withdraw"),  # 회원탈퇴
    path("mypage/", MyPageView.as_view(), name="mypage"),  # 마이 페이지 조회(본인)
    path("profile/", ProfileUpdateView.as_view(), name="profile-update"),  # 프로필수정
    path(
        "<int:pk>/profile/", UserProfileView.as_view(), name="user-profile"
    ),  # 유저 조회(타 유저)
]
