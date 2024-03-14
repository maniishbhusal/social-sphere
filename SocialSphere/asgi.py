import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

import ai_app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialSphere.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(ai_app.routing.websocket_urlpatterns)
    )
})
