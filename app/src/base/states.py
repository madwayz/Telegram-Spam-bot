from aiogram.dispatcher.filters.state import State, StatesGroup


class ChatSettings(StatesGroup):
    waiting_for_text = State()


class ChatList(StatesGroup):
    waiting_for_chats = State()


class AddAccount(StatesGroup):
    waiting_for_phone_number = State()
    waiting_for_security_code = State()