# finance_reports/urls.py

from django.urls import path

from . import views

app_name = 'finance_reports'

urlpatterns = [
    path('', views.index, name='index'),

    # Income URLs
    path('income/add/', views.add_income, name='add_income'),
    path('income/<int:pk>/edit/', views.edit_income, name='edit_income'),
    path('income/<int:pk>/delete/', views.delete_income, name='delete_income'),

    # Expense URLs
    path('expense/add/', views.add_expense, name='add_expense'),
    path('expense/<int:pk>/edit/', views.edit_expense, name='edit_expense'),
    path(
        'expense/<int:pk>/delete/', views.delete_expense, name='delete_expense'
    ),

    # Asset URLs
    path('asset/add/', views.add_asset, name='add_asset'),
    path('asset/<int:pk>/edit/', views.edit_asset, name='edit_asset'),
    path('asset/<int:pk>/delete/', views.delete_asset, name='delete_asset'),

    # Liability URLs
    path('liability/add/', views.add_liability, name='add_liability'),
    path(
        'liability/<int:pk>/edit/', views.edit_liability, name='edit_liability'
    ),
    path(
        'liability/<int:pk>/delete/', views.delete_liability,
        name='delete_liability'
    ),

    # Category URLs
    path('categories/', views.manage_categories, name='manage_categories'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path(
        'category/<int:pk>/delete/', views.delete_category,
        name='delete_category'
    ),
]
