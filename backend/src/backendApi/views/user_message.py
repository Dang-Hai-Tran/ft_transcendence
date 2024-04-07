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

from ..models import UserMessage
from ..serializers.user_message import UserMessageSerializer

class UserMessageViewSet(viewsets.ModelViewSet):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer
