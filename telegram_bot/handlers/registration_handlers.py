"""This module contains handlers for user registration commands and messages
for the Telegram bot. It includes functions for initiating the registration
process, processing user-provided email and telephone number, and verifying
the collected information.

The handlers use the aiogram library for Telegram bot interactions, httpx
for making asynchronous HTTP requests to the StockTic API, and Django's
validators for validating email addresses.
"""

import logging
import re

import httpx
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from django.core import validators
from django.core.exceptions import ValidationError

from telegram_bot.services.bot_service import get_jwt_token
from telegram_bot.settings import BotSettings as settings
from telegram_bot.states import RegistrationStates

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

registration_router = Router()


@registration_router.message(Command("register"))
async def cmd_register(message: types.Message, state: FSMContext) -> None:
    """Initiates the user registration process.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    telegram_user_id = message.from_user.id

    # Check if the user is already registered by attempting to get a JWT token
    token = await get_jwt_token(telegram_user_id)

    if token:
        # User is already registered
        await message.answer("You are already registered.")
        return

    await state.set_state(RegistrationStates.waiting_for_email)
    await message.answer("Please provide your email address:")


@registration_router.message(RegistrationStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext) -> None:
    """Processes the email address provided by the user.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    email = message.text
    try:
        validators.validate_email(email)
        await state.update_data(email=email)
        await state.set_state(RegistrationStates.waiting_for_telephone)
        await message.answer("Please provide your telephone number:")
    except ValidationError:
        await message.answer(
            "Invalid email address. Please provide a valid email address."
        )


@registration_router.message(RegistrationStates.waiting_for_telephone)
async def process_telephone(message: types.Message, state: FSMContext) -> None:
    """Processes the telephone number provided by the user.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    telephone = message.text.strip()
    if re.match(r"^\+?1?\d{9,15}$", telephone):
        await state.update_data(telephone=telephone)
        await state.set_state(RegistrationStates.waiting_for_verification)
        await message.answer(
            "Is your information correct? "
            'Type "yes" to confirm or "no" to restart.'
        )
    else:
        await message.answer(
            "Invalid telephone number. "
            "Please provide a valid telephone number."
        )


@registration_router.message(RegistrationStates.waiting_for_verification)
async def process_verification(
    message: types.Message, state: FSMContext
) -> None:
    """Processes the verification provided by the user.

    Args:
        message (types.Message): The message object from the user.
        state (FSMContext): The finite state machine context.
    """
    logger.info(
        "Starting verification process for user: %s", message.from_user.id
    )

    if message.text.lower() == "yes":
        data = await state.get_data()
        logger.info("Collected data from state: %s", data)

        async with httpx.AsyncClient() as client:
            try:
                logger.info(
                    "Sending POST request to %s",
                    f"{settings.API_BASE_URL}/users/",
                )

                response = await client.post(
                    f"{settings.API_BASE_URL}/users/",
                    json={
                        "email": data["email"],
                        "telephone": data["telephone"],
                        "telegram_user_id": message.from_user.id,
                        "password": "defaultpassword",
                    },
                )

                logger.info("Received response: %s", response.status_code)

                if response.status_code == 201:
                    logger.info("User registration successful")
                    await message.answer(
                        f"Registration successful! "
                        f"Welcome {message.from_user.full_name}!"
                    )
                    await state.clear()
                elif response.status_code == 400:
                    logger.info("Email already registered")
                    await message.answer(
                        "This email is already registered. "
                        "Please try with a different email."
                    )
                    await state.clear()
                else:
                    logger.error(
                        "Unexpected response: %s", response.status_code
                    )
                    await message.answer(
                        "An error occurred. Please try again later."
                    )

            except httpx.RequestError as e:
                logger.error("Request error occurred: %s", e)
                await message.answer(f"Request error occurred: {e}")

            except httpx.HTTPError as e:
                logger.error("HTTP error occurred: %s", e)
                await message.answer(f"HTTP error occurred: {e}")
    else:
        logger.info("User cancelled the registration process")
        await state.clear()
        await message.answer(
            "Registration cancelled. "
            "You can start over by typing /register."
        )
