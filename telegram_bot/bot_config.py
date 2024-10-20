"""This module defines the configuration for the Telegram bot.

Classes:
    BotConfig: A class to hold the bot configuration.
"""


class BotConfig:
    """A class to hold the bot configuration.

    Attributes:
        admin_ids (list): A list of admin user IDs.
        welcome_message (str): The welcome message for the bot.
    """

    def __init__(self, admin_ids, welcome_message) -> None:
        """Initializes the BotConfig class with admin IDs and a
        welcome message.

        Args:
            admin_ids (list): A list of admin user IDs.
            welcome_message (str): The welcome message for the bot.
        """
        self.admin_ids = admin_ids
        self.welcome_message = welcome_message
