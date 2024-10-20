"""This module provides services for the Telegram bot, including functions
to start the bot, retrieve JWT tokens, and check user registration status.

The services use the aiogram library for Telegram bot interactions
and httpx for making asynchronous HTTP requests to the StockTic API.
"""

import logging

import httpx
from aiogram import Dispatcher

from telegram_bot.settings import BotSettings as settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start_bot(dp: Dispatcher, bot):
    """Start bot with dispatcher.

    Args:
        dp (Dispatcher): The dispatcher instance.
        bot: The bot instance.
    """
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"An error occurred while polling: {e}")


async def get_jwt_token(telegram_user_id):
    """Get JWT token using Telegram ID.

    Args:
        telegram_user_id (int): The Telegram user ID.

    Returns:
        str: The JWT token if the user is registered, otherwise None.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{settings.API_BASE_URL}/token/by-telegram-id/",
                json={"telegram_user_id": telegram_user_id},
            )
            response.raise_for_status()
            return response.json().get("access")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None  # User not found
            raise e


async def check_user_registration(user_id: int) -> dict:
    """Check if the user is registered in the system.

    Args:
        user_id (int): The Telegram user ID.

    Returns:
        dict: The user data if registered, otherwise None.
    """
    try:
        token = await get_jwt_token(user_id)
        if not token:
            return None

        headers = {"Authorization": f"Bearer {token}"}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.API_BASE_URL}/users/get_by_telegram_id/",
                params={"telegram_user_id": user_id},
                headers=headers,
            )
            if response.status_code == 200 and response.json():
                return response.json()  # Return user data

    except httpx.RequestError as e:
        logger.error(
            f"Request error occurred while checking registration: {e}"
        )
    except httpx.HTTPError as e:
        logger.error(f"HTTP error occurred while checking registration: {e}")

    return None
