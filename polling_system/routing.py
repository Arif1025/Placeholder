from django.urls import re_path
from polling_system.consumers import PollConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/$', PollConsumer.as_asgi()),
]