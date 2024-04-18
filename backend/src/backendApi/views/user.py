from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.exceptions import TokenError
from datetime import timedelta
from django.core.files.storage import default_storage
from django.http import FileResponse

from ..models import User
from ..models import Otp
from ..serializers.user import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"

    @action(detail=False, methods=["post"])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": f"User {user.username} registered"}, status=201)

    @action(detail=True, methods=["post"])
    def logIn(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.get(username=username)
        if user is None:
            return Response({"error": "User not found"}, status=404)
        if not user.check_password(password):
            return Response({"error": "Password not matched"}, status=400)
        instance = Otp.objects.get(user=user)
        if instance.otpStatus:
            if "otp" not in request.data:
                return Response({"error": "No OTP provided"}, status=400)
            otp = request.data.get("otp")
            if not instance.verifyOtp(otp):
                return Response({"error": "Invalid OTP"}, status=400)
        user.status = "online"
        user.save()
        refresh = RefreshToken.for_user(user)
        request.session["refresh_token"] = str(refresh)
        return Response(
            {
                "message": f"User {username} login",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=200,
        )

    @action(detail=True, methods=["post"])
    def logOut(self, request):
        user = request.user
        # Update user status to 'offline'
        user.status = "offline"
        user.save()
        # Invalidate access token
        refresh_token = request.session.get("refresh_token")
        if not refresh_token:
            return Response({"error": "No refresh token found"}, status=400)
        try:
            refresh = RefreshToken(token=refresh_token, verify=True)
            access_token = refresh.access_token
            access_token.set_exp(lifetime=timedelta(seconds=0))
            del request.session["refresh_token"]
        except TokenError:
            return Response({"error": "Invalid refresh token"}, status=400)
        return Response({"message": f"User {user.username} logout"}, status=200)

    @action(detail=True, methods=["get"])
    def getMe(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["put"])
    def updateMe(self, request):
        user = request.user
        # Update user data
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    @action(detail=True, methods=["post"])
    def uploadAvatarPicture(self, request):
        user = request.user
        avatar = request.FILES.get("avatar")
        if avatar:
            avatarPath = default_storage.save(
                f"avatars/{user.username}/{avatar.name}", avatar
            )
            user.avatarPath = avatarPath
            user.save()
            return Response({"message": "Avatar uploaded successfully"}, status=200)
        else:
            return Response({"error": "No avatar picture provided"}, status=400)

    @action(detail=True, methods=["get"])
    def getAvatarPicture(self, request):
        user = request.user
        avatarPath = user.avatarPath
        if avatarPath:
            return FileResponse(default_storage.open(avatarPath, "rb"))
        else:
            return Response({"error": "Profile picture not found"}, status=404)

    def get_permissions(self):
        if self.action in ["register", "logIn"]:
            self.permission_classes = [AllowAny]
        elif self.action in [
            "list",
            "logOut",
            "getMe",
            "updateMe",
            "getAvatarPicture",
            "uploadAvatarPicture",
        ]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
