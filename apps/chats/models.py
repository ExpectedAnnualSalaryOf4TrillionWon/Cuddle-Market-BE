from django.db import models
from django.conf import settings
from apps.products.models import Product


# 채팅방 테이블
class ChatRoom(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chatrooms_as_buyer"
    )  # 구매자
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chatrooms_as_seller"
    )  # 판매자
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="chatrooms"
    )  # 대상 상품
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일시

    class Meta:
        db_table = "chat_room"

    def __str__(self):
        return f"ChatRoom {self.id} - {self.product.title}"


# 채팅 메시지 테이블
class ChatMessage(models.Model):
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name="messages"
    )  # 채팅방
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )  # 발신자
    message = models.CharField(max_length=1000, null=False)  # 메시지 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 발신 시간

    class Meta:
        db_table = "chat_message"

    def __str__(self):
        return f"{self.sender} in {self.chat_room.id}: {self.message[:20]}"
