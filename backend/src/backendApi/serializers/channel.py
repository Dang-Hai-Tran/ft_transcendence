from rest_framework import serializers
from ..models import User, Channel


class BaseChannelSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    admin_usernames = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    member_usernames = serializers.ListField(
        child=serializers.CharField(), required=False
    )

    def validate(self, data):
        super().validate(data)
        owner = self.context["request"].user
        admin_usernames = data.get("admin_usernames", [owner.username])
        member_usernames = data.get("member_usernames", [owner.username])
        # Raise an error if the owner is not in admin_usernames
        if owner.username not in admin_usernames:
            raise serializers.ValidationError("The owner must be in admin_usernames.")
        # Raise an error if the owner is not in member_usernames
        if owner.username not in member_usernames:
            raise serializers.ValidationError("The owner must be in member_usernames.")
        # Raise an error if exists an admin_username not in member_usernames
        for admin_username in admin_usernames:
            if admin_username not in member_usernames:
                raise serializers.ValidationError(
                    "All admin_usernames must be in member_usernames."
                )

        return data


class ChannelSerializer(BaseChannelSerializer):
    class Meta:
        model = Channel
        fields = [
            "id",
            "name",
            "visibility",
            "password",
            "owner_username",
            "admin_usernames",
            "member_usernames",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def get_admin_usernames(self, obj):
        return [admin.username for admin in obj.admins.all()]

    def get_member_usernames(self, obj):
        return [member.username for member in obj.members.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["admin_usernames"] = self.get_admin_usernames(instance)
        representation["member_usernames"] = self.get_member_usernames(instance)
        return representation

    def create(self, validated_data):
        # Get the current user from the request
        owner = self.context["request"].user
        # if password is provided, set validated_data['visibility'] to 'protected'
        if "password" in validated_data:
            validated_data["visibility"] = "protected"
        # Set the owner_username, admin_usernames, and member_usernames by default
        validated_data["owner"] = owner
        admin_usernames = validated_data.pop("admin_usernames", [owner.username])
        member_usernames = validated_data.pop("member_usernames", [owner.username])

        # Create the channel
        channel = Channel.objects.create(**validated_data)

        # Add the admins and members
        admins = User.objects.filter(username__in=admin_usernames)
        channel.admins.set(admins)
        members = User.objects.filter(username__in=member_usernames)
        channel.members.set(members)

        return channel

    def update(self, instance, validated_data):
        admin_usernames = validated_data.pop("admin_usernames", None)
        member_usernames = validated_data.pop("member_usernames", None)
        if admin_usernames is not None:
            admins = User.objects.filter(username__in=admin_usernames)
            instance.admins.set(admins)
        if member_usernames is not None:
            members = User.objects.filter(username__in=member_usernames)
            instance.members.set(members)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
