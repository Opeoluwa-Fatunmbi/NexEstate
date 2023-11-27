from django.urls import path
from apps.properties.views import (
    PropertyListAPIView,
    ListAgentsPropertiesView,
    PropertyDetailView,
    UpdatePropertyView,
    DeletePropertyView,
    CreatePropertyView,
    UploadPropertyImageView,
    PropertySearchAPIView,
    PropertyTaxAPIView,
)

app_name = "properties"


urlpatterns = [
    path("", PropertyListAPIView.as_view(), name="list"),
    path("agents/", ListAgentsPropertiesView.as_view(), name="agents"),
    path("search/", PropertySearchAPIView.as_view(), name="search"),
    path("<slug:slug>/", PropertyDetailView.as_view(), name="detail"),
    path("<slug:slug>/update/", UpdatePropertyView.as_view(), name="update"),
    path("<slug:slug>/delete/", DeletePropertyView.as_view(), name="delete"),
    path("create/", CreatePropertyView.as_view(), name="create"),
    path("<slug:slug>/upload/", UploadPropertyImageView.as_view(), name="upload"),
    path("tax/", PropertyTaxAPIView.as_view(), name="tax"),
]
