# product/urls.py
from django.urls import path

from apps.categories.views import AllCategoryDataAPIView

urlpatterns = [path("all-get", AllCategoryDataAPIView.as_view(), name="all-get")]
