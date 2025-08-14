from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    # 일반 사용자 생성 메서드
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일은 필수 항목입니다.")
        email = self.normalize_email(email)  # 이메일 정규화
        user = self.model(email=email, **extra_fields)  # 유저 인스턴스 생성
        user.set_password(password)  # 비밀번호 해싱 처리
        user.save(using=self._db)  # DB에 저장
        return user

    # 관리자(superuser) 생성 메서드
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)  # 관리자 권한 부여
        extra_fields.setdefault("is_superuser", True)  # 슈퍼유저 권한 부여
        return self.create_user(email, password, **extra_fields)


#  커스텀 User 모델 정의
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # 로그인 ID로 사용할 이메일
    password = models.CharField(max_length=128)  # 비밀번호 (set_password로 해싱됨)
    nickname = models.CharField(max_length=20)  # 닉네임
    profile_img = models.URLField(blank=True, null=True)  # 프로필 이미지
    region = models.CharField(max_length=50, blank=True, null=True)  # 지역

    is_active = models.BooleanField(default=True)  # 탈퇴 여부 (soft delete 용)
    is_staff = models.BooleanField(default=False)  # 관리자 페이지 접속 권한

    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일

    # 커스텀 매니저 연결
    objects = UserManager()

    # 로그인 시 사용할 필드 설정
    USERNAME_FIELD = "email"  # 기본 유저 모델의 username 대신 email 사용
    REQUIRED_FIELDS = ["nickname"]  # createsuperuser 시 추가로 입력받을 필드

    def __str__(self):
        return self.email  # User 인스턴스를 문자열로 표현할 때 이메일 반환
