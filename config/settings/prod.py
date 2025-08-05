from .base import *

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# 보안 설정
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# 배포용 static 설정 예시 (필요 시)
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
