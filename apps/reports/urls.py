from django.urls import path
from apps.reports.views import PropertyValuationReportView

app_name = "reports"

urlpatterns = [
    path(
        "<slug:property_slug>/valuation-report/",
        PropertyValuationReportView.as_view(),
        name="generate-property-valuation-report",
    ),
]
