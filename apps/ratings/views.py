from django.shortcuts import render
from adrf.views import APIView
from rest_framework import status
from apps.ratings.models import Rating
from apps.ratings.serializers import RatingSerializer
from apps.common.responses import CustomResponse
from rest_framework.throttling import UserRateThrottle
from apps.profiles.models import Profile
from apps.accounts.models import User


# Create your views here.


class CreateAgentReview(APIView):
    throttle_classes = [UserRateThrottle]
    throttle_scope = "create_agent_review"

    async def post(self, request, profile_id):
        agent_profile = await Profile.objects.get(id=profile_id, is_agent=True)
        if not agent_profile:
            return CustomResponse.error(message="Agent not found", status=404)
        data = request.data
        profile_user = await User.objects.get(id=agent_profile.user.id)

        if profile_user.email == request.user.email:
            return CustomResponse.error(message="You cannot rate yourself", status=403)

        already_exists = Rating.objects.filter(
            rater=request.user, agent=agent_profile
        ).exists()
        if already_exists:
            return CustomResponse.error(
                message="You have already rated this agent", status=403
            )
        elif data["rating"] not in [1, 2, 3, 4, 5]:
            return CustomResponse.error(
                message="Rating must be between 1 and 5", status=400
            )
        elif data["rating"] == 0:
            return CustomResponse.error(
                message="Rating must be between 1 and 5", status=400
            )
        else:
            data["rater"] = request.user.id
            data["agent"] = agent_profile.id
            serializer = RatingSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return CustomResponse.success(
                    message="Rating created successfully", status=201
                )
            return CustomResponse.error(serializer.errors, status=400)
