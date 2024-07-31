from aiogram.fsm.state import StatesGroup, State


class TickerStates(StatesGroup):
    waiting_for_ticker_info = State()
    waiting_for_latest_price = State()


class RegistrationStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_telephone = State()
    waiting_for_verification = State()
