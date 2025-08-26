from rest_framework import serializers
from .models import ChatRoom, ChatMessage
from apps.products.models import ProductImage, Product
from apps.users.models import User  # 채팅방 유저 이름 가져오려구import


class ChatRoomListSerializer(serializers.ModelSerializer):
    partner_nickname = serializers.SerializerMethodField()  # 상대방 닉네임
    product_image = serializers.SerializerMethodField()  # 상품 대표 이미지
    last_message = serializers.SerializerMethodField()  # 마지막 메시지 내용
    last_message_time = serializers.SerializerMethodField()  # 마지막 메시지 시간
    product_title = serializers.CharField(
        source="product.title", read_only=True
    )  # 상품명
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )  # 가격

    class Meta:
        model = ChatRoom
        fields = [
            "partner_nickname",
            "product_image",
            "product_title",
            "product_price",
            "last_message",
            "last_message_time",
        ]

    # 상대방 닉네임 계산
    def get_partner_nickname(self, obj):
        user = self.context["request"].user
        return obj.seller.nickname if obj.buyer == user else obj.buyer.nickname

    # 상품 대표 이미지 (ProductImage 중 is_main=True)
    def get_product_image(self, obj):
        main_image = ProductImage.objects.filter(
            product=obj.product, is_main=True
        ).first()
        return main_image.url if main_image else None

    # 최근 메시지 내용
    def get_last_message(self, obj):
        last_msg = obj.messages.order_by("-created_at").first()
        return last_msg.message if last_msg else None

    # 최근 메시지 시간
    def get_last_message_time(self, obj):
        last_msg = obj.messages.order_by("-created_at").first()
        return last_msg.created_at if last_msg else None


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    buyer_id = serializers.IntegerField(write_only=True)
    seller_id = serializers.IntegerField(write_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ChatRoom
        fields = ["buyer_id", "seller_id", "product_id"]

    def create(self, validated_data):
        buyer = User.objects.get(id=validated_data["buyer_id"])
        seller = User.objects.get(id=validated_data["seller_id"])
        product = Product.objects.get(id=validated_data["product_id"])

        chatroom, created = ChatRoom.objects.get_or_create(
            buyer=buyer, seller=seller, product=product
        )
        return chatroom


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(write_only=True)

    class Meta:
        model = ChatMessage
        fields = ["content"]

    def create(self, validated_data):
        request = self.context["request"]
        chatroom_id = self.context["chatroom_id"]
        chat_room = ChatRoom.objects.get(id=chatroom_id)
        sender = request.user

        return ChatMessage.objects.create(
            chat_room=chat_room,
            sender=sender,
            message=validated_data["content"],
        )


class ChatMessageListSerializer(serializers.ModelSerializer):
    sender_nickname = serializers.CharField(source="sender.nickname", read_only=True)

    class Meta:
        model = ChatMessage
        fields = ["sender_nickname", "message"]
