from aiogram.fsm.state import StatesGroup, State


class TickerStates(StatesGroup):
    waiting_for_ticker_info = State()
    waiting_for_latest_price = State()
    waiting_for_ticker_news = State()


class RegistrationStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_telephone = State()
    waiting_for_verification = State()


class NotificationStates(StatesGroup):
    waiting_for_ticker = State()
    waiting_for_value = State()
    waiting_for_type = State()
    waiting_for_criteria = State()
    waiting_for_unregistration_ticker = State()
    waiting_for_unregistration_value = State()
