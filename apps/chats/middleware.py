from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken,AccessToken
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
import jwt
from django.conf import settings
User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        query_params = parse_qs(query_string)

        token = query_params.get("token", [None])[0]

        if token:
            try:
                #  signature + 만료 검증
                UntypedToken(token)  

                #  user_id 가져오기
                decoded = jwt.decode(
                    token,
                    settings.SIMPLE_JWT.get("SIGNING_KEY", settings.SECRET_KEY),
                    algorithms=[settings.SIMPLE_JWT.get("ALGORITHM", "HS256")]
                )
                scope["user"] = await self.get_user(decoded["user_id"])

            except Exception as e:
                print("JWT Error:", e)   # 👉 디버깅 로그 꼭 찍어주세요
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()
