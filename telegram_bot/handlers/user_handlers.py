import re

import httpx
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text, Bold, Italic
from bot_config import BotConfig
from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError

from telegram_bot.states import TickerStates, RegistrationStates
from tickers.services import Finance

user_router = Router()


@user_router.message(Command('start'))
async def cmd_start(message: types.Message, config: BotConfig) -> None:
    """
    This handler will be called when user sends `/start` command
    """
    content = Text(
        'Hello! ',
        Bold(message.from_user.full_name),
        '\n',
        Italic(config.welcome_message),
    )
    await message.answer(
        **content.as_kwargs()
    )


@user_router.message(Command('register'))
async def cmd_register(message: types.Message, state: FSMContext) -> None:
    """
    Initiates the user registration process
    """
    await state.set_state(RegistrationStates.waiting_for_email)
    await message.answer('Please provide your email address:')


@user_router.message(RegistrationStates.waiting_for_email)
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


@user_router.message(RegistrationStates.waiting_for_telephone)
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


@user_router.message(RegistrationStates.waiting_for_verification)
async def process_verification(
    message: types.Message, state: FSMContext
) -> None:
    """
    Process the verification provided by the user
    """
    if message.text.lower() == 'yes':
        data = await state.get_data()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.API_BASE_URL}/users/", json={
                    "email": data['email'],
                    "telephone": data['telephone'],
                    "telegram_user_id": message.from_user.id,
                    "password": "defaultpassword"
                    # Set a default password, or ask the user to provide one
                }
            )
            print(response.status_code)
            if response.status_code == 201:
                await message.answer('Registration successful! Welcome!')
                await state.clear()
            elif response.status_code == 400:
                await message.answer(
                    'This email is already registered. Please try with a different email.'
                )
                await state.clear()
            else:
                print(response.status_code)
                await message.answer(
                    'An error occurred. Please try again later.'
                )
    else:
        await state.clear()
        await message.answer(
            'Registration cancelled. You can start over by typing /register.'
        )


@user_router.message(Command('ticker_info'))
async def cmd_ticker_info(message: types.Message, state: FSMContext) -> None:
    """
    This handler will be called when user sends `/ticker_info` command
    """
    await state.set_state(TickerStates.waiting_for_ticker_info)
    await message.answer('Please provide a ticker symbol:')


@user_router.message(TickerStates.waiting_for_ticker_info)
async def process_ticker_info(
    message: types.Message, state: FSMContext, config: BotConfig
) -> None:
    """
    This handler will process the ticker symbol provided by the user
    """
    ticker = message.text.upper()
    finance = Finance(ticker)
    info = finance.get_info()
    if info:
        response = (
            f"Ticker Information for {ticker}:\n"
            f"Name: {info.get('longName', 'N/A')}\n"
            f"Sector: {info.get('sector', 'N/A')}\n"
            f"Industry: {info.get('industry', 'N/A')}\n"
            f"Price: {info.get('previousClose', 'N/A')}\n"
            f"Market Cap: {info.get('marketCap', 'N/A')}\n"
            f"PE Ratio: {finance.get_pe_ratio()}\n"
            f"EPS: {finance.get_eps()}\n"
            f"Dividend Yield: {finance.get_dividend_yield()}\n"
            f"Beta: {finance.get_beta()}\n"
        )
    else:
        response = f"Could not retrieve information for ticker {ticker}."

    await message.answer(response)
    await state.clear()


@user_router.message(Command('latest_price'))
async def cmd_latest_price(message: types.Message, state: FSMContext) -> None:
    """
    This handler will be called when user sends `/latest_price` command
    """
    await state.set_state(TickerStates.waiting_for_latest_price)
    await message.answer('Please provide a ticker symbol:')


@user_router.message(TickerStates.waiting_for_latest_price)
async def process_latest_price(
    message: types.Message, state: FSMContext
) -> None:
    """
    This handler will process the ticker symbol provided by the user
    """
    ticker = message.text.upper()
    finance = Finance(ticker)
    latest_price = finance.get_latest_price()
    if latest_price is not None:
        response = f"The latest price for {ticker} is ${latest_price:.2f}."
    else:
        response = f"Could not retrieve the latest price for ticker {ticker}."

    await message.answer(response)
    await state.clear()
