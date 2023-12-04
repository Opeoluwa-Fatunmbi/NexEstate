from django.urls import path
from apps.ratings.views import (
    CreateAgentReview,
    DeleteAgentReview,
    UpdateAgentReview,
    GetAgentAverageRating,
    GetAgentReviews,
    GetAgentRatingPercentage,
    GetAgentRatingCount,
    GetAgentReviewDetail,
)

app_name = "ratings"


urlpatterns = [
    path("agents/<uuid:profile_id>/reviews/", GetAgentReviews.as_view()),
    path(
        "agents/<uuid:profile_id>/reviews/<uuid:review_id>/",
        GetAgentReviewDetail.as_view(),
    ),
    path(
        "agents/<uuid:profile_id>/reviews/<uuid:review_id>/",
        UpdateAgentReview.as_view(),
    ),
    path(
        "agents/<uuid:profile_id>/reviews/<uuid:review_id>/",
        DeleteAgentReview.as_view(),
    ),
    path("agents/<uuid:profile_id>/reviews/", CreateAgentReview.as_view()),
    path("agents/<uuid:profile_id>/average_rating/", GetAgentAverageRating.as_view()),
    path(
        "agents/<uuid:profile_id>/rating_percentage/",
        GetAgentRatingPercentage.as_view(),
    ),
    path("agents/<uuid:profile_id>/rating_count/", GetAgentRatingCount.as_view()),
]
