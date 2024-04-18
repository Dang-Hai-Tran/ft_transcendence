from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from backendApi.hash import hash_password, verify_password
import pyotp


class User(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    statusChoices = [("online", "Online"), ("offline", "Offline")]
    status = models.CharField(max_length=100, choices=statusChoices, default="offline")
    avatarPath = models.CharField(max_length=100, default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.password.startswith("pbkdf2_sha256"):
            self.password = hash_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} : {self.username}"


class Channel(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, unique=True)
    visibilityChoices = [("public", "Public"), ("private", "Private")]
    visibility = models.CharField(choices=visibilityChoices, default="public")
    password = models.CharField(max_length=100, null=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="channel_owner",
    )
    members = models.ManyToManyField(User, related_name="channel_members")
    admins = models.ManyToManyField(User, related_name="channel_admins")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith("pbkdf2_sha256"):
            self.password = hash_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} : {self.name}"


class ChannelBannedUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="channelbanneduser_user"
    )
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="channelbanneduser_channel"
    )
    until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel.name} : {self.user.username}"


class ChannelMutedUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="channelmuteduser_user"
    )
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="channelmuteduser_channel"
    )
    until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel.name} : {self.user.username}"


class ChannelInvitedUser(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="channelinviteduser_user"
    )
    channel = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="channelinviteduser_channel"
    )
    statusChoices = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(choices=statusChoices, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.channel.name} : {self.user.username}"


class Game(models.Model):
    visibilityChoices = [("public", "Public"), ("private", "Private")]
    visibility = models.CharField(choices=visibilityChoices, default="public")
    modeChoices = [("normal", "Normal"), ("tournament", "Tournament")]
    mode = models.CharField(choices=modeChoices, default="normal")
    statusChoices = [("in progressing", "In progressing"), ("end", "End")]
    status = models.CharField(choices=statusChoices, default="in progressing")
    maxScore = models.IntegerField()
    users = models.ManyToManyField(User, related_name="game_users")
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="game_winner"
    )
    winnerScore = models.IntegerField(null=True, blank=True)
    loser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="game_loser")
    loserScore = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} : {self.mode} - {self.visibility} - {self.status}"


class GameScore(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="gamescore_game")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gamescore_user")
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.game.id} - {self.user.username}: {self.score}"


class UserMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="usermessage_sender"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="usermessage_receiver"
    )
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChannelMessage(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="channelmessage_sender"
    )
    receiver = models.ForeignKey(
        Channel, on_delete=models.CASCADE, related_name="channelmessage_receiver"
    )
    content = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Friendship(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendship_sender"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friendship_receiver"
    )
    statusChoices = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]
    status = models.CharField(max_length=100, choices=statusChoices, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender} : {self.receiver}"


class MutedUser(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="muteduser_sender"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="muteduser_receiver"
    )
    until = models.DateField()
    mutedReason = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BannedUser(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="banneduser_sender"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="banneduser_receiver"
    )
    until = models.DateField()
    bannedReason = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Otp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    secretKey = models.CharField(max_length=100, unique=True)
    otpStatus = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def getOtp(self):
        totp = pyotp.TOTP(self.secretKey)
        otp = totp.now()
        return otp

    def verifyOtp(self, otpVerified):
        totp = pyotp.TOTP(self.secretKey)
        return totp.verify(otpVerified, valid_window=60)
