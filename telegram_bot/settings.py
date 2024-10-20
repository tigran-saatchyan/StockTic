import os


class BotSettings:
    """
    bot_config
    """

    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    TIME_ZONE = os.getenv("TIME_ZONE", "UTC")
