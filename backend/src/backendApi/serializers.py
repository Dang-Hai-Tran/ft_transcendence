from rest_framework import serializers
from .models import User, InvitedCommand, Channel, Game, Message, MutedCommand, BannedCommand, Otp
import pyotp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ['is_staff', 'is_superuser']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        secretKey = pyotp.random_base32()
        Otp.objects.create(user=user, secretKey=secretKey)
        return user


class ChannelSerializer(serializers.ModelSerializer):
    createdBy = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())
    admins = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())
    muteds = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())
    inviteds = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())
    banneds = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())

    class Meta:
        model = Channel
        fields = '__all__'

    def create(self, validated_data):
        createdBy = validated_data.pop('createdBy')
        users = validated_data.pop('users', [])
        admins = validated_data.pop('admins', [])
        muteds = validated_data.pop('muteds', [])
        inviteds = validated_data.pop('inviteds', [])
        banneds = validated_data.pop('banneds', [])
        channel = Channel.objects.create(createdBy=createdBy, **validated_data)
        channel.users.set(users)
        channel.admins.set(admins)
        channel.muteds.set(muteds)
        channel.inviteds.set(inviteds)
        channel.banneds.set(banneds)
        return channel

    def update(self, instance, validated_data):
        users = validated_data.pop('users', [])
        admins = validated_data.pop('admins', [])
        muteds = validated_data.pop('muteds', [])
        inviteds = validated_data.pop('inviteds', [])
        banneds = validated_data.pop('banneds', [])
        instance = super().update(instance, validated_data)
        instance.users.set(users)
        instance.admins.set(admins)
        instance.muteds.set(muteds)
        instance.inviteds.set(inviteds)
        instance.banneds.set(banneds)
        instance.save()
        return instance


class GameSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())

    class Meta:
        model = Game
        fields = "__all__"

    def create(self, validated_data):
        users = validated_data.pop('users', [])
        game = Game.objects.create(**validated_data)
        game.users.set(users)
        return game

    def update(self, instance, validated_data):
        users = validated_data.pop('users', [])
        instance = super().update(instance, validated_data)
        instance.users.set(users)
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class InvitedCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitedCommand
        fields = "__all__"


class MutedCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = MutedCommand
        fields = "__all__"
    # Override the default create method to add muted user to the muteds field in Channel model

    def create(self, validated_data):
        muted_user = validated_data.pop('receiver')
        channel = validated_data.pop('channel')
        if channel:
            channel.muteds.add(muted_user)
        muted_command = MutedCommand.objects.create(**validated_data)
        muted_command.save()
        return muted_command


class BannedCommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannedCommand
        fields = "__all__"

class OtpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Otp
        fields = '__all__'
