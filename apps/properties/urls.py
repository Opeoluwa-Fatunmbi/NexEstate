from django.urls import path
from apps.properties.views import (
    ListAllPropertiesAPIView,
    ListAgentsPropertiesAPIView,
    # PropertyDetailView,
    UpdatePropertyView,
    DeletePropertyView,
    CreatePropertyView,
    UploadPropertyImageView,
    PropertySearchAPIView,
    PropertyTaxAPIView,
    AddToFavouritesView,
    DeletePropertyFromFavouritesView,
    ListFavoritePropertiesAPIView,
    SmartSearchView,
)

app_name = "properties"


urlpatterns = [
    path("", ListAllPropertiesAPIView.as_view(), name="list"),
    path("agents/", ListAgentsPropertiesAPIView.as_view(), name="agents"),
    path("search/", PropertySearchAPIView.as_view(), name="search"),
    # path("<slug:slug>/", PropertyDetailView.as_view(), name="detail"),
    path("<slug:slug>/update/", UpdatePropertyView.as_view(), name="update"),
    path("<slug:slug>/delete/", DeletePropertyView.as_view(), name="delete"),
    path("create/", CreatePropertyView.as_view(), name="create"),
    path("<slug:slug>/upload/", UploadPropertyImageView.as_view(), name="upload"),
    path("tax/", PropertyTaxAPIView.as_view(), name="tax"),
    path(
        "<slug:slug>/add-to-favorites/",
        AddToFavouritesView.as_view(),
        name="add-to-favorites",
    ),
    path(
        "<slug:slug>/remove-from-favorites/",
        DeletePropertyFromFavouritesView.as_view(),
        name="remove-from-favorites",
    ),
    path(
        "favorites/",
        ListFavoritePropertiesAPIView.as_view(),
        name="list-favorites",
    ),
    path("smart-search/", SmartSearchView.as_view(), name="smart-search"),
]
