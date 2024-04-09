# Import dependencies
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.user import UserViewSet
from .views.channel import ChannelViewSet
from .views.user_message import UserMessageViewSet
from .views.otp import OtpViewSet
from .consumers.userchat import UserChatConsumer

urlpatterns = [
    # Tokens
    path("token", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
    # Users
    path("users", UserViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "users/<int:pk>",
        UserViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    # Auth
    path("auth/register", UserViewSet.as_view({"post": "register"})),
    path("auth/login", UserViewSet.as_view({"post": "logIn"})),
    path("auth/logout", UserViewSet.as_view({"post": "logOut"})),
    path("profile/me", UserViewSet.as_view({"get": "getMe", "put": "updateMe"})),
    path(
        "profile/me/avatar",
        UserViewSet.as_view({"post": "uploadAvatarPicture", "get": "getAvatarPicture"}),
    ),
    # OTP
    path("otps", OtpViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "otps/<int:pk>",
        OtpViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    # Auth
    path("auth/otp", OtpViewSet.as_view({"get": "getOtpCode"})),
    path("auth/otp/check", OtpViewSet.as_view({"post": "checkOtpCode"})),
    path("auth/otp/qr-code", OtpViewSet.as_view({"get": "getQRcode"})),
    path("auth/otp/status", OtpViewSet.as_view({"get": "getOtpStatus"})),
    path("auth/otp/switch", OtpViewSet.as_view({"post": "switchOtpStatus"})),
    path(
        "user-messages", UserMessageViewSet.as_view({"get": "list", "post": "create"})
    ),
    path(
        "user-messages/<int:pk>",
        UserMessageViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    # Channels
    path("channels", ChannelViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "channels/<int:pk>",
        ChannelViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        "channels/me",
        ChannelViewSet.as_view({"post": "generateChannel", "get": "listChannels"}),
    ),
    path(
        "channels/me/<int:pk>",
        ChannelViewSet.as_view({"put": "updateChannel"}),
    ),
]
