from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
import qrcode
from django.http import HttpResponse
from io import BytesIO
from django.core.files.storage import default_storage
from django.http import FileResponse

from ..models import User
from ..models import Otp
from ..serializers.otp import OtpSerializer

class OtpViewSet(viewsets.ModelViewSet):
    queryset = Otp.objects.all()
    serializer_class = OtpSerializer

    @action(detail=True, methods=['get'])
    def getOtpStatus(self, request):
        user = request.user
        if user is None:
            return Response({'error': 'User not found'}, status=404)
        instance = Otp.objects.get(user=user)
        return Response({'otpStatus': instance.otpStatus}, status=200)

    @action(detail=True, methods=['post'])
    def switchOtpStatus(self, request):
        username = request.data.get('username')
        user = User.objects.get(username=username)
        if user is None:
            return Response({'error': 'User not found'}, status=404)
        instance = Otp.objects.get(user=user)
        instance.otpStatus = not instance.otpStatus
        instance.save()
        return Response({'otpStatus': instance.otpStatus}, status=200)

    @action(detail=True, methods=['get'])
    def getOtpCode(self, request):
        user = request.user
        if user is None:
            return Response({'error': 'User not found'}, status=404)
        instance = Otp.objects.get(user=user)
        otp = instance.getOtp()
        print(f'OTP code of {user.username} is {otp}')
        return Response({'otp': otp}, status=200)

    @action(detail=True, methods=['post'])
    def checkOtpCode(self, request):
        username = request.data.get('username')
        otp = request.data.get('otp')
        user = User.objects.get(username=username)
        if user is None:
            return Response({'error': 'User not found'}, status=404)
        instance = Otp.objects.get(user=user)
        print(f"Otp code of {username} is {instance.getOtp()}")
        if instance.verifyOtp(otp):
            return Response({'message': 'OTP verified successfully'}, status=200)
        else:
            return Response({'error': 'Invalid OTP'}, status=400)

    @action(detail=False, methods=['get'])
    def getQRcode(self, request):
        user = request.user
        if user is None:
            return Response({'error': 'User not found'}, status=404)
        # Generate the OTP QR code
        otp_instance = Otp.objects.get(user=user)
        otp_secret = otp_instance.secretKey
        otp_uri = f'otpauth://totp/Transcendence:{
            user.username}?secret={otp_secret}&issuer=Transcendence'
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(otp_uri)
        qr.make(fit=True)
        # Save the QR code image to a temporary file
        img = qr.make_image(fill_color="black", back_color="white")
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        # Return the QR code image as a response
        return HttpResponse(img_io, content_type='image/png')

    def get_permissions(self):
        if self.action in ['getOtpStatus', 'switchOtpStatus', 'getOtpCode', 'checkOtpCode', 'getQRcode']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()