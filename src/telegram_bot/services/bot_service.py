import logging

from aiogram import Dispatcher


async def start_bot(dp: Dispatcher, bot):
    """
    Start bot with dispatcher
    """
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"An error occurred while polling: {e}")
