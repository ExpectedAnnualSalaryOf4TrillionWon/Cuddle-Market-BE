import os

from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import date
from apps.categories.models import State, City
from apps.s3_utils import upload_to_s3_and_get_url

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
            "created_at",
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
            "state_name",
            "city_name",
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


class UpdateMyPageSerializer(serializers.ModelSerializer):
    """
    마이페이지 정보 조회 및 수정을 위한 Serializer
    - profile_image 필드에 이미지 파일 또는 URL을 다룸
    """

    # 수정(업로드) 시에는 파일을 받기 위해 ImageField로 오버라이드.
    # required=False로 설정하여 이미지를 변경하지 않는 경우에도 유효성 검사를 통과하도록 함.
    profile_image = serializers.ImageField(required=False, allow_null=True)
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), allow_null=True, required=False
    )
    state = serializers.PrimaryKeyRelatedField(
        queryset=State.objects.all(), allow_null=True, required=False
    )

    class Meta:
        model = User
        fields = [
            "nickname",
            "city",
            "state",
            "profile_image",
        ]
        extra_kwargs = {
            "profile_image": {
                "error_messages": {"invalid": "유효한 이미지 파일을 선택해주세요."}
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["profile_image"] = instance.profile_image
        return representation

    def update(self, instance, validated_data):
        profile_image_file = validated_data.get("profile_image", None)

        if profile_image_file:
            # --- 파일명 조합 로직 시작 ---

            # 1. 짧은 UUID 생성 (앞 8자리)
            import uuid

            short_uuid = str(uuid.uuid4())[:8]

            # 2. 원본 파일 이름에서 공백 등 처리
            original_filename = profile_image_file.name.replace(" ", "_")

            # 3. "short_uuid-원본파일이름" 형태로 새 파일명 조합
            new_filename = f"{short_uuid}-{original_filename}"

            # 4. 최종 S3 객체 키(경로 포함) 생성
            object_name = f"profiles/{instance.id}/{new_filename}"

            # --- 파일명 조합 로직 끝 ---

            bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
            s3_url = upload_to_s3_and_get_url(
                profile_image_file, bucket_name, object_name
            )

            if s3_url:
                validated_data["profile_image"] = s3_url
            else:
                raise serializers.ValidationError(
                    {"profile_image": "이미지 업로드에 실패했습니다."}
                )
        else:
            validated_data.pop("profile_image", None)

        return super().update(instance, validated_data)


class DevLoginSerializer(serializers.Serializer[None]):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
