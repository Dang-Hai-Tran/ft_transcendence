from rest_framework import serializers
from ..models import User, Game

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
