import logging

import httpx
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram_bot.settings import BotSettings as settings
from telegram_bot.states import NotificationStates
from telegram_bot.utils import (
    notification_type_keyboard,
    notification_criteria_keyboard,
)

notification_router = Router()
logger = logging.getLogger(__name__)


# Function to get JWT token using Telegram ID
async def get_jwt_token(telegram_user_id):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.API_BASE_URL}/token/by-telegram-id/",
            json={"telegram_user_id": telegram_user_id},
        )
        response.raise_for_status()
        return response.json()["access"]


@notification_router.message(Command("register_notification"))
async def cmd_register_notification(message: types.Message, state: FSMContext) -> None:
    """
    Initiates the notification registration process
    """
    await state.set_state(NotificationStates.waiting_for_ticker)
    await message.answer(
        "Please provide the ticker symbol you want to register for notifications:"
    )


@notification_router.message(NotificationStates.waiting_for_ticker)
async def process_ticker(message: types.Message, state: FSMContext) -> None:
    """
    Process the ticker symbol provided by the user
    """
    ticker = message.text.upper()
    await state.update_data(ticker=ticker)
    await state.set_state(NotificationStates.waiting_for_value)
    await message.answer(
        "Please provide the notification value (e.g., price at which you want to be notified):"
    )


@notification_router.message(NotificationStates.waiting_for_value)
async def process_value(message: types.Message, state: FSMContext) -> None:
    """
    Process the notification value provided by the user
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
    """
    Process the notification criteria selected by the user
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
async def process_type(callback_query: types.CallbackQuery, state: FSMContext) -> None:
    """
    Process the notification type selected by the user
    """
    await state.update_data(notification_type=callback_query.data)
    data = await state.get_data()

    # Log the data being sent to the API
    logger.debug(f"Registering notification with data: {data}")

    async with httpx.AsyncClient() as client:
        try:
            # Obtain JWT token
            token = await get_jwt_token(callback_query.from_user.id)

            headers = {"Authorization": f"Bearer {token}"}

            # Retrieve user ID based on telegram_user_id
            user_response = await client.get(
                f"{settings.API_BASE_URL}/users/get_by_telegram_id/",
                params={"telegram_user_id": callback_query.from_user.id},
                headers=headers,
            )
            if user_response.status_code != 200 or not user_response.json():
                await callback_query.message.answer(
                    "User not found. Please register first."
                )
                return
            user_id = user_response.json()["id"]

            # Retrieve ticker ID based on ticker symbol
            ticker_response = await client.get(
                f"{settings.API_BASE_URL}/tickers/get_by_symbol/",
                params={"symbol": data["ticker"]},
                headers=headers,
            )
            if ticker_response.status_code != 200 or not ticker_response.json():
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
            logger.debug(f"API response: {response.status_code} - {response.text}")
            if response.status_code == 201:
                await callback_query.message.answer(
                    "Notification registration successful!"
                )
                await state.clear()
            else:
                logger.error(f"Failed to register notification: {response.text}")
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
async def cmd_unregister_notification(
    message: types.Message, state: FSMContext
) -> None:
    """
    Initiates the notification unregistration process
    """
    await state.set_state(NotificationStates.waiting_for_unregistration_ticker)
    await message.answer(
        "Please provide the ticker symbol you want to unregister from notifications:"
    )


@notification_router.message(NotificationStates.waiting_for_unregistration_ticker)
async def process_ticker_for_unregistration(
    message: types.Message, state: FSMContext
) -> None:
    """
    Process the ticker symbol provided by the user for unregistration
    """
    ticker = message.text.upper()
    await state.update_data(ticker=ticker)
    await state.set_state(NotificationStates.waiting_for_unregistration_value)
    await message.answer(
        "Please provide the notification value for the ticker you want to unregister:"
    )


@notification_router.message(NotificationStates.waiting_for_unregistration_value)
async def process_value_for_unregistration(
    message: types.Message, state: FSMContext
) -> None:
    """
    Process the notification value provided by the user for unregistration
    """
    try:
        value = float(message.text)
        logger.debug(f"Received unregistration value: {value}")
        await state.update_data(notification_value=value)
        await unregister_notification(message, state)
    except ValueError:
        await message.answer("Invalid value. Please provide a valid number.")


