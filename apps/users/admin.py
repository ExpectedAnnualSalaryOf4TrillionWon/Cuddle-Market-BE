from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id", 
        "email", 
        "nickname", 
        "is_active", 
        "is_staff", 
        "is_superuser", 
        "created_at",  # date_joined 대신 created_at 사용
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "nickname")
    ordering = ("-id",)
    readonly_fields = ("created_at", "updated_at", "last_login")  # 이 줄 추가
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("개인정보", {"fields": ("nickname", "name", "profile_image", "birthday", "state", "city")}),
        ("권한", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("상태", {"fields": ("profile_completed",)}),
        ("중요 일자", {"fields": ("last_login", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "nickname",
                "password1",
                "password2",
                "is_active",
                "is_staff",
                "is_superuser",
            ),
        }),
    )

