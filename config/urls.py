# config/urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/products/", include("apps.products.urls")),
    path("api/v1/categories/", include("apps.categories.urls")),
]

if settings.DEBUG:
    urlpatterns += (
        path(
            "docs/",
            SpectacularSwaggerView.as_view(),
            name="swagger-ui",
        ),
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "redoc/",
            SpectacularRedocView.as_view(),
            name="redoc",
        ),
    )
