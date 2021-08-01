from aiogram.dispatcher.filters.state import State, StatesGroup


class AccountSettings(StatesGroup):
    waiting_for_text = State()


class InputChatName(StatesGroup):
    waiting_for_chat = State()


class AddAccount(StatesGroup):
    waiting_for_phone_number = State()
    waiting_for_security_code = State()


class ChatSettingsAddInterval(StatesGroup):
    waiting_for_interval = State()


class ChatSettingsEditInterval(StatesGroup):
    waiting_for_interval = State()


class ChatSettingsAddQuantity(StatesGroup):
    waiting_for_quantity = State()


class ChatSettingsEditQuantity(StatesGroup):
    waiting_for_quantity = State()


class AccountRegister(StatesGroup):
    register_phone_number = State()
    register_api_id = State()
    register_api_hash = State()
    register_security_code = State()
    finish = State()


class AccountReauth(StatesGroup):
    register_security_code = State()
