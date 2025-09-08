<img width="1960" height="980" alt="image" src="https://github.com/user-attachments/assets/b847a58c-af7c-4b1c-b5e1-fe3ffe875750" />
<br>

📋 목차

1. 프로젝트 소개

2. 배포 링크

3. 기능 요약

4. 파이널 웹뷰

5. 기술 스택 소개

6. 팀 소개

7. 팀 컴벤션

8. ERD

9. 프로젝트 구조

10. Document

# 프로젝트 소개

<div> 
<img  alt="Image" src="https://github.com/user-attachments/assets/6ea2172e-9a39-454d-8e13-461cc12dc075" /> </div>
<br/>
<!-- CUDDLE MARKET는 반려동물을 사랑하는 사람들을 위한 반려동물 중고용품 웹 플랫폼입니다.<br/>
더 이상 사용하지 않는 반려동물 용품을 쉽게 사고팔 수 있고, 다른 반려인들과 따뜻한 커뮤니티를 형성할 수 있습니다.
- 🐾 반려동물 용품의 합리적인 재사용
- 🐾 사용자 친화적인 간단한 UI/UX
- 🐾 따뜻한 감성을 담은 브랜드 아이덴티티 -->

**"더 이상 반려동물 용품은 한 번 쓰고 버리는 물건이 아닙니다."**

아이처럼 빠르게 성장하는 우리 반려동물들. <br/>
금세 작아진 옷, 흥미를 잃은 장난감, 한두 번 쓴 캐리어... <br/>
집 한구석에 쌓여가는 용품들을 보며 아까운 마음이 드셨나요? <br/>

**CUDDLE MARKET**은 반려동물을 사랑하는 모든 가족들이 모여
따뜻한 마음을 나누는 동네 시장입니다.

반려동물이 사용했던 소중한 물건이 또 다른 새로운 기쁨이 되는 곳,
서로의 경험을 나누며 함께 성장하는 커뮤니티,

**CUDDLE MARKET에 오신 것을 환영합니다!**

# 배포링크

<a href="https://cuddle-market-fe.vercel.app/">👉 cuddle market 바로가기</a>

# 📌 주요 기능 (요약 버전)

회원 관리: 이메일 회원가입/로그인, 카카오 소셜 로그인, 마이페이지, 회원 탈퇴

상품 관리: 상품 등록/수정/삭제, 다중 이미지 업로드(S3), 거래 상태 변경

검색 & 필터: 통합 검색, 카테고리/반려동물 타입 필터, 최신순·인기순 정렬

관심 상품(찜): 상품 찜 등록/취소, 찜 개수 조회, 내 관심목록 관리

실시간 채팅: 구매자–판매자 1:1 채팅, 채팅방 생성/삭제, 메시지 송수신(WebSocket)

## Final Web View

