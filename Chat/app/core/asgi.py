import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.core.settings")

django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter

import app.messaging.routing
from app.messaging.middleware import JWTAuthMiddleware

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": JWTAuthMiddleware(
            URLRouter(app.messaging.routing.websocket_urlpatterns)
        ),
    }
)
