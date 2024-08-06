# historical_data/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<str:ticker>/', views.historical_data_view, name='historical_data_view'),
]
