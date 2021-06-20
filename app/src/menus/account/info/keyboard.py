from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_account_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton('Настройка текста📝', callback_data='text_settings'),
        InlineKeyboardButton('База чатов👥', callback_data='chat_list'),
        InlineKeyboardButton('Изменить аккаунт🔄', callback_data='edit_account'),
        InlineKeyboardButton('Назад🔙', callback_data='back_to_main_menu'),
    )
    return kb
