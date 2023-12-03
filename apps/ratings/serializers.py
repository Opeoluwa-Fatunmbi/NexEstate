from rest_framework import serializers
from .models import Rating
from apps.profiles.models import Profile


class RatingSerializer(serializers.Serializer):
    rater = serializers.SerializerMethodField(read_only=True)
    agent = serializers.SerializerMethodField(read_only=True)

    def get_rater(self, obj):
        return obj.user.username

    def get_agent(self, obj):
        return obj.agent.user.username
    
    def create(self, validated_data):
        return Rating.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.rating = validated_data.get("rating", instance.rating)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.save()
        return instance

