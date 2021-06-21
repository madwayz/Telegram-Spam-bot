from aiogram.dispatcher.filters.state import State, StatesGroup


class ChatSettings(StatesGroup):
    waiting_for_text = State()
