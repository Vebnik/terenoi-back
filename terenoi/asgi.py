"""
ASGI config for terenoi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terenoi.settings')
django.setup()
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path
from django_channels_jwt_auth_middleware.auth import JWTAuthMiddlewareStack
from notifications import consumers



ws_patterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi())

]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddlewareStack(
        URLRouter(
            ws_patterns
        )
    ),
})
