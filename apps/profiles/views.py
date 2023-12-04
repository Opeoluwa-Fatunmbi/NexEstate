from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from apps.common.responses import CustomResponse
from adrf.views import APIView
from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer, UpdateProfileSerializer
from apps.profiles.exceptions import ProfileNotFound, NotYourProfile
from apps.profiles.renderers import ProfileJSONRenderer

# Create your views here.


class AgentListView(APIView):
    serializer_class = ProfileSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @extend_schema(
        description="Get all agents",
        responses={200: ProfileSerializer(many=True)},
    )
    def get(self, request):
        queryset = Profile.objects.filter(is_agent=True)
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse.success(serializer.data, status=200)


class TopAgentsListView(APIView):
    serializer_class = ProfileSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    @extend_schema(
        description="Get top agents",
        responses={200: ProfileSerializer(many=True)},
    )
    def get(self, request):
        queryset = Profile.objects.filter(is_agent=True).order_by("-rating")[:10]
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse.success(serializer.data, status=200)


class GetProfileView(APIView):
    serializer_class = ProfileSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    renderer_classes = (ProfileJSONRenderer,)

    @extend_schema(
        description="Get a user's profile",
        responses={200: ProfileSerializer()},
    )
    def get(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        if profile.user != user:
            raise ProfileNotFound
        serializer = self.serializer_class(profile)
        return CustomResponse.success(serializer.data, status=200)


class UpdateProfileView(APIView):
    serializer_class = UpdateProfileSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    renderer_classes = (ProfileJSONRenderer,)

    @extend_schema(
        description="Update a user's profile",
        responses={200: ProfileSerializer()},
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        if profile.user != user:
            raise NotYourProfile
        serializer = self.serializer_class(profile, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(serializer.data, status=200)
