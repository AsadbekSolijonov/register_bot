from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    language = State()
    fullname = State()
    phone_number = State()
    location = State()
