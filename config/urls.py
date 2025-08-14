# config/urls.py
from django.contrib import admin
from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/users/', include('apps.users.urls')),
#     path('api/', include('apps.products.urls')),
#     path('api/', include('apps.posts.urls')),
#     # 댓글 API 연결
# ]
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("apps.users.urls")),
    path("api/products/", include("apps.products.urls")),
    path("api/posts/", include("apps.posts.urls")),
]
