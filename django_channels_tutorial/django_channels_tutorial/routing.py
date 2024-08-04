from django.urls import path

from .consumers import TutorialConsumer

websocket_urlpatterns = [
    path('ws/', TutorialConsumer.as_asgi()),
]
