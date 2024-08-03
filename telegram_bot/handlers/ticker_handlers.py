# telegram_bot/handlers/ticker_handlers.py
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram_bot.states import TickerStates
from tickers.services import Finance

ticker_router = Router()


@ticker_router.message(Command('ticker_info'))
async def cmd_ticker_info(message: types.Message, state: FSMContext) -> None:
    """
    This handler will be called when user sends `/ticker_info` command
    """
    await state.set_state(TickerStates.waiting_for_ticker_info)
    await message.answer('Please provide a ticker symbol:')


@ticker_router.message(TickerStates.waiting_for_ticker_info)
async def process_ticker_info(
    message: types.Message, state: FSMContext
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


@ticker_router.message(Command('latest_price'))
async def cmd_latest_price(message: types.Message, state: FSMContext) -> None:
    """
    Request the latest price for a ticker symbol
    """
    await state.set_state(TickerStates.waiting_for_latest_price)
    await message.answer('Please provide a ticker symbol:')


@ticker_router.message(TickerStates.waiting_for_latest_price)
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
