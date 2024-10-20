"""This module defines the URL patterns for the Tickers API.

Functions:
    urlpatterns: A list of URL patterns for the Tickers API.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api import FetchTickersAPIView, TickerViewSet

router = DefaultRouter()
router.register(r"tickers", TickerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "fetch-tickers/", FetchTickersAPIView.as_view(), name="fetch-tickers"
    ),
]
