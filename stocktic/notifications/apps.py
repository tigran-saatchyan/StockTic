"""This module defines the configuration for the notification's app.

Classes:
    NotificationsConfig: Configuration class for the notification's app.
"""

from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Configuration class for the notification's app.

    Attributes:
        default_auto_field (str): The default auto field type for models
            in the app.
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "notifications"
