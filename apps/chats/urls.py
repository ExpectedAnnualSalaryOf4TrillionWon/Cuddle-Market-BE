from django.urls import path
from .views import (
    ChatRoomListCreateView,
    ChatMessageView,
    ChatRoomDeleteView,
    
)

urlpatterns = [
    path("chatrooms/", ChatRoomListCreateView.as_view(), name="chatroom-list-create"),  # 채팅방 생성 및 목록 조회       
    path("chatrooms/<int:chatroom_id>/", ChatRoomDeleteView.as_view(), name="chatroom-delete"),  #채팅방삭제
    path("chatrooms/<int:chatroom_id>/messages/", ChatMessageView.as_view(), name="chatmessage"), #채팅 내역조회
]
