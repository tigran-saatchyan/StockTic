"""This module defines the settings for the Telegram bot.

Classes:
    BotSettings: A class to hold the settings for the Telegram bot.
"""

import os


class BotSettings:
    """A class to hold the settings for the Telegram bot.

    Attributes:
        API_BASE_URL (str): The base URL for the API.
        TIME_ZONE (str): The time zone for the bot.
    """

    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
