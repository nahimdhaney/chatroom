from django.urls import re_path

from . import consumers
from bot import consumers as consumers2
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
]
