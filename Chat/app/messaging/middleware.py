import logging
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

logger = logging.getLogger(__name__)


class JWTAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
        self.jwt_auth = JWTAuthentication()

    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        query_params = parse_qs(query_string)
        logger.info(f"Query string recebida: {query_string}")

        token = query_params.get("token")

        if token:
            try:
                token_str = token[0]
                logger.info(f"Token encontrado: {token_str[:20]}...")
                validated_token = self.jwt_auth.get_validated_token(token_str)
                user = await sync_to_async(self.jwt_auth.get_user)(validated_token)
                scope["user"] = user
                logger.info(f"Usuário autenticado: {user.username}")
            except (InvalidToken, TokenError) as e:
                logger.error(f"Erro na validação do token: {e}")
                scope["user"] = AnonymousUser()
        else:
            logger.warning("Nenhum token encontrado na query string")
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)
