"""This module defines the URL patterns for the notifications app.

URL Patterns:
    notification_list: URL pattern for listing notifications.
    notification_add: URL pattern for adding a new notification.
    notification_edit: URL pattern for editing an existing notification.
    notification_delete: URL pattern for deleting a notification.
"""

from django.urls import path

from .views import (
    NotificationCreateView,
    NotificationDeleteView,
    NotificationListView,
    NotificationUpdateView,
)

app_name = "notifications"

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification_list"),
    path("add/", NotificationCreateView.as_view(), name="notification_add"),
    path(
        "edit/<int:pk>/",
        NotificationUpdateView.as_view(),
        name="notification_edit",
    ),
    path(
        "delete/<int:pk>/",
        NotificationDeleteView.as_view(),
        name="notification_delete",
    ),
]
