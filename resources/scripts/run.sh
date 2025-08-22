#!/bin/bash
set -e

# 데이터베이스 마이그레이션
echo "Applying database migrations..."
python manage.py migrate --noinput

# 정적 파일 수집
echo "Collecting static files..."
python manage.py collectstatic --noinput
# Gunicorn 실행
echo "Starting Gunicorn..."
exec daphne config.asgi:application -b 0.0.0.0 -p 8000