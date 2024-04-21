from datetime import datetime

from backendApi.models import BannedUser, Friendship, MutedUser, User
from backendApi.serializers.banned_user import BannedUserSerializer
from backendApi.serializers.friendship import FriendshipSerializer
from backendApi.serializers.muted_user import MutedUserSerializer
from django.utils.dateparse import parse_date
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


class FriendshipViewSet(viewsets.ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = "__all__"

    @action(detail=True, methods=["post"])
    def inviteFriend(self, request):
        sender = request.user
        receiver_username = request.data.get("username", None)
        if not receiver_username:
            return Response({"error": "Username not provided"}, status=400)
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=404)

        # Check if the invitation is already sent
        if Friendship.objects.filter(
            sender=sender, receiver=receiver, status="pending"
        ).exists():
            return Response({"error": "Invitation already sent"}, status=400)

        # Check if sender and user are friends
        if Friendship.objects.filter(
            sender=sender, receiver=receiver, status="accepted"
        ).exists():
            return Response({"error": "Users are already friend"}, status=400)

        # Check if the receiver is banned by the sender
        if BannedUser.objects.filter(sender=sender, receiver=receiver).exists():
            banned_user = BannedUser.objects.get(sender=sender, receiver=receiver)
            if banned_user.until >= datetime.now().date():
                return Response({"error": "Receiver is banned by sender"}, status=400)

        # Check if the sender is banned by the receiver
        if BannedUser.objects.filter(sender=receiver, receiver=sender).exists():
            banned_user = BannedUser.objects.get(sender=receiver, receiver=sender)
            if banned_user.until >= datetime.now().date():
                return Response({"error": "Sender is banned by receiver"}, status=400)

        # Create a new friendship request or update the status of an existing one
        if Friendship.objects.filter(sender=sender, receiver=receiver).exists():
            friendship = Friendship.objects.get(sender=sender, receiver=receiver)
            friendship.status = "pending"
            friendship.save()
        elif Friendship.objects.filter(sender=receiver, receiver=sender).exists():
            friendship = Friendship.objects.get(sender=receiver, receiver=sender)
            friendship.status = "pending"
            friendship.save()
        else:
            friendship = Friendship.objects.create(
                sender=sender, receiver=receiver, status="pending"
            )
        serializer = self.get_serializer(friendship)
        return Response(serializer.data, status=201)

    # Update friendship status
    @action(detail=True, methods=["put"])
    def updateFriendshipStatus(self, request, friendship_id):
        try:
            friendship = Friendship.objects.get(id=friendship_id)
        except Friendship.DoesNotExist:
            return Response({"error": "Friendship not found"}, status=404)
        if not friendship.receiver == request.user:
            return Response(
                {"error": "You are not the receiver of this friendship"}, status=403
            )
        status = request.data.get("status", None)
        if not status:
            return Response({"error": "Status not provided"}, status=400)
        if status not in ["pending", "accepted", "declined"]:
            return Response({"error": "Invalid status"}, status=400)
        friendship.status = status
        friendship.save()
        serializer = self.get_serializer(friendship)
        return Response(serializer.data, status=200)

    # Get list friendship sent from user
    @action(detail=True, methods=["get"])
    def listFriendshipsSent(self, request):
        sender = request.user
        friendships = Friendship.objects.filter(sender=sender)
        serializer = self.get_serializer(friendships, many=True)
        return Response(serializer.data, status=200)

    # Get list friendship received by user
    @action(detail=True, methods=["get"])
    def listFriendshipsReceived(self, request):
        receiver = request.user
        friendships = Friendship.objects.filter(receiver=receiver)
        serializer = self.get_serializer(friendships, many=True)
        return Response(serializer.data, status=200)

    # Ban a user to send friend invitation
    @action(detail=False, methods=["post"])
    def banUser(self, request):
        sender = request.user
        receiver_username = request.data.get("username", None)
        if not receiver_username:
            return Response({"error": "Username not provided"}, status=400)
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=404)

        # Check if the user is already banned
        banned_user = None
        if BannedUser.objects.filter(sender=sender, receiver=receiver).exists():
            banned_user = BannedUser.objects.get(sender=sender, receiver=receiver)
            if banned_user.until >= datetime.now().date():
                return Response({"error": "Receiver is already banned"}, status=400)
        until_string = request.data.get("until", None)
        reason = request.data.get("bannedReason", None)
        if not until_string:
            until = datetime.max.date()
        else:
            until = parse_date(until_string)

        # Create a new banned user
        if not banned_user:
            banned_user = BannedUser.objects.create(
                sender=sender, receiver=receiver, until=until, bannedReason=reason
            )
        else:
            banned_user.until = until
            banned_user.bannedReason = reason
            banned_user.save()

        serializer = BannedUserSerializer(banned_user)
        return Response(serializer.data, status=201)

    # Unban a user
    @action(detail=True, methods=["post"])
    def unbanUser(self, request):
        sender = request.user
        receiver_username = request.data.get("username", None)
        if not receiver_username:
            return Response({"error": "Username not provided"}, status=400)
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=404)

        # Check if the user is banned
        if (
            not BannedUser.objects.filter(sender=sender, receiver=receiver).exists()
            or BannedUser.objects.get(sender=sender, receiver=receiver).until
            < datetime.now().date()
        ):
            return Response({"error": "Receiver is not banned"}, status=400)
        banned_user = BannedUser.objects.get(sender=sender, receiver=receiver)
        banned_user.until = datetime.min.date()
        banned_user.save()
        serializer = BannedUserSerializer(banned_user)
        return Response(serializer.data, status=200)

    # Muted user to send message
    @action(detail=False, methods=["post"])
    def muteUser(self, request):
        sender = request.user
        receiver_username = request.data.get("username", None)
        if not receiver_username:
            return Response({"error": "Username not provided"}, status=400)
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=404)

        # Check if the user is already muted
        muted_user = None
        if MutedUser.objects.filter(sender=sender, receiver=receiver).exists():
            muted_user = MutedUser.objects.get(sender=sender, receiver=receiver)
            if muted_user.until >= datetime.now().date():
                return Response({"error": "Receiver is already muted"}, status=400)
        until_string = request.data.get("until", None)
        reason = request.data.get("reason", None)
        if not until_string:
            until = datetime.max.date()
        else:
            until = parse_date(until_string)

        # Create a new muted user
        if not muted_user:
            muted_user = MutedUser.objects.create(
                sender=sender, receiver=receiver, until=until, mutedReason=reason
            )
        else:
            muted_user.until = until
            muted_user.mutedReason = reason
            muted_user.save()
        serializer = MutedUserSerializer(muted_user)
        return Response(serializer.data, status=201)

    # Unmute user to send message
    def unmuteUser(self, request):
        sender = request.user
        receiver_username = request.data.get("username", None)
        if not receiver_username:
            return Response({"error": "Username not provided"}, status=400)
        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({"error": "Receiver not found"}, status=404)

        # Check if the user is muted
        if (
            not MutedUser.objects.filter(sender=sender, receiver=receiver).exists()
            or MutedUser.objects.get(sender=sender, receiver=receiver).until
            < datetime.now().date()
        ):
            return Response({"error": "Receiver is not muted"}, status=400)
        muted_user = MutedUser.objects.get(sender=sender, receiver=receiver)
        muted_user.until = datetime.min.date()
        muted_user.save()
        serializer = MutedUserSerializer(muted_user)
        return Response(serializer.data, status=200)

    def get_permissions(self):
        if self.action in [
            "inviteFriend",
            "updateFriendshipStatus",
            "banUser",
            "unbanUser",
            "muteUser",
            "unmuteUser",
            "listFriendshipsSent",
            "listFriendshipsReceived",
        ]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
