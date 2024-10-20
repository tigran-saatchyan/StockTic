"""This module initializes the Telegram bot instance.

Attributes:
    TELEGRAM_BOT_TOKEN (str): The token for the Telegram bot.
    bot (Bot): The instance of the Telegram bot.
"""

import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(
    token=TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML")
)
