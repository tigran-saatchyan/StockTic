"""This module contains handlers for notification-related commands and messages
for the Telegram bot. It includes functions for registering, unregistering,
and retrieving notifications, as well as processing user inputs during these
operations.

The handlers use the aiogram library for Telegram bot interactions and httpx
for making asynchronous HTTP requests to the StockTic API.
"""

import logging

import httpx
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram_bot.services.decorators import require_registration
from telegram_bot.settings import BotSettings as settings
from telegram_bot.states import NotificationStates
from telegram_bot.utils import (
    notification_criteria_keyboard,
    notification_type_keyboard,
)

notification_router = Router()
logger = logging.getLogger(__name__)


@notification_router.message(Command("register_notification"))
@require_registration
async def cmd_register_notification(
    message: types.Message, state: FSMContext
) -> None:
    """Initiates the notification registration process.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    await state.set_state(NotificationStates.waiting_for_ticker)
    await message.answer(
        "Please provide the ticker symbol you want to register "
        "for notifications:"
    )


@notification_router.message(NotificationStates.waiting_for_ticker)
async def process_ticker(message: types.Message, state: FSMContext) -> None:
    """Processes the ticker symbol provided by the user.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    ticker = message.text.upper()
    await state.update_data(ticker=ticker)
    await state.set_state(NotificationStates.waiting_for_value)
    await message.answer(
        "Please provide the notification value (e.g., price at which "
        "you want to be notified):"
    )


@notification_router.message(NotificationStates.waiting_for_value)
async def process_value(message: types.Message, state: FSMContext) -> None:
    """Processes the notification value provided by the user.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    try:
        value = float(message.text)
        logger.debug(f"Received notification value: {value}")
        await state.update_data(notification_value=value)
        await state.set_state(NotificationStates.waiting_for_criteria)
        await message.answer(
            "Please select the notification criteria:",
            reply_markup=notification_criteria_keyboard(),
        )
    except ValueError:
        await message.answer("Invalid value. Please provide a valid number.")


@notification_router.callback_query(
    lambda c: c.data in ["more_than", "less_than"],
    NotificationStates.waiting_for_criteria,
)
async def process_criteria(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    """Processes the notification criteria selected by the user.

    Args:
        callback_query (types.CallbackQuery): The callback query object.
        state (FSMContext): The finite state machine context.
    """
    await state.update_data(notification_criteria=callback_query.data)
    await state.set_state(NotificationStates.waiting_for_type)
    await callback_query.message.answer(
        "Please select the notification type:",
        reply_markup=notification_type_keyboard(),
    )
    await callback_query.answer()


@notification_router.callback_query(
    lambda c: c.data in ["email", "telegram", "all"],
    NotificationStates.waiting_for_type,
)
async def process_type(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    """Processes the notification type selected by the user.

    Args:
        callback_query (types.CallbackQuery): The callback query object.
        state (FSMContext): The finite state machine context.
    """
    await state.update_data(notification_type=callback_query.data)
    data = await state.get_data()

    user_id = data.get("user_id")
    headers = data.get("headers")

    if not user_id or not headers:
        await callback_query.message.answer(
            "User data not found. Please try again."
        )
        return

    async with httpx.AsyncClient() as client:
        try:
            ticker_response = await client.get(
                f"{settings.API_BASE_URL}/tickers/get_by_symbol/",
                params={"symbol": data["ticker"]},
                headers=headers,
            )
            if (
                ticker_response.status_code != 200
                or not ticker_response.json()
            ):
                await callback_query.message.answer(
                    "Ticker not found. Please provide a valid ticker symbol."
                )
                return

            ticker_id = ticker_response.json()["id"]

            response = await client.post(
                f"{settings.API_BASE_URL}/notifications/",
                json={
                    "user": user_id,
                    "ticker": ticker_id,
                    "notification_value": data["notification_value"],
                    "notification_type": data["notification_type"],
                    "notification_criteria": data["notification_criteria"],
                },
                headers=headers,
            )

            if response.status_code == 201:
                await callback_query.message.answer(
                    "Notification registration successful!"
                )
                await state.clear()
            else:
                logger.error(
                    f"Failed to register notification: {response.text}"
                )
                await callback_query.message.answer(
                    "An error occurred. Please try again later."
                )
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {e}")
            await callback_query.message.answer(f"Request error occurred: {e}")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            await callback_query.message.answer(f"HTTP error occurred: {e}")
    await callback_query.answer()


@notification_router.message(Command("unregister_notification"))
@require_registration
async def cmd_unregister_notification(
    message: types.Message, state: FSMContext
) -> None:
    """Initiates the notification unregistration process.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    await state.set_state(NotificationStates.waiting_for_unregistration_ticker)
    await message.answer(
        "Please provide the ticker symbol you want "
        "to unregister from notifications:"
    )