<table>
<thead>
<tr>
<th align="center">메인 화면</th>
<th align="center">소셜 로그인</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/메인화면.gif"><img src="./gif/메인화면.gif" alt="MainPage" style="width: 400px;"></a></td>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/소셜 로그인.gif"><img src="./gif/소셜 로그인.gif" alt="Login" style="width: 400px;"></a></td>
</tr>
</tbody>
</table>
<table>
<thead>
<tr>
<th align="center">마이 페이지</th>
<th align="center">프로필 수정</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/마이페이지.gif"><img src="./gif/마이페이지.gif" alt="MyPage" style="width: 400px;"></a></td>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/프로필 수정.gif"><img src="./gif/프로필 수정.gif" alt="ProfileUpdate" style="width: 400px;"></a></td>
</tr>
</tbody>
</table>
<table>
<thead>
<tr>
<th align="center">필터링</th>
<th align="center">상세 페이지</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/필터링.gif"><img src="./gif/필터링.gif" alt="Filtered" style="width: 400px;"></a></td>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/상품 상세페이지.gif"><img src="./gif/상품 상세페이지.gif" alt="ProductDetail" style="width: 400px;"></a></td>
</tr>
</tbody>
</table>
<table>
<thead>
<tr>
<th align="center">찜하기</th>
<th align="center">찜 취소</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/찜하기.gif"><img src="./gif/찜하기.gif" alt="Like" style="width: 400px;"></a></td>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/찜 취소.gif"><img src="./gif/찜 취소.gif" alt="LikeCancel"  style="width: 400px;"></a></td>
</tr>
</tbody>
</table>
<table>
<thead>
<tr>
<th align="center">상품 등록</th>
<th align="center">상품 수정</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/상품등록.gif"><img src="./gif/상품등록.gif" alt="ProductRegister" style="width: 400px;"></a></td>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/상품 수정.gif"><img src="./gif/상품 수정.gif" alt="ProductUpdate" style="width: 400px;"></a></td>
</tr>
</tbody>
</table>
<table>
<thead>
<tr>
<th align="center">채팅</th>
<th align="center">로그아웃</th>
</tr>
</thead>
<tbody>
<tr>
<td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/채팅.gif"><img src="./gif/채팅.gif" alt="Chatting" style="width: 400px;"></a></td>
  <td align="center"><a target="_blank" rel="noopener noreferrer nofollow" href="./gif/로그아웃.gif"><img src="./gif/로그아웃.gif" alt="Logout" style="width: 400px;"></a></td>
</tr>
</tbody>
</table>

# 기술스택

## 사용 스택

### 🔧 System Architecture

//

# FE

<div>
<img align="center" src="https://img.shields.io/badge/HTML5-FE642E?style=flat-square&logo=html5&logoColor=white"/>
<img align="center" src="https://img.shields.io/badge/CSS3-2E9AFE?style=flat-square&logo=CSS3&logoColor=white"/>
<img align="center" src="https://img.shields.io/badge/Javascript-f7df1e?style=flat-square&logo=Javascript&logoColor=black"/><br>
<img align="center" src="https://img.shields.io/badge/React-2E2E2E?style=flat-square&logo=React&logoColor=61dafb"/>
<img align="center" src="https://img.shields.io/badge/TypeScript-3178c6?style=flat-square&logo=TypeScript&logoColor=white"/>
<img align="center" src="https://img.shields.io/badge/figma-A259FF?style=flat-square&logo=figma&logoColor=fff
"/><br>
<img align="center" src="https://img.shields.io/badge/prettier-61e1e6?style=flat-square&logo=prettier&logoColor=magenta"/>
<img align="center" src="https://img.shields.io/badge/Tailwind-06B6D4?style=flat-square&logo=tailwind-css&logoColor=fff"/>
<img align="center" src="https://img.shields.io/badge/zustand-lightgray?style=flat-square"/>
<img align="center" src="https://img.shields.io/badge/npm-%23CB3837?style=flat-square&logo=npm"/>
</div>

