"""This module provides a decorator to ensure that a user is registered before
allowing access to certain handlers in the Telegram bot.

The decorator uses the aiogram library for Telegram bot interactions and
httpx for making asynchronous HTTP requests to the StockTic API.
"""

from functools import wraps

import httpx
from aiogram import types
from aiogram.fsm.context import FSMContext

from telegram_bot.services.bot_service import get_jwt_token
from telegram_bot.settings import BotSettings as settings


def require_registration(handler):
    """Decorator to ensure the user is registered before accessing the handler.

    Args:
        handler (Callable): The handler function to be decorated.

    Returns:
        Callable: The wrapped handler function.
    """

    @wraps(handler)
    async def wrapper(
        message: types.Message, state: FSMContext, *args, **kwargs
    ):
        """Wrapper function to check user registration.

        Args:
            message (types.Message): The message object from the user.
            state (FSMContext): The finite state machine context.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Callable: The original handler function if the user is registered,
                      otherwise None.
        """
        user_id = message.from_user.id

        # Get JWT token
        token = await get_jwt_token(user_id)
        if not token:
            await message.answer(
                "You are not registered. Please register first."
            )
            return None

        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            try:
                user_response = await client.get(
                    f"{settings.API_BASE_URL}/users/get_by_telegram_id/",
                    params={"telegram_user_id": user_id},
                    headers=headers,
                )
                if (
                    user_response.status_code != 200
                    or not user_response.json()
                ):
                    await message.answer(
                        "User not found. Please register first."
                    )
                    return None

                user_data = user_response.json()
                # Save data in FSMContext
                await state.update_data(
                    user_id=user_data["id"], token=token, headers=headers
                )
            except httpx.RequestError as e:
                await message.answer(f"Request error occurred: {e}")
                return None
            except httpx.HTTPError as e:
                await message.answer(f"HTTP error occurred: {e}")
                return None

        return await handler(message, state, *args, **kwargs)

    return wrapper
