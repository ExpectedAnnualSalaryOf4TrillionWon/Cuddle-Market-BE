from django.db import models
from django.conf import settings


class ChatRoom(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chatrooms_as_buyer',
        verbose_name='구매자'
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chatrooms_as_seller',
        verbose_name='판매자'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='chatrooms',
        verbose_name='상품'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    def __str__(self):
        return f"ChatRoom (상품: {self.product.id}, {self.buyer.nickname} ↔ {self.seller.nickname})"


class ChatMessage(models.Model):
    chat_room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='채팅방'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages',
        verbose_name='발신자'
    )
    content = models.TextField(verbose_name='메시지 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='전송 시간')

    def __str__(self):
        return f"[{self.chat_room.id}] {self.sender.nickname}: {self.content[:20]}"
