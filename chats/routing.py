from django.urls import re_path

from .consumers import ChatConsumer, NotificationConsumer
from supports.consumers import SupportChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/notification/$', NotificationConsumer.as_asgi()),
    re_path(r'ws/support_chat/(?P<room_name>\w+)/$', SupportChatConsumer.as_asgi()),
]