from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from backendApi.hash import verify_password


from backendApi.models import Channel, ChannelInvitedUser, ChannelBannedUser, User
from backendApi.serializers.channel import ChannelSerializer
from backendApi.permissions import IsChannelAdmin, IsChannelMember, IsChannelInvitedUser


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"

    # Create channel view. Each user can create a channel.
    @action(detail=False, methods=["post"])
    def generateMyChannel(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            channel = serializer.save()
        return Response({"message": f"Channel {channel.name} created"}, status=201)

    # List every channel the user can see. That includes public channels, private channels in which the user is invited and every channels the user has joined.
    @action(detail=True, methods=["get"])
    def listMyChannels(self, request):
        user = request.user
        channelAlls = Channel.objects.all()
        channels = []
        for channel in channelAlls:
            if (
                channel.visibility == "public"
                or channel.members.filter(id=user.id).exists()
                or ChannelInvitedUser.objects.filter(
                    channel=channel, user=user
                ).exists()
            ):
                channels.append(channel)
        serializer = self.get_serializer(channels, many=True)
        return Response(serializer.data)

    # Update channel view. Only the channel's owner can update a channel.
    @action(detail=True, methods=["put"])
    def updateMyChannel(self, request, pk):
        try:
            channel = Channel.objects.get(id=pk)
        except Channel.DoesNotExist:
            return Response({"error": "Channel not found"}, status=404)
        user = request.user
        if not channel.owner == user:
            return Response({"error": "You are not the owner of this channel"}, status=403)
        serializer = self.get_serializer(channel, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    # Get channel view if user in channel or is invited or channel is public
    @action(detail=True, methods=["get"])
    def getMyChannel(self, request, pk):
        try:
            channel = Channel.objects.get(id=pk)
        except Channel.DoesNotExist:
            return Response({"error": "Channel not found"}, status=404)
        user = request.user
        if (
            not channel.visibility == "public"
            and not channel.members.filter(id=user.id).exists()
            and not ChannelInvitedUser.objects.filter(
                channel=channel, user=user
            ).exists()
        ):
            return Response(
                {
                    "error": "You are not in this channel or invited or channel isn't public"
                },
                status=403,
            )
        serializer = self.get_serializer(channel)
        return Response(serializer.data)

    # Owner add channel's admin by username
    @action(detail=True, methods=["post"])
    def addAdminChannel(self, request, pk):
        try:
            channel = Channel.objects.get(id=pk)
        except Channel.DoesNotExist:
            return Response({"error": "Channel not found"}, status=404)
        user = request.user
        if not channel.owner == user:
            return Response({"error": "You are not the owner of this channel"}, status=403)
        username = request.data.get("username", None)
        if not username:
            return Response({"error": "Username not provided"}, status=400)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        if channel.admins.filter(username=username).exists():
            return Response({"error": "User is already an admin"}, status=400)
        # Check if the user is a member of the channel
        if not channel.members.filter(id=user.id).exists():
            return Response({"error": "User is not a member"}, status=400)
        channel.admins.add(user)
        return Response({"message": f"User {username} added as admin"}, status=200)

    @action(detail=True, methods=["post"])
    def removeAdminChannel(self, request, pk):
        try:
            channel = Channel.objects.get(id=pk)
        except Channel.DoesNotExist:
            return Response({"error": "Channel not found"}, status=404)
        user = request.user
        if not channel.admins.filter(id=user.id).exists():
            return Response({"error": "You are not an admin"}, status=403)
        username = request.data.get("username", None)
        if not username:
            return Response({"error": "Username not provided"}, status=400)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        if not channel.admins.filter(username=username).exists():
            return Response({"error": "User is not an admin"}, status=400)
        channel.admins.remove(user)
        return Response({"message": f"User {username} removed as admin"}, status=200)

    @action(detail=True, methods=["post"])
    def joinChannel(self, request, pk):
        try:
            channel = Channel.objects.get(id=pk)
        except Channel.DoesNotExist:
            return Response({"error": "Channel not found"}, status=404)
        user = request.user
        if channel.members.filter(id=user.id).exists():
            return Response({"error": "You are already in this channel"}, status=400)
        # Check if the user is banned from the channel
        if ChannelBannedUser.objects.filter(channel=channel, user=user).exists():
            return Response({"error": "You are banned from this channel"}, status=403)
        # Check if user is invited
        if ChannelInvitedUser.objects.filter(channel=channel, user=user).exists():
            channel_invited_user = ChannelInvitedUser.objects.get(
                channel=channel, user=user
            )
            channel_invited_user.status = "accepted"
            channel_invited_user.save()
        else:
            if channel.visibility == "private":
                return Response(
                    {"error": "You are not invited to this private channel"},
                    status=403,
                )
            if channel.password and not verify_password(
                request.data.get("password", None), channel.password
            ):
                return Response({"error": "Invalid password provided"}, status=400)
        channel.members.add(user)
        serializer = self.get_serializer(channel)
        return Response(serializer.data, status=200)

    @action(detail=True, methods=["post"])
    def leaveChannel(self, request, pk):
        try:
            channel = Channel.objects.get(id=pk)
        except Channel.DoesNotExist:
            return Response({"error": "Channel not found"}, status=404)
        user = request.user
        if not channel.members.filter(id=user.id).exists():
            return Response({"error": "You are not in this channel"}, status=400)
        channel.members.remove(user)
        # Check if the user is an admin and remove it
        if channel.admins.filter(id=user.id).exists():
            channel.admins.remove(user)
        serializer = self.get_serializer(channel)
        return Response(serializer.data, status=200)
    
    @action(detail=True, methods=["post"])
    def banMember(self, request, pk):
        try:
            channel = Channel.objects.get(id=pk)
        except Channel.DoesNotExist:
            return Response({"error": "Channel not found"}, status=404)
        user = request.user
        if not channel.admins.filter(id=user.id).exists():
            return Response({"error": "You are not an admin"}, status=403)
        username = request.data.get("username", None)
        until = request.data.get("until", None)
        if not username:
            return Response({"error": "Username not provided"}, status=400)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        if not channel.members.filter(id=user.id).exists():
            return Response({"error": "User is not in this channel"}, status=400)
        ChannelBannedUser.objects.create(channel=channel, user=user, until=until)
        return Response({"message": f"User {username} banned"}, status=200)

    def get_permissions(self):
        if self.action in [
            "generateMyChannel",
            "listMyChannels",
            "getMyChannel",
            "updateMyChannel",
            "addAdminChannel",
            "removeAdminChannel",
            "joinChannel",
            "leaveChannel",
            "banMember",
        ]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
