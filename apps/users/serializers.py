from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import date
from apps.categories.models import State, City

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    일반적인 사용자 정보 조회를 위한 시리얼라이저
    """

    state_name = serializers.CharField(source="state.name", read_only=True)
    city_name = serializers.CharField(source="city.name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "provider",
            "email",
            "name",
            "nickname",
            "profile_image",
            "birthday",
            "city_name",
            "state_name",
            "is_active",
            "is_staff",
            "is_superuser",
            "profile_completed",
            "last_login",
        )
        read_only_fields = fields


class SocialProfileRegistrationSerializer(serializers.ModelSerializer):
    """
    소셜 로그인 후 추가 정보 입력을 처리하는 시리얼라이저
    사용자 프로필을 완성(profile_completed=True)시킴
    """

    # 1. state 필드를 SlugRelatedField로 변경
    state = serializers.SlugRelatedField(
        queryset=State.objects.all(),  # 이 이름으로 객체를 찾을 DB 테이블
        slug_field="name",  # 'name' 필드를 기준으로 찾고, 보여줌
        allow_null=True,  # null 값을 허용
        required=False,  # 필수 입력이 아님
    )

    # 2. city 필드도 SlugRelatedField로 변경
    city = serializers.SlugRelatedField(
        queryset=City.objects.all(), slug_field="name", allow_null=True, required=False
    )

    class Meta:
        model = User
        fields = [
            "nickname",
            "name",
            "birthday",
            "state",
            "city",
        ]

    def validate_nickname(self, value):
        """닉네임 중복 검사"""
        # 현재 요청을 보낸 사용자를 제외하고 중복 검사
        if User.objects.exclude(pk=self.instance.pk).filter(nickname=value).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

    def validate_birthday(self, value):
        """
        'birthday' 필드에 대한 유효성 검사를 수행합니다.
        """
        # value는 사용자가 입력한 생년월일 값입니다.
        if value > date.today():
            raise serializers.ValidationError(
                "생년월일은 오늘 날짜보다 미래일 수 없습니다."
            )
        return value

    def update(self, instance, validated_data):
        """
        사용자 정보를 업데이트하고, 프로필 완성 상태로 변경합니다.
        """
        # validated_data에 있는 필드들만 업데이트
        instance = super().update(instance, validated_data)

        # 프로필 완성 상태로 변경
        instance.profile_completed = True

        # 변경된 필드만 업데이트
        instance.save(update_fields=["profile_completed"] + list(validated_data.keys()))

        return instance
