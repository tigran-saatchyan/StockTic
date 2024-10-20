"""This module defines the configuration for the Users app.

Classes:
    UsersConfig: Configuration class for the Users app.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration class for the Users app.

    Attributes:
        default_auto_field (str): The default auto field type for the app.
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
