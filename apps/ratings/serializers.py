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
