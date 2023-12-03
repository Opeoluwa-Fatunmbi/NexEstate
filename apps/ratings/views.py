from django.shortcuts import render
from adrf.views import APIView
from rest_framework import status
from apps.ratings.models import Rating
from apps.ratings.serializers import RatingSerializer
from apps.common.responses import CustomResponse
from rest_framework.throttling import UserRateThrottle
from apps.profiles.models import Profile
from apps.accounts.models import User
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class CreateAgentReview(APIView):
    serializer_class = RatingSerializer
    throttle_classes = [UserRateThrottle]
    throttle_scope = "create_agent_review"
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Create a review for an agent",
        responses={201: RatingSerializer, 400: "Bad Request"},
    )
    async def post(self, request, profile_id):
        agent_profile = get_object_or_404(Profile, id=profile_id, is_agent=True)
        data = request.data
        profile_user = await User.objects.get(id=agent_profile.user.id)

        if profile_user.email == request.user.email:
            return CustomResponse.error(
                message="You cannot rate yourself", status=status.HTTP_403_FORBIDDEN
            )

        if Rating.objects.filter(rater=request.user, agent=agent_profile).exists():
            return CustomResponse.error(
                message="You have already rated this agent",
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["rater"] = request.user.id
        data["agent"] = agent_profile.id
        serializer = RatingSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                message="Rating created successfully", status=status.HTTP_201_CREATED
            )

        return CustomResponse.error(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
