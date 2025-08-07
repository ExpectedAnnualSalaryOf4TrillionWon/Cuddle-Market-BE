# users/urls.py
from django.urls import path
from .views import (SignupView,LoginTokenView
                    ,LogoutView,
                    UserWithdrawView,
                    MyPageView,
                    ProfileUpdateView,)

urlpatterns = [
    path('signup/', SignupView.as_view(), name='user-signup'),
    path('login/', LoginTokenView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('withdraw/', UserWithdrawView.as_view(), name='user-withdraw'),
    path('mypage/', MyPageView.as_view(), name='mypage'),              # GET
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),  # PUT
]
