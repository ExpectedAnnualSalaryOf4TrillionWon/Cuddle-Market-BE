from django.contrib import admin
from .models import ChatRoom, ChatMessage


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "seller", "product", "created_at")
    list_filter = ("created_at", "product")
    search_fields = (
        "buyer__email",
        "buyer__nickname",
        "seller__email",
        "seller__nickname",
        "product__title",
    )
    ordering = ("-created_at",)

    # FK 필드 선택 시 자동완성 (유저/상품 많을 경우 편리)
    autocomplete_fields = ("buyer", "seller", "product")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat_room", "sender", "short_message", "created_at")
    list_filter = ("created_at", "sender")
    search_fields = ("sender__email", "sender__nickname", "message")
    ordering = ("-created_at",)

    autocomplete_fields = ("chat_room", "sender")

    # 긴 메시지는 리스트에서 잘리도록 커스텀
    def short_message(self, obj):
        return obj.message[:30] + ("..." if len(obj.message) > 30 else "")

    short_message.short_description = "Message"
