from backendApi.models import User, Friendship, BannedUser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from datetime import datetime

from backendApi.serializers.friendship import FriendshipSerializer


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
            return Response({"error": "User not found"}, status=404)

        # Check if the invitation is already sent
        if (
            Friendship.objects.filter(
                sender=sender, receiver=receiver, status="pending"
            ).exists()
            or Friendship.objects.filter(
                sender=receiver, receiver=sender, status="pending"
            ).exists()
        ):
            return Response({"error": "Invitation already sent"}, status=400)

        # Check if sender and user are friends
        if (
            Friendship.objects.filter(
                sender=sender, receiver=receiver, status="accepted"
            ).exists()
            or Friendship.objects.filter(
                sender=receiver, receiver=sender, status="accepted"
            ).exists()
        ):
            return Response({"error": "User is already a friend"}, status=400)

        # Check if the receiver is banned by the sender
        if BannedUser.objects.filter(sender=sender, receiver=receiver).exists():
            banned_user = BannedUser.objects.get(sender=sender, receiver=receiver)
            if banned_user.until >= datetime.now().date():
                return Response({"error": "User is banned"}, status=400)

        # Create a new friendship request
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
