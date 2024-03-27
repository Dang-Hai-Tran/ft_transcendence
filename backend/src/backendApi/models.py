from collections.abc import Iterable
from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from datetime import timedelta
from django.utils import timezone
import pyotp

# Create your models here.


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    statusChoices = [("online", "Online"),
                     ("offline", "Offline")]
    status = models.CharField(
        max_length=100, choices=statusChoices, default="offline")
    avatarPath = models.CharField(max_length=100, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} : {self.username}"


class Game(models.Model):
    visibilityChoices = [("public", "Public"), ("private", "Private")]
    visibility = models.CharField(choices=visibilityChoices, default="public")
    name = models.CharField(max_length=100)
    modeChoices = [("normal", "Normal"), ("tournament", "Tournament")]
    mode = models.CharField(choices=modeChoices, default="normal")
    statusChoices = [("in progressing", "In progressing"), ("end", "End")]
    status = models.CharField(choices=statusChoices, default="in progressing")
    maxScore = models.IntegerField()
    users = models.ManyToManyField(User, related_name="game_users")
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="game_winner")
    winnerScore = models.IntegerField()
    loser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="game_loser")
    loserScore = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} : {self.name}"


class Channel(models.Model):
    visibilityChoices = [("public", "Public"), ("private", "Private")]
    visibility = models.CharField(choices=visibilityChoices, default="public")
    name = models.CharField(max_length=100, default="")
    password = models.CharField(max_length=100, null=True)
    description = models.TextField(default="")
    users = models.ManyToManyField(User, related_name="channel_users")
    createdBy = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="channel_creator")
    admins = models.ManyToManyField(User, related_name="channel_admins")
    banneds = models.ManyToManyField(User, related_name="channel_banneds")
    muteds = models.ManyToManyField(User, related_name="channel_muteds")
    inviteds = models.ManyToManyField(User, related_name="channel_invited")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} : {self.name}"


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_receiver", null=True, default=None)
    content = models.TextField(default="")
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class InvitedCommand(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invited_sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="invited_receiver")
    statusChoices = [("pending", "Pending"), ("accepted",
                                              "Accepted"), ("declined", "Declined")]
    status = models.CharField(
        max_length=100, choices=statusChoices, default="pending")
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    invitedReason = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)


class MutedCommand(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="muted_sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="muted_receiver")
    until = models.DateTimeField(default=timezone.now() + timedelta(days=1))
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE)
    mutedReason = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)


class BannedCommand(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="banned_sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="banned_receiver")
    until = models.DateTimeField()
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE)
    bannedReason = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)


class Otp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secretKey = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def getOtp(self):
        totp = pyotp.TOTP(self.secretKey, interval=120)
        otp = totp.now()
        return otp

    def verifyOtp(self, otpVerified):
        otp = self.getOtp()
        return otp == otpVerified
