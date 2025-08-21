from django.core.management.base import BaseCommand
from django.db import transaction
from apps.categories.models import PetType, PetTypeDetail


class Command(BaseCommand):
    help = "반려동물 종류 및 상세 종류 데이터를 생성하거나 업데이트합니다."

    @transaction.atomic
    def handle(self, *args, **options):
        """
        데이터가 이미 존재하면 업데이트하고, 없으면 새로 생성합니다.
        """
        self.stdout.write(self.style.SUCCESS("반려동물 데이터 시딩/업데이트를 시작합니다..."))

        all_pets_data = {
            "포유류": {
                "code": "MAMMAL",
                "details": {
                    "강아지": "DOG", "고양이": "CAT", "토끼": "RABBIT", "햄스터": "HAMSTER",
                    "기니피그": "GUINEA_PIG", "페럿": "FERRET", "친칠라": "CHINCHILLA", "고슴도치": "HEDGEHOG",
                },
            },
            "조류": {
                "code": "BIRD",
                "details": {
                    "잉꼬": "BUDGERIGAR", "앵무새": "PARROT", "카나리아": "CANARY", "모란앵무": "LOVEBIRD",
                },
            },
            "파충류": {
                "code": "REPTILE",
                "details": {
                    "도마뱀": "LIZARD", "뱀": "SNAKE", "거북이": "TURTLE", "게코": "GECKO",
                },
            },
            "수생동물": {
                "code": "AQUATIC",
                "details": {
                    "금붕어": "GOLDFISH", "열대어": "TROPICAL_FISH", "체리새우": "CHERRY_SHRIMP", "달팽이": "SNAIL",
                },
            },
            "곤충/절지동물": {
                "code": "INSECT_ARTHROPOD",
                "details": {
                    "귀뚜라미": "CRICKET", "사마귀": "MANTIS", "딱정벌레": "BEETLE", "거미": "SPIDER",
                },
            },
        }

        # 생성 및 업데이트 카운터 초기화
        types_created, types_updated = 0, 0
        details_created, details_updated = 0, 0

        for type_name, type_data in all_pets_data.items():
            type_code = type_data["code"]

            # 1. PetType 생성 또는 업데이트
            pet_type_obj, created = PetType.objects.update_or_create(
                code=type_code, defaults={"name": type_name}
            )
            if created:
                types_created += 1
            else:
                types_updated += 1

            # 2. 해당 PetType에 속한 PetTypeDetail 생성 또는 업데이트
            for detail_name, detail_code in type_data["details"].items():
                _, detail_created = PetTypeDetail.objects.update_or_create(
                    code=detail_code,
                    defaults={
                        "name": detail_name,
                        "pet_type": pet_type_obj,
                    },
                )
                if detail_created:
                    details_created += 1
                else:
                    details_updated += 1

        # 최종 결과 요약 출력
        self.stdout.write("-" * 50)
        self.stdout.write(self.style.SUCCESS("작업 요약:"))
        self.stdout.write(f"- PetType:     {types_created}개 생성, {types_updated}개 업데이트 완료.")
        self.stdout.write(f"- PetTypeDetail: {details_created}개 생성, {details_updated}개 업데이트 완료.")