@notification_router.message(
    NotificationStates.waiting_for_unregistration_ticker
)
async def process_ticker_for_unregistration(
    message: types.Message, state: FSMContext
) -> None:
    """Processes the ticker symbol provided by the user for unregistration.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    ticker = message.text.upper()
    await state.update_data(ticker=ticker)
    await state.set_state(NotificationStates.waiting_for_unregistration_value)
    await message.answer(
        "Please provide the notification value "
        "for the ticker you want to unregister:"
    )


@notification_router.message(
    NotificationStates.waiting_for_unregistration_value
)
async def process_value_for_unregistration(
    message: types.Message, state: FSMContext
) -> None:
    """Processes the notification value provided
    by the user for unregistration.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    try:
        value = float(message.text)
        logger.debug(f"Received unregistration value: {value}")
        await state.update_data(notification_value=value)
        await unregister_notification(message, state)
    except ValueError:
        await message.answer("Invalid value. Please provide a valid number.")


async def unregister_notification(
    message: types.Message, state: FSMContext
) -> None:
    """Unregisters the notification for the user.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    data = await state.get_data()

    user_id = data.get("user_id")
    headers = data.get("headers")

    if not user_id or not headers:
        await message.answer("User data not found. Please try again.")
        return

    async with httpx.AsyncClient() as client:
        try:
            ticker_response = await client.get(
                f"{settings.API_BASE_URL}/tickers/get_by_symbol/",
                params={"symbol": data["ticker"]},
                headers=headers,
            )
            if (
                ticker_response.status_code != 200
                or not ticker_response.json()
            ):
                await message.answer(
                    "Ticker not found. Please provide a valid ticker symbol."
                )
                return

            ticker_id = ticker_response.json()["id"]

            notification_response = await client.get(
                f"{settings.API_BASE_URL}/notifications/",
                params={"user": user_id, "ticker": ticker_id},
                headers=headers,
            )

            notifications = notification_response.json()
            correct_notification = next(
                (
                    n
                    for n in notifications
                    if n["notification_value"] == data["notification_value"]
                ),
                None,
            )

            if not correct_notification:
                await message.answer("No matching notification found.")
                return

            notification_id = correct_notification["id"]

            response = await client.delete(
                f"{settings.API_BASE_URL}/notifications/{notification_id}/",
                headers=headers,
            )

            if response.status_code == 204:
                await message.answer("Notification unregistration successful!")
                await state.clear()
            else:
                logger.error(
                    f"Failed to unregister notification: {response.text}"
                )
                await message.answer(
                    "An error occurred. Please try again later."
                )
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {e}")
            await message.answer(f"Request error occurred: {e}")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            await message.answer(f"HTTP error occurred: {e}")


@notification_router.message(Command("get_notifications"))
@require_registration
async def cmd_get_notifications(
    message: types.Message, state: FSMContext
) -> None:
    """Retrieves all notifications registered by the user.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    data = await state.get_data()

    user_id = data.get("user_id")
    headers = data.get("headers")

    if not user_id or not headers:
        await message.answer("User data not found. Please try again.")
        return

    async with httpx.AsyncClient() as client:
        try:
            notification_response = await client.get(
                f"{settings.API_BASE_URL}/notifications/",
                params={"user": user_id},
                headers=headers,
            )

            if (
                notification_response.status_code != 200
                or not notification_response.json()
            ):
                await message.answer("No notifications found.")
                return

            notifications = notification_response.json()
            response_message = "Here are your registered notifications:\n\n"
            for notification in notifications:
                ticker = await get_ticker_by_id(
                    notification["ticker"], headers
                )
                response_message += (
                    f"Ticker: {ticker['symbol']} ({ticker['name']})\n"
                    f"Value: {notification['notification_value']} $\n"
                    f"Type: {notification['notification_type'].title()}\n"
                    f"Criteria: {notification[
                        'notification_criteria'
                    ].replace('_', ' ').title()}\n\n"
                )

            await message.answer(response_message)
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {e}")
            await message.answer(f"Request error occurred: {e}")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            await message.answer(f"HTTP error occurred: {e}")


async def get_ticker_by_id(ticker_id, headers):
    """Fetches ticker information by its ID.

    Args:
        ticker_id (int): The ID of the ticker.
        headers (dict): The headers for the HTTP request.

    Returns:
        dict: The ticker information if found, otherwise None.
    """
    async with httpx.AsyncClient() as client:
        ticker_response = await client.get(
            f"{settings.API_BASE_URL}/tickers/{ticker_id}/", headers=headers
        )
        if ticker_response.status_code == 200:
            return ticker_response.json()
        return None
