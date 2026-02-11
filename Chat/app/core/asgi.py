import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import app.messaging.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.core.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                app.messaging.routing.websocket_urlpatterns
            )
        ),
    }
)
