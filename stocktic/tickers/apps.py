"""This module defines the configuration for the Tickers app.

Classes:
    TickersConfig: Configuration class for the Tickers app.
"""

from django.apps import AppConfig


class TickersConfig(AppConfig):
    """Configuration class for the Tickers app.

    Attributes:
        default_auto_field (str): The default auto field type for models
            in this app.
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "tickers"
