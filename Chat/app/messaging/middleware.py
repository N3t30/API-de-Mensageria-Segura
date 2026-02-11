from urllib.parse import parse_qs

from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner 
        self.jwt_auth = JWTAuthentication()

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)

        token = query_params.get("token")

        if token:
            try:
                validated_token = self.jwt_auth.get_validated_token(token[0])
                user = self.jwt_auth.get_user(validated_token)
                scope["user"] = user
            except (InvalidToken, TokenError):
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await self.inner(scope, receive, send)