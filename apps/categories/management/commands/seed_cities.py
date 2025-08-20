from django.core.management.base import BaseCommand
from django.db import transaction
from apps.categories.models import State, City


class Command(BaseCommand):
    help = "대한민국 모든 시/도(State)에 대한 시/군/구(City) 데이터를 데이터베이스에 추가합니다."

    @transaction.atomic
    def handle(self, *args, **options):
        """
        이 명령어가 실행될 때 호출되는 메인 로직입니다.
        모든 데이터는 행정안전부 2024년 최신 행정구역현황을 기반으로 합니다.
        """
        # {State 코드: [소속 City 목록]} 형태의 전체 데이터
        all_cities_data = {
            "SEOUL": [
                "종로구",
                "중구",
                "용산구",
                "성동구",
                "광진구",
                "동대문구",
                "중랑구",
                "성북구",
                "강북구",
                "도봉구",
                "노원구",
                "은평구",
                "서대문구",
                "마포구",
                "양천구",
                "강서구",
                "구로구",
                "금천구",
                "영등포구",
                "동작구",
                "관악구",
                "서초구",
                "강남구",
                "송파구",
                "강동구",
            ],
            "BUSAN": [
                "중구",
                "서구",
                "동구",
                "영도구",
                "부산진구",
                "동래구",
                "남구",
                "북구",
                "해운대구",
                "사하구",
                "금정구",
                "강서구",
                "연제구",
                "수영구",
                "사상구",
                "기장군",
            ],
            "DAEGU": [
                "중구",
                "동구",
                "서구",
                "남구",
                "북구",
                "수성구",
                "달서구",
                "달성군",
                "군위군",
            ],
            "INCHEON": [
                "중구",
                "동구",
                "미추홀구",
                "연수구",
                "남동구",
                "부평구",
                "계양구",
                "서구",
                "강화군",
                "옹진군",
            ],
            "GWANGJU": ["동구", "서구", "남구", "북구", "광산구"],
            "DAEJEON": ["동구", "중구", "서구", "유성구", "대덕구"],
            "ULSAN": ["중구", "남구", "동구", "북구", "울주군"],
            # 'SEJONG': 세종특별자치시는 기초자치단체가 없으므로 제외
            "GYEONGGIDO": [
                "수원시",
                "성남시",
                "고양시",
                "용인시",
                "부천시",
                "안산시",
                "안양시",
                "남양주시",
                "화성시",
                "평택시",
                "의정부시",
                "시흥시",
                "파주시",
                "김포시",
                "광명시",
                "광주시",
                "군포시",
                "오산시",
                "이천시",
                "양주시",
                "구리시",
                "안성시",
                "포천시",
                "의왕시",
                "하남시",
                "여주시",
                "동두천시",
                "과천시",
                "가평군",
                "양평군",
                "연천군",
            ],
            "GANGWON": [
                "춘천시",
                "원주시",
                "강릉시",
                "동해시",
                "태백시",
                "속초시",
                "삼척시",
                "홍천군",
                "횡성군",
                "영월군",
                "평창군",
                "정선군",
                "철원군",
                "화천군",
                "양구군",
                "인제군",
                "고성군",
                "양양군",
            ],
            "CHUNGBUK": [
                "청주시",
                "충주시",
                "제천시",
                "보은군",
                "옥천군",
                "영동군",
                "증평군",
                "진천군",
                "괴산군",
                "음성군",
                "단양군",
            ],
            "CHUNGNAM": [
                "천안시",
                "공주시",
                "보령시",
                "아산시",
                "서산시",
                "논산시",
                "계룡시",
                "당진시",
                "금산군",
                "부여군",
                "서천군",
                "청양군",
                "홍성군",
                "예산군",
                "태안군",
            ],
            "JEONBUK": [
                "전주시",
                "익산시",
                "군산시",
                "정읍시",
                "남원시",
                "김제시",
                "완주군",
                "진안군",
                "무주군",
                "장수군",
                "임실군",
                "순창군",
                "고창군",
                "부안군",
            ],
            "JEONNAM": [
                "목포시",
                "여수시",
                "순천시",
                "나주시",
                "광양시",
                "담양군",
                "곡성군",
                "구례군",
                "고흥군",
                "보성군",
                "화순군",
                "장흥군",
                "강진군",
                "해남군",
                "영암군",
                "무안군",
                "함평군",
                "영광군",
                "장성군",
                "완도군",
                "진도군",
                "신안군",
            ],
            "GYEONGBUK": [
                "포항시",
                "경주시",
                "김천시",
                "안동시",
                "구미시",
                "영주시",
                "영천시",
                "상주시",
                "문경시",
                "경산시",
                "의성군",
                "청송군",
                "영양군",
                "영덕군",
                "청도군",
                "고령군",
                "성주군",
                "칠곡군",
                "예천군",
                "봉화군",
                "울진군",
                "울릉군",
            ],
            "GYEONGNAM": [
                "창원시",
                "진주시",
                "통영시",
                "사천시",
                "김해시",
                "밀양시",
                "거제시",
                "양산시",
                "의령군",
                "함안군",
                "창녕군",
                "고성군",
                "남해군",
                "하동군",
                "산청군",
                "함양군",
                "거창군",
                "합천군",
            ],
            "JEJU": ["제주시", "서귀포시"],
        }

        total_created_count = 0
        total_skipped_count = 0

        # items()를 사용하여 State 코드와 City 이름 리스트를 순회합니다.
        for state_code, city_names in all_cities_data.items():
            try:
                # 1. City 데이터의 부모가 될 State 객체를 먼저 찾습니다.
                state_obj = State.objects.get(code=state_code)
            except State.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(
                        f"State '{state_code}'을(를) 찾을 수 없습니다. 이 시/도의 City 데이터는 건너뜁니다."
                    )
                )
                total_skipped_count += len(city_names)
                continue  # 다음 State로 넘어갑니다.

            state_created_count = 0
            # 2. 해당 State에 속한 City들을 하나씩 생성합니다.
            for index, city_name in enumerate(city_names, 1):
                # City 코드를 'STATE코드-순번' 형태로 생성합니다. (예: SEOUL-01, SEOUL-02)
                city_code = f"{state_code}-{index:02}"  # 01, 02, ... 형태로 포맷팅, 최소 2자리 너비, 너비가 부족하면 남는 공간은 0으로

                obj, created = City.objects.get_or_create(
                    code=city_code,
                    defaults={
                        "name": city_name,
                        "state": state_obj,  # ForeignKey 관계 설정
                    },
                )

                if created:
                    state_created_count += 1

            if state_created_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"'{state_obj.name}'에 {state_created_count}개의 시/군/구 데이터를 성공적으로 추가했습니다."
                    )
                )

            total_created_count += state_created_count

        self.stdout.write("-" * 50)
        if total_created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"총 {total_created_count}개의 새로운 시/군/구 데이터가 추가되었습니다."
                )
            )
        if total_skipped_count > 0:
            self.stdout.write(
                self.style.WARNING(
                    f"총 {total_skipped_count}개의 시/군/구 데이터는 부모 시/도를 찾지 못해 건너뛰었습니다."
                )
            )

        self.stdout.write(self.style.SUCCESS("모든 작업이 완료되었습니다."))
