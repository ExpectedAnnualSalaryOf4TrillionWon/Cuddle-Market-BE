from datetime import timedelta

from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

REFRESH_TOKEN_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=300),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
}
CSRF_COOKIE_DOMAIN = "*"

SPECTACULAR_SETTINGS = {
    "TITLE": "Cuddle Market API",
    "DESCRIPTION": "cuddle market swagger",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
}
