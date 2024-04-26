from rest_framework import serializers
from ..models import User, Game, Tournament


class GameSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    player_usernames = serializers.ListField(
        child=serializers.CharField(), read_only=True, required=False
    )
    winner_username = serializers.CharField(source="winner.username", read_only=True)
    loser_username = serializers.CharField(source="loser.username", read_only=True)
    tournament_name = serializers.CharField()

    class Meta:
        model = Game
        fields = [
            "id",
            "visibility",
            "mode",
            "tournament_name",
            "status",
            "maxScore",
            "owner_username",
            "players_username",
            "winner",
            "winnerScore",
            "loser",
            "loserScore",
            "created_at",
            "updated_at",
        ]

        reads_only_fields = [
            "id",
            "owner_username",
            "users_username",
            "winner",
            "winnerScore",
            "loser",
            "loserScore",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        super().validate(data)
        mode = data.get("mode", None)
        if mode == "tournament":
            if "tournament_name" not in data:
                raise serializers.ValidationError("Tournament name is required")
            tournement_name = data["tournament_name"]
            try:
                tournement = Tournament.objects.get(name=tournement_name)
            except Tournament.DoesNotExist:
                raise serializers.ValidationError("Tournament not found")
            if tournement.status != "ongoing":
                raise serializers.ValidationError("Tournament is not ongoing")
        return data

    def get_player_usernames(self, obj):
        return [player.username for player in obj.players.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["player_usernames"] = self.get_player_usernames(instance)
        if instance.tournament:
            representation["tournament_name"] = instance.tournament.name
        return representation

    def create(self, validated_data):
        owner = self.context["request"].user
        tournement_name = validated_data.pop("tournament_name", None)
        game = Game.objects.create(**validated_data)
        game.owner = owner
        game.players.add(owner)
        if tournement_name:
            tournement = Tournament.objects.get(name=tournement_name)
            game.tournament = tournement
        game.save()
        return game

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
