# from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from django.conf import settings
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async


def _get_user(user_id):
    return get_user_model().objects.get(id=user_id)


get_user = sync_to_async(_get_user, thread_sensitive=True)


class TokenAuthMiddleware:
    """
    Token authorization middleware
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        close_old_connections()
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split()
                if token_name == 'Bearer':
                    UntypedToken(token_key)
            except (InvalidToken, TokenError) as e:
                print(e)
                return None
            else:
                decoded_data = jwt_decode(token_key, settings.SECRET_KEY, algorithms=["HS256"])
                user = await get_user(decoded_data["user_id"])
                scope['user'] = user
        return await self.app(scope, receive, send)
