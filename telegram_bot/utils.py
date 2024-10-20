import httpx
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from django.conf import settings


def notification_type_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Email", callback_data="email"),
                InlineKeyboardButton(text="Telegram", callback_data="telegram"),
                InlineKeyboardButton(text="All", callback_data="all"),
            ]
        ]
    )
    return keyboard


def notification_criteria_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="More than", callback_data="more_than"),
                InlineKeyboardButton(text="Less than", callback_data="less_than"),
            ]
        ]
    )
    return keyboard


def send_telegram_message(telegram_user_id, message):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": telegram_user_id, "text": message}
    httpx.post(url, params=params)
