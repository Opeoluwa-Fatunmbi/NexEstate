from rest_framework import serializers
from .models import Rating
from apps.profiles.models import Profile


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField()
    comment = serializers.CharField()

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

    def create(self, validated_data):
        rating = Rating.objects.create(**validated_data)
        return rating

    def update(self, instance, validated_data):
        instance.rating = validated_data.get("rating", instance.rating)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "rating": instance.rating,
            "comment": instance.comment,
            "user": instance.user.id,
            "agent": instance.agent.id,
        }

    def to_internal_value(self, data):
        return {
            "rating": data.get("rating"),
            "comment": data.get("comment"),
            "user": data.get("user"),
            "agent": data.get("agent"),
        }

    def validate(self, data):
        user = data.get("user")
        agent = data.get("agent")
        if user == agent:
            raise serializers.ValidationError("You cannot rate yourself")
        if not Profile.objects.filter(user=agent).exists():
            raise serializers.ValidationError("Agent does not exist")
        return data
