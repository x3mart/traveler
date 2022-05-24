from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/support_chat/(?P<room_name>\w+)/$', consumers.SupportChatConsumer.as_asgi()),
]