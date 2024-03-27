from django.shortcuts import render
from .models import User, InvitedCommand, Channel, Game, Message, MutedCommand, BannedCommand, Otp
from .serializers import UserSerializer, InvitedCommandSerializer, ChannelSerializer, GameSerializer, MessageSerializer, MutedCommandSerializer, BannedCommandSerializer, OtpSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    @action(detail=False, methods=['post'])
    def signUp(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate access and refresh tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=201)

    @action(detail=True, methods=['get'])
    def signIn(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username=username)
        if user is None:
            return Response({'message': 'User not found'}, status=404)
        if not user.check_password(password):
            return Response({'message': 'Password not matched'}, status=400)
        otp = request.data.get('otp')
        instance = Otp.objects.get(user=user)
        if not instance.verifyOtp(otp):
            return Response({'message': 'Invalid OTP'}, status=400)
        user.status = 'online'
        serializer = UserSerializer(user)
        return Response({
            'user': serializer.data
        }, status=200)

    def get_permissions(self):
        if self.action == 'signUp':
            self.permission_classes = [AllowAny]
        elif self.action == 'signIn':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


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

    @action(detail=True, methods=['get'])
    def getOtp(self, request):
        username = request.data.get('username')
        user = User.objects.get(username=username)
        if user is None:
            return Response({'message': 'User not found'}, status=404)
        instance = Otp.objects.get(user=user)
        otp = instance.getOtp()
        print(f'OTP code of {username} is {otp}')
        return Response({'otp': otp}, status=200)

    @action(detail=True, methods=['post'])
    def checkOtp(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')
        user = User.objects.get(username=username)
        if user is None:
            return Response({'message': 'User not found'}, status=404)
        instance = Otp.objects.get(user=user)
        print(f"Otp code of {username} is {instance.getOtp()}")
        if instance.verifyOtp(otp):
            return Response({'message': 'OTP verified successfully'}, status=200)
        else:
            return Response({'message': 'Invalid OTP'}, status=400)
    
    def get_permissions(self):
        if self.action in ['getOtp', 'checkOtp']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
