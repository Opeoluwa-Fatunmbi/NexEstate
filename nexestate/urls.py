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
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/properties/", include("apps.properties.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    # path("api/v1/chats/", include("apps.chats.urls")),
    path("api/v1/payments/", include("apps.payments.urls")),
    # path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    path("api/v1/reports/", include("apps.reports.urls")),
    # path("api/v1/analytics/", include("apps.analytics.urls")),
    path("api/v1/enquiries/", include("apps.enquiries.urls")),
    path("api/v1/ratings/", include("apps.ratings.urls")),
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
