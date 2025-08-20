# users/management/commands/seed_pets.py

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.categories.models import PetType, PetTypeDetail


class Command(BaseCommand):
    help = "올바른 설계 원칙에 따라 반려동물 종류 및 상세 종류 데이터를 추가합니다."

    @transaction.atomic
    def handle(self, *args, **options):
        """
        PetType과 PetTypeDetail의 code가 각각 독립적인 고유 값을 갖도록 데이터를 생성합니다.
        데이터가 이미 존재하면 건너뜁니다.
        """
        # {PetType 이름: {'code': PetType 코드, 'details': {PetTypeDetail 이름: PetTypeDetail 코드}}}
        # 각 code는 부모-자식 관계없이 그 자체로 고유합니다.
        all_pets_data = {
            "포유류": {
                "code": "MAMMAL",
                "details": {
                    "강아지": "DOG",
                    "고양이": "CAT",
                    "토끼": "RABBIT",
                    "햄스터": "HAMSTER",
                    "기니피그": "GUINEA_PIG",
                    "페럿": "FERRET",
                    "친칠라": "CHINCHILLA",
                    "고슴도치": "HEDGEHOG",
                },
            },
            "조류": {
                "code": "BIRD",
                "details": {
                    "잉꼬": "BUDGERIGAR",
                    "앵무새": "PARROT",
                    "카나리아": "CANARY",
                    "모란앵무": "LOVEBIRD",
                },
            },
            "파충류": {
                "code": "REPTILE",
                "details": {
                    "도마뱀": "LIZARD",
                    "뱀": "SNAKE",
                    "거북이": "TURTLE",
                    "게코": "GECKO",
                },
            },
            "수생동물": {
                "code": "AQUATIC",
                "details": {
                    "금붕어": "GOLDFISH",
                    "열대어": "TROPICAL_FISH",
                    "체리새우": "CHERRY_SHRIMP",
                    "달팽이": "SNAIL",
                },
            },
            "곤충/절지동물": {
                "code": "INSECT_ARTHROPOD",
                "details": {
                    "귀뚜라미": "CRICKET",
                    "사마귀": "MANTIS",
                    "딱정벌레": "BEETLE",
                    "거미": "SPIDER",
                },
            },
        }

        total_types_created = 0
        total_details_created = 0

        # PetType과 PetTypeDetail 데이터를 생성합니다.
        for type_name, type_data in all_pets_data.items():
            type_code = type_data["code"]

            # 1. PetType 객체를 생성하거나 가져옵니다.
            pet_type_obj, created = PetType.objects.get_or_create(
                code=type_code, defaults={"name": type_name}
            )
            if created:
                total_types_created += 1
                self.stdout.write(
                    self.style.SUCCESS(f"PetType '{type_name}' 생성 완료")
                )

            # 2. 해당 PetType에 속한 PetTypeDetail 객체들을 생성합니다.
            for detail_name, detail_code in type_data["details"].items():
                # get_or_create를 사용하여 PetTypeDetail 데이터를 추가합니다.
                # code는 부모 정보 없이, 독립적이고 고유한 값을 사용합니다.
                _, detail_created = PetTypeDetail.objects.get_or_create(
                    code=detail_code,
                    defaults={
                        "name": detail_name,
                        "pet_type": pet_type_obj,  # ForeignKey 관계로 부모를 지정
                    },
                )
                if detail_created:
                    total_details_created += 1

        self.stdout.write("-" * 50)
        if total_types_created > 0 or total_details_created > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"총 {total_types_created}개의 PetType과 {total_details_created}개의 PetTypeDetail 데이터가 추가되었습니다."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("모든 반려동물 데이터가 이미 존재합니다.")
            )
