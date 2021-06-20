from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_create_account_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton('Добавить💿', callback_data='add_taxi_account'),
        InlineKeyboardButton('Назад🔙', callback_data='back_to_main_menu'),
    )
    return kb
