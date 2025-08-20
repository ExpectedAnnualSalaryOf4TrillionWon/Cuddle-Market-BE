from django.core.management.base import BaseCommand
from apps.categories.models import State


class Command(BaseCommand):
    help = '초기 시/도(State) 데이터를 데이터베이스에 추가합니다.'

    def handle(self, *args, **options):
        """
        이 명령어가 실행될 때 호출되는 메인 로직입니다.
        """
        states_data = [
            {'code': 'SEOUL', 'name': '서울특별시'},
            {'code': 'GYEONGGIDO', 'name': '경기도'},
            {'code': 'INCHEON', 'name': '인천광역시'},
            {'code': 'BUSAN', 'name': '부산광역시'},
            {'code': 'GYEONGNAM', 'name': '경상남도'},
            {'code': 'GYEONGBUK', 'name': '경상북도'},
            {'code': 'DAEGU', 'name': '대구광역시'},
            {'code': 'CHUNGNAM', 'name': '충청남도'},
            {'code': 'CHUNGBUK', 'name': '충청북도'},
            {'code': 'JEONNAM', 'name': '전라남도'},
            {'code': 'JEONBUK', 'name': '전북특별자치도'},
            {'code': 'GANGWON', 'name': '강원특별자치도'},
            {'code': 'DAEJEON', 'name': '대전광역시'},
            {'code': 'GWANGJU', 'name': '광주광역시'},
            {'code': 'ULSAN', 'name': '울산광역시'},
            {'code': 'JEJU', 'name': '제주특별자치도'},
            {'code': 'SEJONG', 'name': '세종특별자치시'},
        ]

        created_count = 0
        for state_info in states_data:
            # get_or_create: code가 이미 존재하면 가져오고, 없으면 새로 생성합니다.
            # 이 방법을 사용하면 스크립트를 여러 번 실행해도 데이터가 중복으로 쌓이지 않습니다.
            obj, created = State.objects.get_or_create(
                code=state_info['code'],
                defaults={'name': state_info['name']}
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"'{state_info['name']}' 생성 완료"))
            else:
                self.stdout.write(f"'{state_info['name']}'은(는) 이미 존재합니다.")

        self.stdout.write(self.style.SUCCESS(f'총 {created_count}개의 시/도 데이터가 성공적으로 추가되었습니다.'))

