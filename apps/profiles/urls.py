from django.urls import path
from apps.profiles.views import (
    AgentListView,
    TopAgentsListView,
    GetProfileView,
    UpdateProfileView,
)

app_name = "profiles"

urlpatterns = [
    path("agents/", AgentListView.as_view(), name="agents"),
    path("top-agents/", TopAgentsListView.as_view(), name="top_agents"),
    path("profile/", GetProfileView.as_view(), name="profiles"),
    path("update-profile/", UpdateProfileView.as_view(), name="update_profile"),
]
