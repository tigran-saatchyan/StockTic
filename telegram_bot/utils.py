"""This module provides utility functions for the Telegram bot.

Functions:
    notification_type_keyboard: Returns an inline keyboard for
        notification type selection.
    notification_criteria_keyboard: Returns an inline keyboard for
        notification criteria selection.
    send_telegram_message: Sends a message to a Telegram user.
"""

import httpx
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings


def notification_type_keyboard():
    """Returns an inline keyboard for notification type selection.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup for
            notification type selection.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Email", callback_data="email"),
                InlineKeyboardButton(
                    text="Telegram", callback_data="telegram"
                ),
                InlineKeyboardButton(text="All", callback_data="all"),
            ]
        ]
    )


def notification_criteria_keyboard():
    """Returns an inline keyboard for notification criteria selection.

    Returns:
        InlineKeyboardMarkup: The inline keyboard markup for notification
            criteria selection.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="More than", callback_data="more_than"
                ),
                InlineKeyboardButton(
                    text="Less than", callback_data="less_than"
                ),
            ]
        ]
    )


def send_telegram_message(telegram_user_id, message):
    """Sends a message to a Telegram user.

    Args:
        telegram_user_id (int): The Telegram user ID to send the message to.
        message (str): The message to be sent.

    Returns:
        None
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": telegram_user_id, "text": message}
    httpx.post(url, params=params)
