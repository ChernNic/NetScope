from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/terminal/(?P<device_id>\d+)/$", consumers.TelnetConsumer.as_asgi()),
]