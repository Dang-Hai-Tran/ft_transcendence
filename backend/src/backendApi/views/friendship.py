from backendApi.models import User, Friendship, BannedUser
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

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

        # Check if the users are already friends
        if (
            Friendship.objects.filter(
                sender=sender, receiver=receiver, status="accepted"
            ).exists()
            or Friendship.objects.filter(
                sender=receiver, receiver=sender, status="accepted"
            ).exists()
        ):
            return Response({"error": "Users are already friends"}, status=400)

        # Check if the receiver is banned by the sender
        

        # Create a new friendship request
        friendship = Friendship.objects.create(
            sender=sender, receiver=receiver, status="pending"
        )
        serializer = self.get_serializer(friendship)
        return Response(serializer.data, status=201)
