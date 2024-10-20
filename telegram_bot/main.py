"""This module initializes and runs the Telegram bot.

Functions:
    register_routers: Registers routers to the dispatcher.
    main: Main function to run the bot with dispatcher and start
        polling updates from Telegram.
"""

import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot_config import BotConfig
from bot_instance import bot
from handlers import (
    common_router,
    notification_router,
    registration_router,
    ticker_router,
)

from telegram_bot.services import start_bot

logging.basicConfig(level=logging.INFO)


def register_routers(dp: Dispatcher) -> None:
    """Registers routers to the dispatcher.

    Args:
        dp (Dispatcher): The dispatcher to which routers will be registered.
    """
    dp.include_router(common_router)
    dp.include_router(registration_router)
    dp.include_router(ticker_router)
    dp.include_router(notification_router)


async def main() -> None:
    """Main function to run the bot with dispatcher and start polling
    updates from Telegram.
    """
    config = BotConfig(
        admin_ids=[463092387],
        welcome_message="Welcome to the bot! 🤖",
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp["config"] = config

    register_routers(dp)

    try:
        await start_bot(dp, bot)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())
