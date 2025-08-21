# categories/management/commands/seed_categories.py

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.categories.models import (
    Category,
)  # Category 모델의 실제 경로에 맞게 수정하세요.


class Command(BaseCommand):
    help = "초기 상품 카테고리(Category) 데이터를 데이터베이스에 추가합니다."

    @transaction.atomic
    def handle(self, *args, **options):
        """
        이 명령어가 실행될 때 호출되는 메인 로직입니다.
        데이터가 이미 존재하면 건너뜁니다.
        """

        # code 값을 모두 대문자로 변경한 데이터 리스트
        category_options = [
            {"code": "FOOD", "name": "사료/간식"},
            {"code": "TOYS", "name": "장난감"},
            {"code": "HOUSING", "name": "사육장/하우스"},
            {"code": "HEALTH", "name": "건강/위생"},
            {"code": "ACCESSORIES", "name": "의류/악세사리"},
            {"code": "EQUIPMENT", "name": "사육장비"},
            {"code": "CARRIER", "name": "이동장/목줄"},
            {"code": "CLEANING", "name": "청소용품"},
            {"code": "TRAINING", "name": "훈련용품"},
            {"code": "ETC", "name": "기타"},
        ]

        # 생성 및 업데이트 카운터 초기화
        created_count = 0
        updated_count = 0

        for category_info in category_options:
            # get_or_create 대신 update_or_create 사용
            _, created = Category.objects.update_or_create(
                code=category_info["code"], defaults={"name": category_info["name"]}
            )

            # 생성과 업데이트를 구분하여 카운터 증가
            if created:
                created_count += 1
            else:
                updated_count += 1

        # 최종 요약 메시지를 명확하게 출력
        self.stdout.write("-" * 50)
        self.stdout.write(self.style.SUCCESS("작업 요약:"))
        self.stdout.write(f"- 카테고리: {created_count}개 생성, {updated_count}개 업데이트 완료.")