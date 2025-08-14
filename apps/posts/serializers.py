from rest_framework import serializers

from .models import Comment


class CommentCreateSerializer(
    serializers.ModelSerializer
):  # 댓글 생성용 Serializer 정의
    class Meta:
        model = Comment  # 사용할 모델은 Comment
        fields = ["id", "content", "post"]  # 클라이언트가 전달할 필드들
        extra_kwargs = {
            "post": {"write_only": True},  # post 필드는 요청에만 사용, 응답에는 안 나옴
        }

    def create(self, validated_data):  # 실제 저장(create) 동작 오버라이드
        user = self.context["request"].user  # 요청한 유저 정보 가져오기
        return Comment.objects.create(
            user=user, **validated_data
        )  # user 포함해서 댓글 생성


# 댓글 조회용 Serializer 정의
class CommentListSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(
        source="user.nickname", read_only=True
    )  # 작성자 닉네임 포함

    class Meta:
        model = Comment  # 사용할 모델은 Comment
        fields = [
            "id",
            "content",
            "user_nickname",
            "created_at",
        ]  # 응답에 포함될 필드들


# 댓글 수정용 Serializer 정의
class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment  # 사용할 모델은 Comment
        fields = ["content"]  # 수정 가능한 필드는 content
