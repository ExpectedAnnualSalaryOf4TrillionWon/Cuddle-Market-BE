from django.db import models  
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import ChatRoom
from .serializers import ChatRoomListSerializer,ChatRoomCreateSerializer,ChatMessageCreateSerializer,ChatMessageListSerializer
from rest_framework.exceptions import PermissionDenied
from django.core.paginator import Paginator
class ChatRoomListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    # 채팅방 목록 조회
    def get(self, request):
        user = request.user
        # 내가 buyer거나 seller인 채팅방만 필터링
        chatrooms = ChatRoom.objects.filter(
            models.Q(buyer=user) | models.Q(seller=user)
        ).order_by("-created_at")

        serializer = ChatRoomListSerializer(
            chatrooms, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 채팅방 생성
    def post(self, request):
        serializer = ChatRoomCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        chatroom = serializer.save()

        return Response(
            {
                "chatroom_id": chatroom.id,
                "message": "채팅방이 생성되었습니다."
            },
            status=status.HTTP_201_CREATED
        )
    

class ChatRoomDeleteView(APIView): # 채팅방 삭제 기능 
    permission_classes = [IsAuthenticated]

    def delete(self, request, chatroom_id):
        user = request.user
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)
        except ChatRoom.DoesNotExist:
            return Response({"message": "존재하지 않는 채팅방입니다."}, status=status.HTTP_404_NOT_FOUND)

        if chatroom.buyer != user and chatroom.seller != user:
            raise PermissionDenied("삭제 권한이 없습니다.")

        chatroom.delete()
        return Response({"message": "채팅방이 삭제되었습니다."}, status=status.HTTP_200_OK)
    

class ChatMessageView(APIView):# 메시지 내역 조회랑/메시지 전송 같이 만듬
    permission_classes = [IsAuthenticated]

    # 메시지 목록 조회 (GET)
    def get(self, request, chatroom_id):
        user = request.user
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)
        except ChatRoom.DoesNotExist:
            return Response(
                {"message": "존재하지 않는 채팅방입니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 권한 체크 (buyer나 seller만 조회 가능)
        if chatroom.buyer != user and chatroom.seller != user:
            raise PermissionDenied("조회 권한이 없습니다.")

        messages = chatroom.messages.order_by("created_at")
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 50))
        paginator = Paginator(messages, page_size)
        current_page = paginator.get_page(page)

        serializer = ChatMessageListSerializer(current_page, many=True)
        return Response({"messages": serializer.data}, status=status.HTTP_200_OK)

    # 메시지 전송 (POST)
    def post(self, request, chatroom_id):
        serializer = ChatMessageCreateSerializer(
            data=request.data,
            context={"request": request, "chatroom_id": chatroom_id},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "메시지 전송 완료"}, status=status.HTTP_201_CREATED
        )