async def unregister_notification(message: types.Message, state: FSMContext) -> None:
    data = await state.get_data()

    async with httpx.AsyncClient() as client:
        try:
            # Obtain JWT token
            token = await get_jwt_token(message.from_user.id)

            headers = {"Authorization": f"Bearer {token}"}

            # Retrieve user ID based on telegram_user_id
            user_response = await client.get(
                f"{settings.API_BASE_URL}/users/get_by_telegram_id/",
                params={"telegram_user_id": message.from_user.id},
                headers=headers,
            )
            if user_response.status_code != 200 or not user_response.json():
                await message.answer("User not found. Please register first.")
                return
            user_id = user_response.json()["id"]

            # Retrieve ticker ID based on ticker symbol
            ticker_response = await client.get(
                f"{settings.API_BASE_URL}/tickers/get_by_symbol/",
                params={"symbol": data["ticker"]},
                headers=headers,
            )
            if ticker_response.status_code != 200 or not ticker_response.json():
                await message.answer(
                    "Ticker not found. Please provide a valid ticker symbol."
                )
                return
            ticker_id = ticker_response.json()["id"]

            # Get notifications for the user and ticker
            notification_response = await client.get(
                f"{settings.API_BASE_URL}/notifications/",
                params={"user": user_id, "ticker": ticker_id},
                headers=headers,
            )
            if (
                notification_response.status_code != 200
                or not notification_response.json()
            ):
                await message.answer(
                    "Notification not found. Please provide a valid ticker symbol and value."
                )
                return

            # Ensure we get the correct notification by filtering with notification_value
            notifications = notification_response.json()
            correct_notification = None
            for notification in notifications:
                if (
                    notification["ticker"] == ticker_id
                    and notification["notification_value"] == data["notification_value"]
                ):
                    correct_notification = notification
                    break

            if not correct_notification:
                await message.answer("No matching notification found.")
                return

            notification_id = correct_notification["id"]

            response = await client.delete(
                f"{settings.API_BASE_URL}/notifications/{notification_id}/",
                headers=headers,
            )
            logger.debug(f"API response: {response.status_code} - {response.text}")
            if response.status_code == 204:
                await message.answer("Notification unregistration successful!")
                await state.clear()
            else:
                logger.error(f"Failed to unregister notification: {response.text}")
                await message.answer("An error occurred. Please try again later.")
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {e}")
            await message.answer(f"Request error occurred: {e}")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            await message.answer(f"HTTP error occurred: {e}")


@notification_router.message(Command("get_notifications"))
async def cmd_get_notifications(message: types.Message, state: FSMContext) -> None:
    """
    Retrieve all notifications registered by the user
    """
    async with httpx.AsyncClient() as client:
        try:
            # Obtain JWT token
            token = await get_jwt_token(message.from_user.id)

            headers = {"Authorization": f"Bearer {token}"}

            # Retrieve user ID based on telegram_user_id
            user_response = await client.get(
                f"{settings.API_BASE_URL}/users/get_by_telegram_id/",
                params={"telegram_user_id": message.from_user.id},
                headers=headers,
            )
            if user_response.status_code != 200 or not user_response.json():
                await message.answer("User not found. Please register first.")
                return
            user_id = user_response.json()["id"]

            # Get all notifications for the user
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

            # Process and display the notifications
            notifications = notification_response.json()
            response_message = "Here are your registered notifications:\n\n"
            for notification in notifications:
                ticker = await get_ticker_by_id(notification["ticker"], headers)
                response_message += (
                    f"Ticker: {ticker['symbol']} ({ticker['name']})\n"
                    f"Value: {notification['notification_value']} $\n"
                    f"Type: {notification['notification_type'].title()}\n"
                    f"Criteria: {notification['notification_criteria'].replace("_", " ").title()}\n\n"
                )

            await message.answer(response_message)
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {e}")
            await message.answer(f"Request error occurred: {e}")
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            await message.answer(f"HTTP error occurred: {e}")


async def get_ticker_by_id(ticker_id, headers):
    async with httpx.AsyncClient() as client:
        ticker_response = await client.get(
            f"{settings.API_BASE_URL}/tickers/{ticker_id}/", headers=headers
        )
        if ticker_response.status_code == 200:
            return ticker_response.json()
        return None
