from django.db import models

class TimeStampedModel(models.Model):
    """생성일, 수정일 자동 저장"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True   # 상속 전용, DB 테이블은 안생김


class BaseModel(TimeStampedModel):
    """공통적으로 물려줄 기본 모델"""
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
