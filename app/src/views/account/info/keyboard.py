from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_account_info_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton('Настройка текста📝', callback_data='text_settings'),
        InlineKeyboardButton('База чатов👥', callback_data='chat_list'),
        InlineKeyboardButton('Добавить аккаунт💿', callback_data='create_account'),
        # InlineKeyboardButton('Изменить аккаунт🔄', callback_data='update_account'),
        InlineKeyboardButton('Назад🔙', callback_data='menu_my_accounts'),
    )
    return kb


def get_create_account_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton('Добавить аккаунт💿', callback_data='create_account'),
        InlineKeyboardButton('Назад🔙', callback_data='main_menu'),
    )
    return kb
