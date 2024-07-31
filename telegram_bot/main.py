import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot_config import BotConfig
from bot_instance import bot
from handlers import user_router
from services import start_bot

logging.basicConfig(level=logging.INFO)


def register_routers(dp: Dispatcher) -> None:
    """
    Register routers to dispatcher
    """
    dp.include_router(user_router)


async def main() -> None:
    """
    Main function to run bot with dispatcher and start polling
    updates from Telegram
    """
    config = BotConfig(
        admin_ids=[463092387],
        welcome_message='Welcome to the bot! 🤖',
    )

    dp = Dispatcher(storage=MemoryStorage())
    dp['config'] = config

    register_routers(dp)

    try:
        await start_bot(dp, bot)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == '__main__':
    asyncio.run(main())
