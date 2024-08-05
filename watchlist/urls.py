from django.urls import path

from . import views
from .views import WatchlistTickerDeleteView

app_name = 'watchlist'

urlpatterns = [
    path('', views.watchlist_list, name='watchlist_list'),
    path('<int:pk>/', views.watchlist_detail, name='watchlist_detail'),
    path('create/', views.create_watchlist, name='create_watchlist'),
    path('<int:pk>/add/', views.add_ticker, name='add_ticker'),
    path(
        '<int:watchlist_pk>/delete_ticker/<str:ticker_symbol>/',
        WatchlistTickerDeleteView.as_view(), name='delete_ticker'
        ),
]
