from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("map/", consumers.GPSDataConsumer.as_asgi()),
]
