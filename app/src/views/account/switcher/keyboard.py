from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_switch_account_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton('Такси📞', callback_data='taxi_account'),
        InlineKeyboardButton('Инвест📊', callback_data='invest_account'),
        InlineKeyboardButton('Назад🔙', callback_data='main_menu'),
    )
    return kb
