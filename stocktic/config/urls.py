"""This module defines the URL patterns for the Django project, including
admin, app-specific, API, and third-party URLs.

The configuration uses Django's URL dispatcher and includes paths for
various applications and API endpoints.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

API_V1 = "api/v1/"

django_urlpatterns = [
    path("admin/", admin.site.urls),
]

app_urlpatterns = [
    path("tickers/", include("tickers.urls")),
    path("notifications/", include("notifications.urls")),
]
api_urlpatterns = [
    path(API_V1, include("users.urls")),
    path(API_V1, include("notifications.api_urls")),
    path(API_V1, include("tickers.api_urls")),
]

api_token_urlpatterns = [
    path(
        "api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
]
third_party_urlpatterns = []
docs_urlpatterns = [
    path("", include("docs")),
]

urlpatterns = [
    *django_urlpatterns,
    *app_urlpatterns,
    *api_urlpatterns,
    *api_token_urlpatterns,
    *third_party_urlpatterns,
    *docs_urlpatterns,
]

if settings.DEBUG or not settings.TESTING:
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns += debug_toolbar_urls()

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
