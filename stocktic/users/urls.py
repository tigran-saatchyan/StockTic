"""This module defines the URL patterns for the Users app.

Functions:
    urlpatterns: A list of URL patterns for the Users app.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import UserViewSet, get_token_by_telegram_id

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path(
        "token/by-telegram-id/",
        get_token_by_telegram_id,
        name="token_by_telegram_id",
    ),
    path("", include(router.urls)),
]
