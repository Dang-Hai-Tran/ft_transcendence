# Import dependencies
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.user import UserViewSet
from .views.channel import ChannelViewSet
from .views.user_message import UserMessageViewSet
from .views.otp import OtpViewSet
from .views.channel_message import ChannelMessageViewSet

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
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "channel/create",
        ChannelViewSet.as_view({"post": "createChannel"}),
    ),
    path("channel/list", ChannelViewSet.as_view({"get": "listMyChannels"})),
    path(
        "channel/<int:channel_id>/update",
        ChannelViewSet.as_view({"put": "updateMyChannel"}),
    ),
    path(
        "channel/<int:channel_id>/get", ChannelViewSet.as_view({"get": "getMyChannel"})
    ),
    path(
        "channel/<int:channel_id>/admin/add",
        ChannelViewSet.as_view({"post": "addAdmin"}),
    ),
    path(
        "channel/<int:channel_id>/admin/remove",
        ChannelViewSet.as_view({"post": "removeAdmin"}),
    ),
    path(
        "channel/<int:channel_id>/member/join",
        ChannelViewSet.as_view({"post": "joinChannel"}),
    ),
    path(
        "channel/<int:channel_id>/member/leave",
        ChannelViewSet.as_view({"post": "leaveChannel"}),
    ),
    path(
        "channel/<int:channel_id>/member/ban",
        ChannelViewSet.as_view({"post": "banMember"}),
    ),
    path(
        "channel/<int:channel_id>/member/unban",
        ChannelViewSet.as_view({"post": "unbanMember"}),
    ),
    path(
        "channel/<int:channel_id>/member/mute",
        ChannelViewSet.as_view({"post": "muteMember"}),
    ),
    path(
        "channel/<int:channel_id>/member/unmute",
        ChannelViewSet.as_view({"post": "unmuteMember"}),
    ),
    path(
        "channel/<int:channel_id>/member/invite",
        ChannelViewSet.as_view({"post": "inviteMember", "put": "updateInviteStatus"}),
    ),
    # Channel messages
    path(
        "channel/messages",
        ChannelMessageViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "channel/messages/<int:pk>",
        ChannelMessageViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
    ),
    path(
        "channel/<int:channel_id>/message",
        ChannelMessageViewSet.as_view(
            {
                "post": "createMessage",
                "get": "listMessages",
            }
        ),
    ),
    path(
        "channel/<int:channel_id>/message/<int:channelmessage_id>",
        ChannelMessageViewSet.as_view({"put": "updateMessageContent"}),
    ),
    path(
        "channel/<int:channel_id>/message/last",
        ChannelMessageViewSet.as_view({"get": "listLastMessages"}),
    ),
]
