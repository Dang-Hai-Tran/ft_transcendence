from .consumers.userchat import UserChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path("ws/chat/<int:user_id>/<int:other_user_id>/", UserChatConsumer),
]
