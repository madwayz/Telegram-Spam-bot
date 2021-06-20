from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)

    kb.add(
        InlineKeyboardButton('Мои аккаунты🤖', callback_data='menu_my_accounts'),
        InlineKeyboardButton('Рассылка💬', callback_data='menu_distribution')
    )
    return kb
