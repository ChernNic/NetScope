import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import terminal.routing  # убедись, что это есть

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "NetScope.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(terminal.routing.websocket_urlpatterns)
    ),
})
