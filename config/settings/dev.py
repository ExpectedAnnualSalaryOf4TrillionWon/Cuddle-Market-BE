from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

# 개발 환경에서만 Swagger 활성화하거나 debug toolbar 쓸 수 있음
INSTALLED_APPS += [
    # 'debug_toolbar',
    # 기타 개발용 앱
]

MIDDLEWARE += [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
]
