import re
from datetime import datetime

import pytz
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from telegram_bot.settings import BotSettings as settings

from custom_utils.utils import format_market_cap
from telegram_bot.states import TickerStates
from tickers.services import Finance

ticker_router = Router()


@ticker_router.message(Command("ticker_info"))
async def cmd_ticker_info(message: types.Message, state: FSMContext) -> None:
    """
    This handler will be called when user sends `/ticker_info` command
    """
    await state.set_state(TickerStates.waiting_for_ticker_info)
    await message.answer("Please provide a ticker symbol:")


@ticker_router.message(TickerStates.waiting_for_ticker_info)
async def process_ticker_info(message: types.Message, state: FSMContext) -> None:
    """
    This handler will process the ticker symbol provided by the user
    """
    ticker = message.text.upper()
    finance = Finance(ticker)
    info = finance.get_info()
    if info:
        try:
            info["marketCap"] = format_market_cap(int(info.get("marketCap", "N/A")))
        except ValueError:
            info["marketCap"] = "N/A"
        response = (
            f"Ticker Information for {ticker}:\n"
            f"Name: {info.get('longName', 'N/A')}\n"
            f"Sector: {info.get('sector', 'N/A')}\n"
            f"Industry: {info.get('industry', 'N/A')}\n"
            f"Price: {info.get('previousClose', 'N/A')}\n"
            f"Market Cap: {info.get('marketCap')}\n"
            f"PE Ratio: {finance.get_pe_ratio()}\n"
            f"EPS: {finance.get_eps()}\n"
            f"Dividend Yield: {finance.get_dividend_yield()}\n"
            f"Beta: {finance.get_beta()}\n"
        )
    else:
        response = f"Could not retrieve information for ticker {ticker}."

    await message.answer(response)
    await state.clear()


@ticker_router.message(Command("latest_price"))
async def cmd_latest_price(message: types.Message, state: FSMContext) -> None:
    """
    Request the latest price for a ticker symbol
    """
    await state.set_state(TickerStates.waiting_for_latest_price)
    await message.answer("Please provide a ticker symbol:")


@ticker_router.message(TickerStates.waiting_for_latest_price)
async def process_latest_price(message: types.Message, state: FSMContext) -> None:
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


@ticker_router.message(Command("news"))
async def request_ticker_for_news(message: types.Message, state: FSMContext) -> None:
    """
    Requests the ticker symbol from the user to fetch news.
    """
    await message.answer(
        "Please provide the ticker symbol for which you want to get the latest news:"
    )
    await state.set_state(TickerStates.waiting_for_ticker_news)


@ticker_router.message(TickerStates.waiting_for_ticker_news)
async def fetch_news(message: types.Message, state: FSMContext) -> None:
    """
    Fetches the latest news for the provided ticker symbol.
    """
    symbol = message.text.strip().upper()
    finance = Finance(symbol)
    news = finance.get_news()

    if news:
        await message.answer(f"Latest news for {symbol}:")
        for article in news:  # Limit to the top 5 articles
            related_tickers = " ".join(
                [
                    "#" + re.sub(r"[^a-zA-Z]", "", ticker.lower())
                    for ticker in article["relatedTickers"]
                ]
            )
            timestamp = article["providerPublishTime"]
            dt = datetime.fromtimestamp(timestamp, pytz.utc)
            formatted_time = dt.astimezone(pytz.timezone(settings.TIME_ZONE)).strftime(
                "%d-%b-%Y %H:%M (%Z)"
            )
            response = (
                f"Title: {article['title']}\n"
                f"Published: {formatted_time}\n"
                f"Link: {article['link']}\n\n"
                f"Related Tickers: {related_tickers}\n"
            )
            await message.answer(response)
    else:
        await message.answer(f"No news found for {symbol}.")

    await state.clear()
