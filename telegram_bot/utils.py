from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def notification_type_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Email", callback_data="email"),
                InlineKeyboardButton(
                    text="Telegram", callback_data="telegram"
                ),
                InlineKeyboardButton(text="All", callback_data="all")
            ]
        ]
    )
    return keyboard


def notification_criteria_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="More than", callback_data="more_than"
                ),
                InlineKeyboardButton(
                    text="Less than", callback_data="less_than"
                )
            ]
        ]
    )
    return keyboard
