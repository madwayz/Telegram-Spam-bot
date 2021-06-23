from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_confirm_box_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton('Да✅', callback_data='yes_create_account'),
        InlineKeyboardButton('Нет❌', callback_data='no_create_account'),
    )
    return kb
