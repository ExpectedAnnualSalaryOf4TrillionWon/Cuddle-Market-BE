<img width="1960" height="980" alt="image" src="https://github.com/user-attachments/assets/b847a58c-af7c-4b1c-b5e1-fe3ffe875750" />
<br>
# 프로젝트 소개
<br>
- Cuddle Market
반려동물들과 함께하는 사람이 많은 요즘, 반려동물 용품을 새로 구매하는 것이 가격이 비싸 부담스럽기도 하고, 수명이 짧게 사용되고 흥미를 잃거나 선호도에 따라 버려지는 것이 아까운 모든 반려인들을 위해 Cuddle Maket이 개발되었습니다.
내 아이를 위한 소중한 마음과 추억이 또 다른 사랑으로 나누어지는 Cuddle Maket입니다.

📌 주요 기능 (요약 버전)

회원 관리: 이메일 회원가입/로그인, 카카오 소셜 로그인, 마이페이지, 회원 탈퇴

상품 관리: 상품 등록/수정/삭제, 다중 이미지 업로드(S3), 거래 상태 변경

검색 & 필터: 통합 검색, 카테고리/반려동물 타입 필터, 최신순·인기순 정렬

관심 상품(찜): 상품 찜 등록/취소, 찜 개수 조회, 내 관심목록 관리

실시간 채팅: 구매자–판매자 1:1 채팅, 채팅방 생성/삭제, 메시지 송수신(WebSocket)

# 기술스택
Django, DRF, WebSocket, Postman, RDS, EC2, S3, python, Postgresql, Redis, Docker, Daphne, GitHub, Swager

## Team

<table align="center">
<thead>
<tr>
<th align="center"><a href="https://github.com/Dayeon-00"><img src="https://img.shields.io/badge/github-Dayeon-blue?style=for-the-badge&logo=github&logoColor=%23fff&labelColor=%23181717" width="100px/" style="max-width: 100%;"></a><br></th>
<th align="center"><a href="https://github.com/jjub0217"><img src="https://img.shields.io/badge/github-jjub0217-blue?style=for-the-badge&logo=github&logoColor=%23fff&labelColor=%23181717" width="100px/" style="max-width: 100%;"></a><br></th>
<th align="center"><a href="https://github.com/minjekim64"><img src="https://img.shields.io/badge/github-minjekim64-blue?style=for-the-badge&logo=github&logoColor=%23fff&labelColor=%23181717" width="100px/" style="max-width: 100%;"></a><br></th>
</tr>
</thead>
<tbody>
<tr>
<td align="center">총 팀장<br>(BackEnd 팀장)</td> 
<td align="center">부 팀장<br>(FrontEnd 팀장)</td>
<td align="center">팀원<br>(FrontEnd)</td>

</tr>
<tr>
<td align="center">권다연</td>
<td align="center">강주현</td>
<td align="center">김민제</td>

</tr>
</tbody>
</table>
<table align="center">
<thead>
<tr>
<th align="center"><a href="https://github.com/dirage1"><img src="https://img.shields.io/badge/github-dirage1-blue?style=for-the-badge&logo=github&logoColor=%23fff&labelColor=%23181717" width="100px/" style="max-width: 100%;"></a><br></th>
<th align="center"><a href="https://github.com/ParkKangbin"><img src="https://img.shields.io/badge/github-ParkKangbin-blue?style=for-the-badge&logo=github&logoColor=%23fff&labelColor=%23181717" width="100px/" style="max-width: 100%;"></a><br></th>
<th align="center"><a href="https://github.com/ark2313"><img src="https://img.shields.io/badge/github-ark2313-blue?style=for-the-badge&logo=github&logoColor=%23fff&labelColor=%23181717" width="100px/" style="max-width: 100%;"></a><br></th>

</tr>
</thead>
<tbody>
<tr>
<td align="center">팀원<br>(FrontEnd)</td>
<td align="center">팀원<br>(BackEnd)</td>
<td align="center">팀원<br>(BackEnd)</td>
</tr>
<tr>
<td align="center">김승원</td>
<td align="center">박강빈</td>
<td align="center">이상민</td>
</tr>
</tbody>
</table>
<br>
# 프로젝트 구조

```bash
CUDDLE-MARKET-BE/
├── .github/                 # GitHub 설정
├── .idea/                   # IDE 관련 설정 (PyCharm 등)
├── .ruff_cache/             # Ruff linter 캐시
├── .venv/                   # 가상환경
├── apps/                    # Django 앱 모음
│   ├── categories/          # 카테고리 관련 앱
│   ├── chats/               # 채팅 기능 앱
│   ├── likes/               # 좋아요(찜) 기능 앱
│   ├── products/            # 상품 관련 앱
│   ├── users/               # 사용자 관리 앱
│   ├── __pycache__/         
│   ├── __init__.py
│   └── s3_utils.py          # S3 업로드 유틸
├── certbot/                 # 인증서 관련 설정
├── config/                  # Django 프로젝트 설정
│   ├── settings/            # 환경별 세팅 (dev, prod 등)
│   │   └── __init__.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── resources/               # 프로젝트 리소스
├── staticfiles/             # 정적 파일
├── .dockerignore
├── .env                     # 환경 변수 파일
├── .gitignore
├── .python-version          # Python 버전 관리
├── docker-compose-dev.yml   # 개발 환경 Docker Compose
├── docker-compose.yml       # 기본 Docker Compose
├── Dockerfile               # Docker 이미지 빌드 설정
├── manage.py                # Django 명령어 실행 진입점
├── pyproject.toml           # Python 패키지 설정 (uv/poetry)
├── README.md
├── test.sh                  # 테스트 실행용 스크립트
└── uv.lock                  # uv 의존성 lock 파일
```
<br>
Document
<br>
<a href="https://www.notion.so/23fcaf5650aa812d887ccbf811a4208c?v=23fcaf5650aa810995e7000c7a32a853&source=copy_link">요구사항 정의서</a><br> > <a href="">플로우 차트</a><br> > <a href="">와이어프레임</a><br> > <a href="">화면정의서</a><br> > <a href="https://dbdiagram.io/d/Copy-of-Copy-of-%EC%95%A0%EC%99%84%EB%8F%99%EB%AC%BC-%EC%A4%91%EA%B3%A0%EB%A7%88%EC%BC%93-ERD-689c9a3b1d75ee360a6f743a">ERD 문서</a><br> > <a href="https://docs.google.com/spreadsheets/d/12iKca5DBOynjGHntoxBUpVeOxhgDCU8V7FaVWBBDrTw/edit?gid=0#gid=0">테이블 명세서 문서</a><br> > <a href="">API 문서</a><br>
<br>
