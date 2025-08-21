# config/urls.py
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.conf.urls.static import static
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/categories/", include("apps.categories.urls")),
    path("api/v1/", include("apps.chats.urls")),
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

if settings.DEBUG:# 개발 모드일 때만 static 서빙
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)