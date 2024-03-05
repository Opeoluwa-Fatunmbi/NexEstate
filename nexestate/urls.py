from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from apps.common.responses import CustomResponse
from drf_spectacular.utils import extend_schema
from adrf.views import APIView


class HealthCheckView(APIView):
    @extend_schema(
        "/",
        summary="API Health Check",
        description="This endpoint checks the health of the API",
    )
    async def get(self, request):
        return CustomResponse.success(message="pong")


def handler404(request, exception=None):
    response = JsonResponse({"status": "failure", "message": "Not Found"})
    response.status_code = 404
    return response


def handler500(request, exception=None):
    response = JsonResponse({"status": "failure", "message": "Server Error"})
    response.status_code = 500
    return response


handler404 = handler404
handler500 = handler500

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path("api/v1/properties/", include("apps.properties.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    path("api/v1/payments/", include("apps.payments.urls")),
    path("api/v1/profiles/", include("apps.profiles.urls")),
    path("api/v1/reports/", include("apps.reports.urls")),
    path("api/v1/enquiries/", include("apps.enquiries.urls")),
    path("api/v1/ratings/", include("apps.ratings.urls")),
    # Health check
    path("api/v1/healthcheck/", HealthCheckView.as_view()),
    # DOCUMENTATION
    # drf-spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "",
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

# Serving static and media files with NGINX for performance and security

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


