"""
ASGI config for gun_shot_detector project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

from channels.middleware import BaseMiddleware
import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

from detector.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gun_shot_detector.settings')
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# application = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(URLRouter(websocket_urlpatterns))),
})


# from channels.middleware import ProtocolTypeMiddleware, BaseMiddleware

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gun_detector.settings')  # Replace 'your_project' with your project name


class CORSMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope['headers'].append((b'Access-Control-Allow-Origin', b'*'))
        return await super().__call__(scope, receive, send)
