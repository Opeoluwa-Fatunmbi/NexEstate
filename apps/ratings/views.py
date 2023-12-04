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
from rest_framework import serializers
from apps.ratings.pagination import AgentReviewPagination


# Create your views here.


class CreateAgentReview(APIView):
    serializer_class = RatingSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Create a review for an agent",
        responses={201: RatingSerializer()},
    )
    def post(self, request, profile_id):
        user = request.user
        agent = get_object_or_404(Profile, id=profile_id)
        if agent.user == user:
            raise serializers.ValidationError("You cannot rate yourself")
        if not Profile.objects.filter(user=agent.user).exists():
            raise serializers.ValidationError("Agent does not exist")
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, agent=agent)
        return CustomResponse.success(serializer.data, status=201)


class DeleteAgentReview(APIView):
    serializer_class = RatingSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Delete a review for an agent",
        responses={204: "No Content"},
    )
    def delete(self, request, profile_id):
        user = request.user
        agent = get_object_or_404(Profile, id=profile_id)
        rating = Rating.objects.get(user=user, agent=agent)
        rating.delete()
        return CustomResponse.success(status=204)


class UpdateAgentReview(APIView):
    serializer_class = RatingSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Update a review for an agent",
        responses={200: RatingSerializer()},
    )
    def put(self, request, profile_id):
        user = request.user
        agent = get_object_or_404(Profile, id=profile_id)
        rating = Rating.objects.get(user=user, agent=agent)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(rating, serializer.validated_data)
        return CustomResponse.success(serializer.data, status=200)


class GetAgentReviews(APIView):
    serializer_class = RatingSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]
    pagination_class = AgentReviewPagination

    @extend_schema(
        description="Get all reviews for an agent",
        responses={200: RatingSerializer(many=True)},
    )
    def get(self, request, profile_id):
        agent = get_object_or_404(Profile, id=profile_id)
        queryset = Rating.objects.filter(agent=agent)
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse.success(serializer.data, status=200)


class GetAgentReviewDetail(APIView):
    serializer_class = RatingSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Get a review for an agent",
        responses={200: RatingSerializer()},
    )
    def get(self, request, profile_id):
        user = request.user
        agent = get_object_or_404(Profile, id=profile_id)
        rating = Rating.objects.get(user=user, agent=agent)
        serializer = self.serializer_class(rating)
        return CustomResponse.success(serializer.data, status=200)


class GetAgentAverageRating(APIView):
    serializer_class = RatingSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Get the average rating for an agent",
        responses={200: RatingSerializer()},
    )
    def get(self, request, profile_id):
        agent = get_object_or_404(Profile, id=profile_id)
        queryset = Rating.objects.filter(agent=agent)
        serializer = self.serializer_class(queryset, many=True)
        ratings = [rating["rating"] for rating in serializer.data]
        average_rating = sum(ratings) / len(ratings)
        return CustomResponse.success({"average_rating": average_rating}, status=200)


class GetAgentRatingCount(APIView):
    serializer_class = RatingSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Get the number of ratings for an agent",
        responses={200: RatingSerializer()},
    )
    def get(self, request, profile_id):
        agent = get_object_or_404(Profile, id=profile_id)
        queryset = Rating.objects.filter(agent=agent)
        serializer = self.serializer_class(queryset, many=True)
        return CustomResponse.success(
            {"rating_count": len(serializer.data)}, status=200
        )


class GetAgentRatingPercentage(APIView):
    serializer_class = RatingSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Get the percentage of ratings for an agent",
        responses={200: RatingSerializer()},
    )
    def get(self, request, profile_id):
        agent = get_object_or_404(Profile, id=profile_id)
        queryset = Rating.objects.filter(agent=agent)
        serializer = self.serializer_class(queryset, many=True)
        ratings = [rating["rating"] for rating in serializer.data]
        rating_count = len(ratings)
        rating_1 = ratings.count(1)
        rating_2 = ratings.count(2)
        rating_3 = ratings.count(3)
        rating_4 = ratings.count(4)
        rating_5 = ratings.count(5)
        rating_1_percentage = rating_1 / rating_count * 100
        rating_2_percentage = rating_2 / rating_count * 100
        rating_3_percentage = rating_3 / rating_count * 100
        rating_4_percentage = rating_4 / rating_count * 100
        rating_5_percentage = rating_5 / rating_count * 100
        return CustomResponse.success(
            {
                "rating_1_percentage": rating_1_percentage,
                "rating_2_percentage": rating_2_percentage,
                "rating_3_percentage": rating_3_percentage,
                "rating_4_percentage": rating_4_percentage,
                "rating_5_percentage": rating_5_percentage,
            },
            status=200,
        )
