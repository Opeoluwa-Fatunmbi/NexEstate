from django.urls import path
from apps.enquiries.views import (
    CreateEnquiryView,
    GetEnquiriesView,
    GetAnsweredEnquiriesView,
    GetUnAnsweredEnquiriesView,
    DeleteEnquiryView,
    GetEnquiryDetailView,
)

app_name = "enquiries"

urlpatterns = [
    path("create/", CreateEnquiryView.as_view(), name="create-enquiry"),
    path("get/", GetEnquiriesView.as_view(), name="get-enquiries"),
    path(
        "get/answered/",
        GetAnsweredEnquiriesView.as_view(),
        name="get-answered-enquiries",
    ),
    path(
        "get/unanswered/",
        GetUnAnsweredEnquiriesView.as_view(),
        name="get-unanswered-enquiries",
    ),
    path("get/<slug:slug>/", GetEnquiryDetailView.as_view(), name="get-enquiry-detail"),
    path("delete/<slug:slug>/", DeleteEnquiryView.as_view(), name="delete-enquiry"),
]
