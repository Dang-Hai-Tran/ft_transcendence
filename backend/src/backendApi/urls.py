# Import dependencies
from django.urls import path
from .views import UserViewSet, ChannelViewSet, GameViewSet, MessageViewSet, MutedCommandViewSet, BannedCommandViewSet, InvitedCommandViewSet, OtpViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('users', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('users/<int:pk>',
         UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('users/signup', UserViewSet.as_view({'post': 'signUp'})),
    path('users/signin', UserViewSet.as_view({'post': 'signIn'})),
    path('users/logout', UserViewSet.as_view({'post': 'logOut'})),
    path('users/me', UserViewSet.as_view({'get': 'getMe'})),
    path('channels', ChannelViewSet.as_view(
        {'get': 'list', 'post': 'create'})),
    path('channels/<int:pk>',
         ChannelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('games', GameViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('games/<int:pk>',
         GameViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('messages', MessageViewSet.as_view(
        {'get': 'list', 'post': 'create'})),
    path('messages/<int:pk>',
         MessageViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('muted-commands',
         MutedCommandViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('muted-commands/<int:pk>',
         MutedCommandViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('banned-commands',
         BannedCommandViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('banned-commands/<int:pk>',
         BannedCommandViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'})),
    path('invited-commands',
         InvitedCommandViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('invited-commands/<int:pk>', InvitedCommandViewSet.as_view(
        {'get': 'retrieve', 'delete': 'destroy'})),
    path('otps', OtpViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('otps/<int:pk>',
         OtpViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('otps/get', OtpViewSet.as_view({'get': 'getOtp'})),
    path('otps/check', OtpViewSet.as_view({'post': 'checkOtp'})),
]
