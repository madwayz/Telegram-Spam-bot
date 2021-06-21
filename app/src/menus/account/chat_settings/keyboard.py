from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_text_setting_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton('Изменить текст рассылки✏️', callback_data='edit_text_settings'),
        InlineKeyboardButton('Назад🔙', callback_data='back_to_account_info')
    )
    return kb


def get_edit_text_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)

    kb.add(
        InlineKeyboardButton('Отмена❌', callback_data='back_to_text_settings')
    )
    return kb