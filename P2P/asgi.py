
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from accounts import *
from contact import *
from currency import *
from payment import *
from chat.routings import websocket_urlpatterns
import django
from channels.routing import get_default_application
from django.core.wsgi import get_wsgi_application
from P2P.settings import CHANNEL_LAYERS
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P2P.settings')
wsgi_app=get_wsgi_application()
asgi_app=get_asgi_application()

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})

# Use pre-defined channel layer
channel_layer = CHANNEL_LAYERS['redis']
