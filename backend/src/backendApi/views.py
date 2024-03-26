from django.shortcuts import render
from .models import User, InvitedCommand, Channel, Game, Message, MutedCommand, BannedCommand, Otp
from .serializers import UserSerializer, InvitedCommandSerializer, ChannelSerializer, GameSerializer, MessageSerializer, MutedCommandSerializer, BannedCommandSerializer, OtpSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def getUserByUsername(self, request, username):
        user = User.objects.get(username=username)
        if user is None:
            return Response({'message': 'User not found'}, status=404)
        password = request.data.get('password')
        if not user.check_password(password):
            return Response({'message': 'Password not matched'}, status=400)
        otp = request.data.get('otp')
        instance = Otp.objects.get(user=user)
        if not instance.getOtp() == otp:
            return Response({'message': 'Invalid OTP'}, status=400)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    # def get_permissions(self):
    #     if self.action == 'create':
    #         self.permission_classes = [AllowAny]
    #     elif self.action == 'list':
    #         self.permission_classes = [IsAdminUser]
    #     else:
    #         self.permission_classes = [IsAuthenticated]
    #     return super().get_permissions()


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class InvitedCommandViewSet(viewsets.ModelViewSet):
    queryset = InvitedCommand.objects.all()
    serializer_class = InvitedCommandSerializer


class MutedCommandViewSet(viewsets.ModelViewSet):
    queryset = MutedCommand.objects.all()
    serializer_class = MutedCommandSerializer


class BannedCommandViewSet(viewsets.ModelViewSet):
    queryset = BannedCommand.objects.all()
    serializer_class = BannedCommandSerializer

class OtpViewSet(viewsets.ModelViewSet):
    queryset = Otp.objects.all()
    serializer_class = OtpSerializer

    def retrieve(self, request, pk=None):
        # get otp by user
        instance = Otp.objects.get(pk=pk)
        otp = instance.getOtp()
        return Response({'otp': otp})
    
    def getOtpByUsername(self, request, username):
        user = User.objects.get(username=username)
        if user is None:
            return Response({'message': 'User not found'}, status=404)
        instance = Otp.objects.get(user=user)
        otp = instance.getOtp()
        print(f'OTP code of {username} is {otp}')
        return Response({'otp': otp}, status=200)

    def checkOtp(self, request, username):
        otp = request.data.get('otp')
        user = User.objects.get(username=username)
        if user is None:
            return Response({'message': 'User not found'}, status=404)
        instance = Otp.objects.get(user=user)
        if instance.getOtp() == otp:
            return Response({'message': 'OTP verified successfully'}, status=200)
        else:
            return Response({'message': 'Invalid OTP'}, status=400)
