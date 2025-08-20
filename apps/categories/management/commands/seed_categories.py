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

        created_count = 0

        self.stdout.write("카테고리 데이터 생성을 시작합니다...")

        for category_info in category_options:
            # get_or_create: code가 이미 존재하면 가져오고, 없으면 새로 생성합니다.
            _, created = Category.objects.get_or_create(
                code=category_info["code"], defaults={"name": category_info["name"]}
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"  - 카테고리 '{category_info['name']}' 생성 완료"
                    )
                )

        self.stdout.write("-" * 50)
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"총 {created_count}개의 새로운 카테고리가 성공적으로 추가되었습니다."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("모든 카테고리 데이터가 이미 존재합니다.")
            )
