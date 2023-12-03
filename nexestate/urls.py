# Description: Main URL configuration for the project.
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("apps.accounts.urls")),
    path("properties/", include("apps.properties.urls")),
    # path("chats/", include("apps.chats.urls")),
    # path("payments/", include("apps.payments.urls")),
    # path("notifications/", include("apps.notifications.urls")),
    path("profiles/", include("apps.profiles.urls")),
    # path("reports/", include("apps.reports.urls")),
    # path("analytics/", include("apps.analytics.urls")),
    path("enquiries/", include("apps.enquiries.urls")),
    path("ratings/", include("apps.ratings.urls")),
    # drf-spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # django-debug-toolbar
    path("__debug__/", include(debug_toolbar.urls)),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
