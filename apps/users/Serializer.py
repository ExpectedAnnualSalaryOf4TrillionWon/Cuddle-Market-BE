# users/serializers.py
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


# User 모델 기반 회원가입용 시리얼라이저 정의
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )  # 비밀번호는 응답에 포함되지 않도록 write_only 설정

    class Meta:
        model = User  # 사용할 모델은 User
        fields = [
            "email",
            "password",
            "nickname",
            "region",
        ]  # 클라이언트가 주고받을 필드 지정

    def create(self, validated_data):  # serializer.save() 시 호출되는 사용자 생성 로직
        return (
            User.objects.create_user(  # 커스텀 매니저의 create_user 메서드로 유저 생성
                email=validated_data["email"],  # 이메일 필드 전달
                password=validated_data["password"],  # 비밀번호 전달
                nickname=validated_data["nickname"],  # 닉네임 전달
                region=validated_data.get(
                    "region", None
                ),  # 지역은 선택적이므로 get()으로 처리
            )
        )


# users/serializers.py


class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["nickname"] = user.nickname
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["nickname"] = self.user.nickname
        data["email"] = self.user.email
        return data


# 회원 탈퇴용 시리얼라이저 (is_active만 False로 처리)
class UserWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []  # 클라이언트로부터 받을 값은 없음

    def update(self, instance, validated_data):
        # 사용자 탈퇴 처리 (실제 삭제가 아니라 비활성화)
        instance.is_active = False
        instance.save()
        return instance


# 유저 프로필 조회 시리얼 라이져
class MyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "nickname", "profile_img", "region", "created_at"]


# 프로필 수정 시리얼 라이져
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nickname", "profile_img", "region"]  # 수정 가능한 항목만 ㅎ


# 공개용 유저 프로필 조회 시리얼라이저
class PublicUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "nickname", "profile_img", "region"]
