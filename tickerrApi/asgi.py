import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
# from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
import ticket.routing
from tickerrApi.middleware.token_auth_middleware import TokenAuthMiddleware

"""
ASGI config for tickerrApi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tickerrApi.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        TokenAuthMiddleware(
            URLRouter(
                ticket.routing.websocket_urlpatterns
            )
        )
    )
})
