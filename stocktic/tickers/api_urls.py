from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api import TickerViewSet, FetchTickersAPIView

router = DefaultRouter()
router.register(r"tickers", TickerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("fetch-tickers/", FetchTickersAPIView.as_view(), name="fetch-tickers"),
]
