from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<user_name>\w+)/(?P<method_name>\w+)/$', consumers.ChatMethodConsumer.as_asgi(),name='chat_room'),
]