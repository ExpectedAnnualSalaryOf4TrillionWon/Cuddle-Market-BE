from django.db import models

class Category(models.Model):
    id = models.AutoField(primary_key=True)  # 고유 ID (자동 증가)
    code = models.CharField(max_length=50, unique=True, null=False)  # 카테고리 코드 (예: "CAT001")
    name = models.CharField(max_length=100, null=False)  # 카테고리 이름 (예: 간식/사료, 장난감)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일 (자동 기록)
    updated_at = models.DateTimeField(auto_now=True)  # 수정일 (자동 기록)

    class Meta:
        db_table = "category"  # DB 테이블명 지정

    def __str__(self):
        return f"{self.name} ({self.code})"

