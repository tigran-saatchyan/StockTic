"""This module defines the URL patterns for the notifications API.

URL Patterns:
    urlpatterns: A list of URL patterns for the notifications API, including
        the NotificationViewSet.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import NotificationViewSet

router = DefaultRouter()
router.register(r"notifications", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", include(router.urls)),
]
