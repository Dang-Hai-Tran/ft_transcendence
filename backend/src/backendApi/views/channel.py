from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.files.storage import default_storage
from django.db.models import Q

from ..models import Channel, ChannelInvitedUser
from ..serializers.channel import ChannelSerializer
from ..permissions import IsChannelAdmin, IsChannelMember, IsChannelInvitedUser

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    # Create channel view. Each user can create a channel.
    @action(detail=False, methods=['post'])
    def generateChannel(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        channel = serializer.save()
        return Response({"message": f"Channel {channel.name} created"}, status=201)
    
    # List every channel the user can see. That includes public channels, private channels in which the user is invited and every channels the user has joined.
    @action(detail=True, methods=['get'])
    def listChannels(self, request):
        user = request.user
        channelAlls = Channel.objects.all()
        channels = []
        for channel in channelAlls:
            if channel.visibility == 'public' or (channel.visibility == 'protected' and channel.members.filter(id=user.id).exists()):
                channels.append(channel)
            elif channel.visibility == 'private' and (ChannelInvitedUser.objects.filter(channel=channel, user=user).exists() or channel.members.filter(id=user.id).exists()):
                channels.append(channel)
        serializer = self.get_serializer(channels, many=True)
        return Response(serializer.data)
    
    # Update channel view. Only admin can update a channel.
    @action(detail=True, methods=['put'])
    def updateChannel(self, request, pk):
        channel = Channel.objects.get(id=pk)
        if not channel:
            return Response({'error': 'Channel not found'}, status=404)
        user = request.user
        if not channel.admins.filter(id=user.id).exists():
            return Response({'error': 'You are not an admin'}, status=403)
        serializer = self.get_serializer(channel, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
    
    def get_permissions(self):
        if self.action in ['generateChannel', 'listChannels']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['updateChannel']:
            self.permission_classes = [IsChannelAdmin]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
