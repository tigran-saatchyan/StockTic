from django.urls import path

from .views import (
    NotificationListView,
    NotificationCreateView,
    NotificationUpdateView,
    NotificationDeleteView,
)

app_name = "notifications"

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification_list"),
    path("add/", NotificationCreateView.as_view(), name="notification_add"),
    path("edit/<int:pk>/", NotificationUpdateView.as_view(), name="notification_edit"),
    path(
        "delete/<int:pk>/", NotificationDeleteView.as_view(), name="notification_delete"
    ),
]