# BE

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-FF1709?style=flat&logo=django&logoColor=white)
![WebSocket](https://img.shields.io/badge/WebSocket-010101?style=flat&logo=socketdotio&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=flat&logo=postman&logoColor=white)<br>
![Amazon RDS](https://img.shields.io/badge/Amazon%20RDS-527FFF?style=flat&logo=amazonrds&logoColor=white)
![Amazon EC2](https://img.shields.io/badge/Amazon%20EC2-FF9900?style=flat&logo=amazonec2&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=flat&logo=amazons3&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)<br>
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Daphne](https://img.shields.io/badge/Daphne-0A0A0A?style=flat&logo=asciinema&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-85EA2D?style=flat&logo=swagger&logoColor=black)

## Team

<table>
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
<table>
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

# 📌 팀 컨벤션

🗓 일정
데일리 스크럼 : 매일 오전 10시 20분

코어 타임 : 아침 10:00 ~ 오후 06:40

휴식은 10분씩.

📣 의사소통 규칙

화나면 용용 체 쓰기

화내지 않기

어려움은 바로바로 얘기해주기(혼자 힘들어하지 말기)

###개발규칙

1일 1PR + 머지 (진행도와 충돌 여부 확인 목적)

커밋타입의 첫글자는 대문자로 작성합니다.

커밋타입: 커밋메세지
( 예시: Fix: 기본 CRUD 기능 작성 )

# ERD

<img width="1112" height="806" alt="image" src="https://github.com/user-attachments/assets/1ac48ff1-bfe8-4cb9-bb67-cd4c88eac7f2" />

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

# Document

> <a href="https://www.figma.com/design/KzCKMJ5edFNKsj0IbB3pnk/커들마켓-와이어프레임?node-id=158-2357&p=f&t=rJWfgPTkGh9rREMi-0">플로우 차트</a><br> > <a href="https://www.figma.com/design/KzCKMJ5edFNKsj0IbB3pnk/커들마켓-와이어프레임?node-id=0-1&p=f&t=rJWfgPTkGh9rREMi-0">와이어프레임</a><br> > <a href="https://www.figma.com/design/KzCKMJ5edFNKsj0IbB3pnk/커들마켓-와이어프레임?node-id=158-4&t=rJWfgPTkGh9rREMi-1">화면정의서</a><br> > <a href="https://dbdiagram.io/d/Copy-of-Copy-of-%EC%95%A0%EC%99%84%EB%8F%99%EB%AC%BC-%EC%A4%91%EA%B3%A0%EB%A7%88%EC%BC%93-ERD-689c9a3b1d75ee360a6f743a">ERD 문서</a><br> > <a href="https://docs.google.com/spreadsheets/d/12iKca5DBOynjGHntoxBUpVeOxhgDCU8V7FaVWBBDrTw/edit?gid=0#gid=0">테이블 명세서 문서</a><br> > <br>

<details>
<summary>API 문서</summary>
<div markdown="1">

| 기능 (FR)    | HTTP 메서드 | 엔드포인트                                 | 인증 | 설명                              |
| ------------ | ----------- | ------------------------------------------ | ---- | --------------------------------- |
| **FR-001**   | `POST`      | `/api/v1/auth/social/kakao`                | ❌   | 소셜 로그인 / 회원가입            |
| **FR-002**   | `GET`       | `/api/v1/users/mypage`                     | ✅   | 마이페이지 조회                   |
| **FR-003**   | `PATCH`     | `/api/v1/users/mypage/profile`             | ✅   | 프로필 정보 수정                  |
| **FR-004**   | `DELETE`    | `/api/v1/users/withdraw`                   | ✅   | 회원 탈퇴                         |
| **FR-005**   | `POST`      | `/api/v1/auth/logout`                      | ✅   | 로그아웃                          |
| **FR-006**   | `POST`      | `/api/v1/products`                         | ✅   | 상품 등록                         |
| **FR-007**   | `GET`       | `/api/v1/products`                         | ❌   | 메인 페이지 상품 게시글 목록 조회 |
| **FR-008**   | `GET`       | `/api/v1/products/{product_id}`            | ❌   | 상품 상세 조회                    |
| **FR-009**   | `PATCH`     | `/api/v1/products/{product_id}`            | ✅   | 상품 수정(제목, 거래상태 등)      |
| **FR-010**   | `DELETE`    | `/api/v1/products/{product_id}`            | ✅   | 상품 삭제                         |
| **FR-010-1** | `PATCH`     | `/api/v1/products/{product_id}/status`     | ✅   | 거래 상태 변경                    |
| **FR-011**   | `GET`       | `/api/v1/products/search`                  | ❌   | 통합 검색(필터링, 정렬)           |
| **FR-012**   | `POST`      | `/api/v1/likes`                            | ✅   | 관심 목록 추가                    |
| **FR-013**   | `DELETE`    | `/api/v1/likes`                            | ✅   | 관심 목록 삭제                    |
| **FR-014**   | `GET`       | `/api/v1/likes`                            | ✅   | 관심 목록 조회                    |
| **FR-015**   | `GET`       | `/api/v1/chatrooms`                        | ✅   | 채팅방 목록                       |
| **FR-016**   | `POST`      | `/api/v1/chatrooms`                        | ✅   | 채팅방 생성                       |
| **FR-017**   | `DELETE`    | `/api/v1/chatrooms/{chatroom_id}`          | ✅   | 채팅방 삭제                       |
| **FR-018**   | `POST`      | `/api/v1/chatrooms/{chatroom_id}/messages` | ✅   | 채팅 전송                         |
| **FR-019**   | `GET`       | `/api/v1/chatrooms/{chatroom_id}/messages` | ✅   | 채팅 내역 조회                    |
| **FR-020**   | `GET`       | `/api/v1/notifications`                    | ✅   | 알림 기능                         |
| FR-021       | `GET`       | `/api/v1/users/profile`                    | ✅   | 유저 프로필 조회                  |
| FR-023       | `GET`       | `/api/v1/categories/`                      | ❌   | 카테고리 필터링                   |
| FR-024       | `GET`       | `/api/v1/categories/filters/`              | ✅   | 서브 필터                         |
| FR-025       | `GET`       | `/api/v1/products/my-products/`            |      | 내가 등록한 상품 목록             |
| FR-026       | `GET`       | `/api/v1/products/{product_id}/view-count` | ❌   | 상품 조회수 조회                  |

### 2. 엔드포인트 상세 명세

### 2.1 소셜 로그인 / 회원가입

`POST` `/api/v1/auth/social/kakao` — ❌ _(인증 불필요)_

**Path Params**

- `provider` _(string, 필수)_ — `google`, `kakao`, `naver` 중 하나

**Request Body** ✅

```json
{
  "code": "소셜로그인_인가코드"
}
```

**응답 예시 (200 OK)**

```json
{
  "access_token": "jwt_access_token",
  "refresh_token": "jwt_refresh_token",
  "user": {
    "id": 1,
    "provider": "kakao",
    "email": "user@example.com",
    "name": "홍길동",
    "nickname": "길동이",
    "profile_image": "https://example.com/profile.jpg",
    "birthday": "1998-01-01",
    "is_active": true,
    "is_staff": false,
    "is_superuser": false,
    "profile_completed": true,
    "last_login": "2025-09-08T12:34:56Z",
    "created_at": "2025-09-01T09:30:00Z",
    "state_name": "서울특별시",
    "city_name": "강남구"
  }
}
```

---

### 2.2 마이페이지 조회

`GET` `/api/v1/users/mypage` — ✅ _(인증 필요)_

**Request Body** ❌

**Query Params** ❌

**응답 예시 (200 OK)**

```json
{
  "my_product_list": [
		  {
		  "title": "제목",
		  "price": "123.00",
		  "transaction_status": "판매중",
		  "view_count": 123,
		  "main_image": "url"
		  },
		  {"title": "제목2", ...}
	],
  "liked_product_list": [
		  {
		  "title": "제목",
		  "price": "123.00",
		  "transaction_status": "판매중",
		  "view_count": 123,
		  "main_image": "url"
		  },
		  {"title": "제목2", ...}
	]
}

```

---

### 2.2.1 유저페이지 조회

`GET` `/api/v1/users/profile` — ✅ _(인증 필요)_

**Request Body** ❌

**Query Params** ❌

**응답 예시 (200 OK)**

```json
{
  "id": 1,
  "nickname": "닉네임",
  "profile_image": "https://example.com/profile.jpg",
  "state": "서울",
  "city": "강남구",
  "created_at": "2025-01-01T00:00:00"
}
```

---

### 2.3 프로필 정보 수정

`PATCH` `/api/v1/users/mypage/profile` — ✅ _(인증 필요)_

**Request Body** ✅

```json
{
  "nickname": "새닉네임",
  "profile_image": "https://example.com/new_image.jpg",
  "state": "서울",
  "city": "강남구"
}
```

**응답 예시 (200 OK)**

```json
{
  "message": "프로필 정보가 수정되었습니다."
}
```

---

### 2.4 회원 탈퇴

`DELETE` `/api/v1/users/withdraw` — ✅ _(인증 필요)_

**Request Body** ❌

**Query Params** ❌

**응답 예시 (200 OK)**

```json
{
  "message": "회원 탈퇴 완료"
}
```

---

### 2.5 로그아웃

`POST` `/api/v1/auth/logout` — ✅ _(인증 필요)_

**Request Body** ✅

```json
{
  "refresh_token": "리프레시토큰값"
}
```

**응답 예시 (200 OK)**

```json
{
  "message": "로그아웃 완료"
}
```

---

### 2.6 상품 등록

`POST` `/api/v1/products` — ✅ _(인증 필요)_

**Request Body** ✅

```json
{
  "title": "강아지 장난감",
  "description": "강아지가 좋아해요",
  "price": 15000.0,
  "images": {
    "main": "https://example.com/image1.jpg",
    "sub": ["1번사진url", "2번사진url"]
  },
  "state_code": "서울특별시",
  "city_code": "강남구",
  "category_code": "사료/간식",
  "pet_type_code": "포유류",
  "pet_type_detail_code": "강아지",
  "condition_status": "새 것"
}
```

**응답 예시 (201 Created)**

```json
{
  "message": "상품 등록 완료"
}
```

---

### 2.7 메인 페이지 상품 게시글 목록 조회

`GET` `/api/v1/products` — ❌ _(인증 불필요)_

**Query Params**

`last_id` (string, 최초 외에 필수)

`size` (int, 필수, 기본값20)

**응답 예시 (200 OK)**

```json
{
  "product_list": [
    {
      "id": 1,
      "thumbnail": "https://s3.amazonaws.com/bucket/products/1.jpg",
      "title": "강아지 장난감",
      "price": 15000,
      "pet_type_code": "강아지",
      "condition_status": "거의 새것",
      "transaction_status": "판매중",
      "elapsed_time": "2시간 전",
      "like_count": 12
    }
  ]
}
```

---

### 2.8 상품 상세 조회

`GET` `/api/v1/products/{product_id}` — ❌ _(인증 불필요)_

**Path Params**

- `product_id` _(integer, 필수)_

**응답 예시 (200 OK)**

```json
{
  "id": 1,
  "title": "강아지 장난감",
  "description": "강아지가 좋아해요",
  "price": 15000.0,
  "images": "https://example.com/image1.jpg",
  "state_code": "서울특별시",
  "city_code": "서초구",
  "category_code": "사료/간식",
  "pet_type_code": "포유류",
  "pet_type_detail_code": "강아지",
  "transaction_status": "판매중",
  "condition_status": "새 것",
  "view_count": 1234,
  "like_count": 123,
  "seller_info": {
    "id": 1,
    "seller_images": "https:example.com/image3.jpg",
    "nickname": "홍길동",
    "state": "서울특별시",
    "city": "서초구"
  },
  "seller_products": [
    {
      "id": 123,
      "thumbnail": "https:example.com/image3.jpg",
      "PetTypeDetail": "강아지",
      "condition": "거의 새것",
      "transaction_status": "판매중",
      "title": "상품 제목",
      "price": 20000,
      "elapsed_time": "2025-08-08T13:20:00",
      "like_count": 5
    }
  ]
}
```

---

### 2.9 상품 수정

`PATCH` `/api/v1/products/{product_id}` — ✅ _(인증 필요)_

**Path Params**

- `product_id` _(integer, 필수)_

**Request Body** ✅

```json

{
	"id": 123,
	"pet_type_id": 3,
	"pet_type_name": "강아지",
	"category_id":5,
	"category_name":"사료"
  "title": "수정된 상품명",
  "description": "설명 수정",
  "price": 20000,
	"condition_status":"MINT",
	"images":[
	"https://example.com/images1.jpg",
	"https://example.com/images1.jpg"
	],
	"state_id": 1,
	"state_name": "서울특별시"
	"city_id":12,
	"city_name": "강남구"

  }

```

**응답 예시 (200 OK)**

```json
{
  "message": "상품 정보가 수정되었습니다."
}
```

### 2.10-1 거래 상태 변경

`PATCH` `/api/v1/products/{product_id}/status` — ✅ _(인증 필요)_

**Path Params**

- `product_id` _(integer, 필수)_

**Request Body** ✅

```json
{
  "transaction_status": "SOLD"
}
```

**응답 예시 (200 OK)**

```json
{
  "product_id": 1,
  "transaction_status": "SOLD",
  "message": "거래 상태가 변경되었습니다."
}
```

---

### 2.11 상품 삭제

`DELETE` `/api/v1/products/{product_id}` — ✅ _(인증 필요)_

**Path Params**

- `product_id` _(integer, 필수)_

**Request Body** ❌

**응답 예시 (200 OK)**

```json
{
  "message": "상품 삭제 완료",
  "deleted_product_id": 101
}
```

---

### 2.12 통합 검색

`GET` `/api/v1/products/search` — ❌ _(인증 불필요)_

**Query Params** ✅

- `keyword` _(string, 필수)_

**응답 예시 (200 OK)**

```json

[
  {
    "id": 1,
    "thumbnail": "string(url)",
    "PetTypeDetail": "강아지",
    "condition": "거의 새것",
    "transaction_status": "판매중"
    "title": "강아지 장난감",
    "price": 15000,
    "created_at": "2025-08-13T10:32:00",
    "like_count": 15
  }
]

```

---

### 2.13 카테고리 필터링

`GET` `/api/v1/categories/` — ❌ _(인증 불필요)_

**Request Body** ❌

**응답 예시 (200 OK)**

```json
{
  "id": 1,
  "name": "포유류",
  "code": "MAMMAL",
  "children": [
    {
      "id": 10,
      "name": "강아지",
      "code": "DOG",
      "children": [
        { "id": 101, "name": "사료/간식", "code": "FOOD" },
        { "id": 102, "name": "장난감", "code": "TOY" },
        { "id": 103, "name": "사육장/하우스", "code": "CAGE" }
      ]
    },
    {
      "id": 11,
      "name": "고양이",
      "code": "CAT",
      "children": [
        { "id": 104, "name": "사료/간식", "code": "FOOD" },
        { "id": 105, "name": "캣타워", "code": "TOWER" }
      ]
    }
  ]
}
```

---

### 2.14 서브 필터

`GET` `/api/v1/categories/filter` — ❌ _(인증 불필요)_

**Query Params** _(선택)_

- `price_min` _(integer)_
- `price_max` _(integer)_
- `state` _(string)_
- `city` _(string)_

**응답 예시 (200 OK)**

```json
[
  {
    "id": 1,
    "title": "고양이 사료",
    "price": 12000,
    "thumbnail": "https://example.com/image.jpg", //“필터링 걸쳐져서 대표 상품 이미지 URL
    "state": "서울특별시",
    "city": "강남구"
  }
]
```

---

### 2.15 관심 목록 추가

`POST` `/api/v1/likes/` — ✅ _(인증 필요)_

**Request Body** ✅

```json
{
  "product_id": 1
}
```

**응답 예시 (201 Created)**

```json

{
  "message": "관심 목록에 추가되었습니다."
  "product_id": 1,
  "is_liked": true
}

```

---

### 2.16 관심 목록 삭제

`DELETE` `/api/v1/likes/` — ✅ _(인증 필요)_

**Request Body** ✅

```json
{
  "product_id": 1
}
```

**응답 예시 (200 OK)**

```json
{
  "message": "관심 목록에서 삭제되었습니다.",
  "product_id": 1,
  "is_liked": false
}
```

---

### 2.17 관심 목록 조회

`GET` `/api/v1/likes/` — ✅ _(인증 필요)_

**Request Body** ❌

**응답 예시 (200 OK)**

```json
[
  {
    "product_id": 1,
    "title": "강아지 장난감",
    "price": 15000,
    "thumbnail": "https://example.com/image.jpg",
    "view_count": 3,
    "transaction_status": "SELLING
  }
]

```

---

### 2.19 채팅방 목록 조회

`GET` `/api/v1/chatrooms` — ✅ _(인증 필요)_

**Query Params** _(선택)_

- `page` _(integer)_ — 기본값 1
- `page_size` _(integer)_ — 기본값 20

**응답 예시 (200 OK)**

```json
[
  {
    "partner_nickname": "고양이파",  # 상대방 닉네임
    "product_image": "https://example.com/image.jpg",
    "product_title": "강아지 장난감",
    "product_price": 15000,
    "last_message": "안녕하세요!",
    "last_message_time": "2025-08-13T10:32:00"
  }
]

```

---

### 2.20 채팅방 생성

`POST` `/api/v1/chatrooms/` — ✅ _(인증 필요)_

**Request Body** ✅

```json
{
  "buyer_id": 1,
  "product_id": 1,
  "seller_id": 2
}
```

**응답 예시 (201 Created)**

```json
{
  "chatroom_id": 12,
  "message": "채팅방이 생성되었습니다."
}
```

---

### 2.21 채팅 전송

`POST` `/api/v1/chatrooms/{chatroom_id}/messages/` — ✅ _(인증 필요)_

**Path Params**

- `chatroom_id` _(integer, 필수)_

**Request Body** ✅

```json
{
  "content": "안녕하세요!"
}
```

**응답 예시 (201 Created)**

```json
{
  "message": "메시지 전송 완료"
}
```

---

### 2.22 채팅방 삭제

`DELETE` `/api/v1/chatrooms/{chatroom_id}` — ✅ _(인증 필요)_

**Path Params**

- `chatroom_id` _(integer, 필수)_

**Request Body** ❌

**응답 예시 (200 OK)**

```json
{
  "message": "채팅방이 삭제되었습니다."
}
```

---

### 2.23 채팅 내역 조회

`GET` `/api/v1/chatrooms/{chatroom_id}/messages/` — ✅ _(인증 필요)_

**Path Params**

- `chatroom_id` _(integer, 필수)_

**Query Params** _(선택)_

- `page` _(integer)_ — 기본값 1
- `page_size` _(integer)_ — 기본값 50

**응답 예시 (200 OK)**

```json
{
  "messages": [
    {
      "sender_nickname": "강아지사랑",
      "message": "안녕하세요!"
    },
    {
      "sender_nickname": "고양이파",
      "message": "반갑습니다!"
    }
  ]

```

---

### 2.24 알림 기능

`GET` `/api/v1/notifications` — ✅ _(인증 필요)_

**Query Params** _(선택)_

- `is_read` _(boolean)_ — 읽음 여부 필터

**응답 예시 (200 OK)**

```json
[
  {
    "id": 123,
    "type": "CHAT",
    "message": "새로운 채팅 메시지가 도착했습니다."
  }
]
```

---

### 2.26 상품 조회수 조회

`GET` `/api/v1/products/{product_id}/view-count` — ❌ _(인증 불필요)_

**Path Params**

- `product_id` _(integer, 필수)_

**응답 예시 (200 OK)**

```json
{
  "product_id": 1,
  "view_count": 152
}
```

</div>
</details>

<details>
<summary>사용자 요구사항 정의서</summary>
<div markdown="1">

<img width="1342" height="867" alt="image" src="https://github.com/user-attachments/assets/f671f60a-f2ba-4525-a58d-d651433646e9" />
<img width="1327" height="888" alt="image" src="https://github.com/user-attachments/assets/b6ed201e-bf22-4c76-8374-1eaa5e3d2537" />
<img width="1338" height="851" alt="image" src="https://github.com/user-attachments/assets/2901cb4f-4f35-4b35-a11c-567f76e0f671" />
<img width="1340" height="877" alt="image" src="https://github.com/user-attachments/assets/ccb17b5b-cc63-4f8f-b99b-d9c1c25461f1" />

</div>
</details>
