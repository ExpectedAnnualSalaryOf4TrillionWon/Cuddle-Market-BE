# users/serializers.py
from rest_framework import serializers
from .models import User


# User 모델 기반 회원가입용 시리얼라이저 정의
class UserSignupSerializer(serializers.ModelSerializer):  
    password = serializers.CharField(write_only=True)  # 비밀번호는 응답에 포함되지 않도록 write_only 설정

    class Meta:
        model = User  # 사용할 모델은 User
        fields = ['email', 'password', 'nickname', 'region']  # 클라이언트가 주고받을 필드 지정

    def create(self, validated_data):  # serializer.save() 시 호출되는 사용자 생성 로직
        return User.objects.create_user(  # 커스텀 매니저의 create_user 메서드로 유저 생성
            email=validated_data['email'],  # 이메일 필드 전달
            password=validated_data['password'],  # 비밀번호 전달
            nickname=validated_data['nickname'],  # 닉네임 전달
            region=validated_data.get('region', None)  # 지역은 선택적이므로 get()으로 처리
        )

# users/serializers.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['nickname'] = user.nickname
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['nickname'] = self.user.nickname
        data['email'] = self.user.email
        return data
