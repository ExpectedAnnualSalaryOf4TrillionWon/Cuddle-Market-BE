FROM python:3.12.6-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install uv

RUN uv venv /opt/venv

COPY pyproject.toml uv.lock ./

# 가상 환경에 의존성 설치
# lock 파일이 변경될 때만 이 레이어가 재실행됩니다.
RUN /opt/venv/bin/uv pip sync uv.lock


# Final Stage
FROM python:3.12.6-slim

# 작업 디렉토리 설정
WORKDIR /app

# 런타임에 필요한 시스템 의존성만 설치 (용량이 작은 libpq5 사용)
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*

# Builder 스테이지에서 생성한 가상환경을 통째로 복사
COPY --from=builder /opt/venv /opt/venv

# 나머지 소스 코드를 복사
COPY . .

# 가상환경을 활성화하도록 PATH 설정
ENV PATH="/opt/venv/bin:$PATH"

# 포트 노출
EXPOSE 8000

# 서버 실행
CMD ["bash", "resources/scripts/run.sh"]