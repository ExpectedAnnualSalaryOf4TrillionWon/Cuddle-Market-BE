from django.core.management.base import BaseCommand
from apps.categories.models import State


class Command(BaseCommand):
    help = "초기 시/도(State) 데이터를 데이터베이스에 추가합니다."

    def handle(self, *args, **options):
        """
        이 명령어가 실행될 때 호출되는 메인 로직입니다.
        """
        states_data = [
            {"code": "SEOUL", "name": "서울특별시"},
            {"code": "GYEONGGIDO", "name": "경기도"},
            {"code": "INCHEON", "name": "인천광역시"},
            {"code": "BUSAN", "name": "부산광역시"},
            {"code": "GYEONGNAM", "name": "경상남도"},
            {"code": "GYEONGBUK", "name": "경상북도"},
            {"code": "DAEGU", "name": "대구광역시"},
            {"code": "CHUNGNAM", "name": "충청남도"},
            {"code": "CHUNGBUK", "name": "충청북도"},
            {"code": "JEONNAM", "name": "전라남도"},
            {"code": "JEONBUK", "name": "전북특별자치도"},
            {"code": "GANGWON", "name": "강원특별자치도"},
            {"code": "DAEJEON", "name": "대전광역시"},
            {"code": "GWANGJU", "name": "광주광역시"},
            {"code": "ULSAN", "name": "울산광역시"},
            {"code": "JEJU", "name": "제주특별자치도"},
            {"code": "SEJONG", "name": "세종특별자치시"},
        ]

        # 생성 및 업데이트 카운터 초기화
        created_count = 0
        updated_count = 0

        for state_info in states_data:
            _, created = State.objects.update_or_create(
                code=state_info["code"], defaults={"name": state_info["name"]}
            )

            # 2. 생성과 업데이트를 구분하여 카운터 증가
            if created:
                created_count += 1
            else:
                updated_count += 1

        # 3. 최종 요약 메시지를 명확하게 출력
        self.stdout.write("-" * 50)
        self.stdout.write(self.style.SUCCESS("작업 요약:"))
        self.stdout.write(f"- 시/도 데이터: {created_count}개 생성, {updated_count}개 업데이트 완료.")
