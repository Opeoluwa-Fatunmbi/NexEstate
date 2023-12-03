from django.urls import path
from apps.ratings.views import CreateAgentReview

app_name = "ratings"


urlpatterns = [
    path("create/<int:profile_id>/", CreateAgentReview.as_view(), name="create"),
]
