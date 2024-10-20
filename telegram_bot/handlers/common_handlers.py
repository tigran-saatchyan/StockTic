import logging

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from telegram_bot.states import RegistrationStates

common_router = Router()


@common_router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    """
    This handler will be called when the user sends `/start` command.
    """
    # Inline keyboard for registration prompt
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Yes", callback_data="register_yes")],
            [InlineKeyboardButton(text="No", callback_data="register_no")],
        ]
    )
    sent_message = await message.answer(
        "Do you want to register?", reply_markup=keyboard
    )

    data = await state.get_data()
    messages = data.get("messages", [])
    messages.append(sent_message.message_id)
    await state.update_data(messages=messages)


@common_router.callback_query(lambda c: c.data == "register_yes")
async def process_register_yes(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    """
    This handler will be called when the user chooses to register.
    """
    await state.set_state(RegistrationStates.waiting_for_email)
    sent_message = await callback_query.message.answer(
        "Please provide your email address:"
    )
    await callback_query.answer()

    # Store message ID to context for later deletion
    data = await state.get_data()
    messages = data.get("messages", [])
    messages.append(sent_message.message_id)
    await state.update_data(messages=messages)


@common_router.callback_query(lambda c: c.data == "register_no")
async def process_register_no(
    callback_query: types.CallbackQuery, state: FSMContext
) -> None:
    """
    This handler will be called when the user chooses not to register.
    """
    sent_message = await callback_query.message.answer(
        "You can start the registration process later using the command /register or through the menu."
    )
    await callback_query.answer()

    # Store message ID to context for later deletion
    data = await state.get_data()
    messages = data.get("messages", [])
    messages.append(sent_message.message_id)
    await state.update_data(messages=messages)


@common_router.message(Command("clear"))
async def cmd_clear(message: types.Message, state: FSMContext) -> None:
    """
    Clears all messages from the chat
    """
    chat_id = message.chat.id
    message_id = message.message_id
    error_count = 0
    max_errors = 1  # Limit the number of consecutive errors to prevent infinite looping

    for msg_id in range(message_id, message_id - 1000, -1):  # Adjust range as needed
        if error_count >= max_errors:
            break

        try:
            await message.bot.delete_message(chat_id, msg_id)
        except Exception as e:
            error_count += 1
            print(f"Failed to delete message {msg_id}: {e}")
        else:
            error_count = 0  # Reset error count if a message is successfully deleted

    await state.clear()
    await message.answer("All messages have been cleared.")


@common_router.message(Command("get_topic_id"))
async def get_topic_id(message: types.Message) -> None:
    """
    Handler for the /get_topic_id command.

    This handler retrieves the chat ID and the topic ID (message thread ID) from the incoming message
    and sends them back to the user. It also logs this information.

    Args:
        message (types.Message): The incoming message object containing the chat and thread information.
    """
    topic_id = message.message_thread_id
    chat_id = message.chat.id
    await message.answer(f"Chat ID: {chat_id}, Topic ID: {topic_id}")
    logging.info(f"Chat ID: {chat_id}, Topic ID: {topic_id}")
