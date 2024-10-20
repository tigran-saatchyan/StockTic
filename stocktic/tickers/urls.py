# tickers/urls.py
from django.urls import path

from . import views
from .views import FetchTickersAsyncView

app_name = "tickers"

urlpatterns = [
    path("", views.ticker_list, name="ticker_list"),
    path("search/", views.search_tickers, name="search_tickers"),
    path("export/", views.export_tickers, name="export_tickers"),
    path("import/", views.import_tickers, name="import_tickers"),
    path("<str:symbol>/", views.get_stock_info, name="ticker_detail"),
    path("<str:symbol>/history/", views.get_stock_history, name="ticker_history"),
    path(
        "fetch-tickers-async/",
        FetchTickersAsyncView.as_view(),
        name="fetch-tickers-async",
    ),
]
