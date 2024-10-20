"""This module defines the state groups for the Telegram bot's finite state
machine (FSM).

Classes:
    TickerStates: State group for handling ticker-related states.
    RegistrationStates: State group for handling user registration states.
    NotificationStates: State group for handling notification-related states.
"""

from aiogram.fsm.state import State, StatesGroup


class TickerStates(StatesGroup):
    """State group for handling ticker-related states.

    Attributes:
        waiting_for_ticker_info (State): State for waiting for ticker
            information.
        waiting_for_latest_price (State): State for waiting for the latest
            price.
        waiting_for_ticker_news (State): State for waiting for ticker news.
    """

    waiting_for_ticker_info = State()
    waiting_for_latest_price = State()
    waiting_for_ticker_news = State()


class RegistrationStates(StatesGroup):
    """State group for handling user registration states.

    Attributes:
        waiting_for_email (State): State for waiting for the user's email.
        waiting_for_telephone (State): State for waiting for the user's
            telephone number.
        waiting_for_verification (State): State for waiting for verification.
    """

    waiting_for_email = State()
    waiting_for_telephone = State()
    waiting_for_verification = State()


class NotificationStates(StatesGroup):
    """State group for handling notification-related states.

    Attributes:
        waiting_for_ticker (State): State for waiting for the ticker.
        waiting_for_value (State): State for waiting for the value.
        waiting_for_type (State): State for waiting for the type.
        waiting_for_criteria (State): State for waiting for the criteria.
        waiting_for_unregistration_ticker (State): State for waiting for the
            unregistration ticker.
        waiting_for_unregistration_value (State): State for waiting for the
            unregistration value.
    """

    waiting_for_ticker = State()
    waiting_for_value = State()
    waiting_for_type = State()
    waiting_for_criteria = State()
    waiting_for_unregistration_ticker = State()
    waiting_for_unregistration_value = State()
