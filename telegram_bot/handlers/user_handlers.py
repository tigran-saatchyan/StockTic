from aiogram import types, Router
from aiogram.filters import Command
from aiogram.utils.formatting import Text, Bold, Italic

from bot_config import BotConfig

user_router = Router()


@user_router.message(Command('start'))
async def cmd_start(message: types.Message, config: BotConfig) -> None:
    """
    This handler will be called when user sends `/start` command
    """
    content = Text(
        'Hello! ',
        Bold(message.from_user.full_name),
        # start from new line
        '\n',
        Italic(config.welcome_message),
    )
    await message.answer(
        **content.as_kwargs()
    )


@user_router.message(Command('my_status'))
async def cmd_admin_info(message: types.Message, config: BotConfig) -> None:
    """
    This handler will be called when user sends `/admin_info` command
    """
    print(message.from_user.id)
    if message.from_user.id not in config.admin_ids:
        await message.answer('You are not admin!')
    else:
        await message.answer('You are admin!')
