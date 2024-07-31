from django.urls import path
from . import views

app_name = 'watchlist'

urlpatterns = [
    path('', views.watchlist_list, name='watchlist_list'),
    path('<int:pk>/', views.watchlist_detail, name='watchlist_detail'),
    path('create/', views.create_watchlist, name='create_watchlist'),
    path('<int:pk>/add/', views.add_ticker, name='add_ticker'),
]
