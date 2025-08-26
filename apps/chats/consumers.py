import json
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.chats.models import ChatMessage, ChatRoom
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    # 1) 웹소켓 연결 시 실행
    async def connect(self):
        self.chatroom_id = self.scope["url_route"]["kwargs"]["chatroom_id"]
        self.room_group_name = f"chat_{self.chatroom_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    # 2) 연결 해제 시 실행
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # 3) 클라이언트 → 서버 메시지 수신
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get("message")
            if not message:
                await self.send(
                    text_data=json.dumps(
                        {"error": "메시지가 비어있습니다."}, ensure_ascii=False
                    )
                )
                return

            user = self.scope["user"]

            # 혹시 토큰이 잘못됐거나 만료됐다면 AnonymousUser 들어올 수도 있음
            if user.is_anonymous:
                await self.send(
                    text_data=json.dumps(
                        {"error": "인증되지 않은 사용자입니다."}, ensure_ascii=False
                    )
                )
                await self.close()
                return

            saved = await self.save_message(self.chatroom_id, user, message)
            if not saved:
                await self.send(
                    text_data=json.dumps(
                        {"error": "존재하지 않는 채팅방입니다."}, ensure_ascii=False
                    )
                )
                await self.close()
                return

            # 같은 방의 모든 클라이언트에게 메시지 브로드캐스트
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "user": user.nickname,  # ✅ 닉네임 직접 내려줌
                },
            )
        except Exception as e:
            print("Receive Error:", e)
            await self.send(text_data=json.dumps({"error": str(e)}, ensure_ascii=False))
            await self.close()

    # 4) group_send 호출 시 실행됨
    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "user": event["user"],
                    "message": event["message"],
                },
                ensure_ascii=False,
            )
        )

    # 5) DB 저장 (sync → async 변환)
    @database_sync_to_async
    def save_message(self, chatroom_id, user, message):
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)
            return ChatMessage.objects.create(
                chat_room=chatroom, sender=user, message=message
            )
        except ChatRoom.DoesNotExist:
            return None
