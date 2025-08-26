from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
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
                # 1) 토큰 유효성 검사
                UntypedToken(token)

                # 2) 토큰 디코드
                decoded = jwt.decode(
                    token,
                    settings.SECRET_KEY,  # SIMPLE_JWT 대신 SECRET_KEY 사용
                    algorithms=["HS256"],
                )

                # 👉 여기에 print 추가 (디버깅용)
                print("🔑 JWT 토큰 디코딩 결과:", decoded)

                # 3) user_id 가져오기
                user_id = decoded.get("user_id")
                if user_id is None:
                    print("⚠️ JWT에 user_id claim 없음! decoded =", decoded)
                    scope["user"] = AnonymousUser()
                else:
                    scope["user"] = await self.get_user(user_id)

            except Exception as e:
                print("❌ JWT Error:", e)  # 👉 에러 찍기
                scope["user"] = AnonymousUser()
        else:
            print("⚠️ WebSocket 연결에 token 쿼리 파라미터 없음")
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            print("⚠️ DB에서 해당 user_id 없음:", user_id)
            return AnonymousUser()
