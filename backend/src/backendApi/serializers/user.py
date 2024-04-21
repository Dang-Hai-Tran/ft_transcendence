from rest_framework import serializers
from ..models import User, Otp
import pyotp


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "level",
            "status",
            "avatarPath",
            "last_login",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "is_staff",
            "is_superuser",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        secretKey = pyotp.random_base32()
        Otp.objects.create(user=user, secretKey=secretKey)
        return user
