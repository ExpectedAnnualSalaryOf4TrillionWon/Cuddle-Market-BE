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

# 반려동물 종류 테이블 (예: 포유류, 조류 등)
class PetType(models.Model):
    code = models.CharField(max_length=50, unique=True, null=False)  # 고유 코드 (예: "MAMMAL01")
    name = models.CharField(max_length=100, null=False)  # 종류명 (예: 포유류)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일 (자동 기록)
    updated_at = models.DateTimeField(auto_now=True)      # 수정일 (자동 기록)

    def __str__(self):
        return self.name   # admin 등에서 표시될 때 이름 반환
    

# 반려동물 상세 종류 테이블 (예: 강아지, 고양이 등)
class PetTypeDetail(models.Model):
    pet_type = models.ForeignKey(PetType, on_delete=models.CASCADE, related_name="details")  
    # → PetType과 1:N 관계 (예: 포유류 → 강아지/고양이)
    code = models.CharField(max_length=50, unique=True, null=False)  # 상세 코드 (예: "DOG01")
    name = models.CharField(max_length=100, null=False)  # 상세명 (예: 강아지)
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일
    updated_at = models.DateTimeField(auto_now=True)      # 수정일

    def __str__(self):
        return f"{self.pet_type.name} - {self.name}"  # 예: "포유류 - 강아지"
