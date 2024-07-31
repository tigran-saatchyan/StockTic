import re

import httpx
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError

from telegram_bot.states import RegistrationStates

# Ensure this URL matches your Django server's API endpoint

registration_router = Router()


@registration_router.message(Command('register'))
async def cmd_register(message: types.Message, state: FSMContext) -> None:
    """
    Initiates the user registration process
    """
    await state.set_state(RegistrationStates.waiting_for_email)
    await message.answer('Please provide your email address:')


@registration_router.message(RegistrationStates.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext) -> None:
    """
    Process the email address provided by the user
    """
    email = message.text
    try:
        validators.validate_email(email)
        await state.update_data(email=email)
        await state.set_state(RegistrationStates.waiting_for_telephone)
        await message.answer('Please provide your telephone number:')
    except ValidationError:
        await message.answer(
            'Invalid email address. Please provide a valid email address.'
        )


@registration_router.message(RegistrationStates.waiting_for_telephone)
async def process_telephone(message: types.Message, state: FSMContext) -> None:
    """
    Process the telephone number provided by the user
    """
    telephone = message.text.strip()
    if re.match(r"^\+?1?\d{9,15}$", telephone):
        await state.update_data(telephone=telephone)
        await state.set_state(RegistrationStates.waiting_for_verification)
        await message.answer(
            'Is your information correct? Type "yes" to confirm or "no" to restart.'
        )
    else:
        await message.answer(
            'Invalid telephone number. Please provide a valid telephone number.'
        )


@registration_router.message(RegistrationStates.waiting_for_verification)
async def process_verification(
    message: types.Message, state: FSMContext
) -> None:
    """
    Process the verification provided by the user
    """
    if message.text.lower() == 'yes':
        data = await state.get_data()
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.API_BASE_URL}/users/",
                    json={
                        "email": data['email'],
                        "telephone": data['telephone'],
                        "telegram_user_id": message.from_user.id,
                        "password": "defaultpassword"
                    }
                )
                if response.status_code == 201:
                    await message.answer(
                        f'Registration successful! Welcome {message.from_user.full_name}!'
                    )
                    await state.clear()
                elif response.status_code == 400:
                    await message.answer(
                        'This email is already registered. Please try with a different email.'
                    )
                    await state.clear()
                else:
                    await message.answer(
                        'An error occurred. Please try again later.'
                    )
            except httpx.RequestError as e:
                await message.answer(f"Request error occurred: {e}")
            except httpx.HTTPError as e:
                await message.answer(f"HTTP error occurred: {e}")
    else:
        await state.clear()
        await message.answer(
            'Registration cancelled. You can start over by typing /register.'
        )
