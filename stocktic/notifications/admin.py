"""This module registers the Notification model with the Django admin site.

Admin:
    NotificationAdmin: Custom admin interface for the Notification model.
"""

from django.contrib import admin

from notifications.models import Notification

# Register your models here.
admin.register(Notification)
