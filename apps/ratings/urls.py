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
    path("agents/<int:profile_id>/reviews/", GetAgentReviews.as_view()),
    path(
        "agents/<int:profile_id>/reviews/<int:review_id>/",
        GetAgentReviewDetail.as_view(),
    ),
    path("agents/<int:profile_id>/reviews/create/", CreateAgentReview.as_view()),
    path(
        "agents/<int:profile_id>/reviews/<int:review_id>/update/",
        UpdateAgentReview.as_view(),
    ),
    path(
        "agents/<int:profile_id>/reviews/<int:review_id>/delete/",
        DeleteAgentReview.as_view(),
    ),
    path("agents/<int:profile_id>/reviews/average/", GetAgentAverageRating.as_view()),
    path(
        "agents/<int:profile_id>/reviews/percentage/",
        GetAgentRatingPercentage.as_view(),
    ),
    path("agents/<int:profile_id>/reviews/count/", GetAgentRatingCount.as_view()),
]
