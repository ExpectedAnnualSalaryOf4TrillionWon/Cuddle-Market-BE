from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models

from apps.categories.models import State, City


# 커스텀 User를 만들 때 필요한 매니저 클래스
class UserManager(BaseUserManager):
    # 일반 유저 생성 메서드
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")  # 이메일 필수
        email = self.normalize_email(email)  # 이메일 포맷 정규화 (대소문자 정리 등)
        user = self.model(email=email, **extra_fields)  # User 객체 생성
        user.set_password(password)  # 비밀번호 해싱 처리
        user.save(using=self._db)  # DB에 저장
        return user

    # 슈퍼유저 생성 메서드
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)  # 관리자 권한
        extra_fields.setdefault("is_superuser", True)  # 슈퍼유저 권한
        return self.create_user(email, password, **extra_fields)


# 사용자 테이블
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    provider = models.CharField(max_length=20, blank=True, null=True)
    provider_id = models.CharField(max_length=255, blank=True, null=False)
    nickname = models.CharField(max_length=8, null=False)
    name = models.CharField(max_length=30, blank=True, null=True)
    profile_image = models.URLField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    # 권한 관련 필드
    profile_completed = models.BooleanField(default=False)  # 추가 정보 입력 확인
    is_active = models.BooleanField(default=True)  # 계정 활성화 여부
    is_superuser = models.BooleanField(default=False)  # 슈퍼유저 권한 여부
    is_staff = models.BooleanField(default=False)  # 관리자 페이지 접근 권한 여부

    # 생성/수정 시간
    created_at = models.DateTimeField(auto_now_add=True)  # 가입일
    updated_at = models.DateTimeField(auto_now=True)  # 정보 수정일

    # 로그인에 사용할 필드 (USERNAME_FIELD는 email 사용)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # createsuperuser 할 때 추가로 입력받을 필드 없음

    objects = UserManager()  # 커스텀 매니저 연결

    def __str__(self):
        return self.email  # admin 페이지 등에서 이메일로 표시
