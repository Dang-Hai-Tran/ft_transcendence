from backendApi.models import ChannelBannedUser
from rest_framework import serializers


class ChannelBannedUserSerializer(serializers.ModelSerializer):
    channel_name = serializers.CharField(source="channel.name", read_only=True)
    banneduser_name = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = ChannelBannedUser
        fields = ["id", "channel_name", "banneduser_name", "until", "created_at"] 
