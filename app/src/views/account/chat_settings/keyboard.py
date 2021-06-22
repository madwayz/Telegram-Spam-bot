from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_text_setting_keyboard(state):
    kb = InlineKeyboardMarkup(row_width=1)
    alias = state.get('alias')
    kb.add(
        InlineKeyboardButton('Изменить текст рассылки✏️', callback_data='edit_text_settings'),
        InlineKeyboardButton('Назад🔙', callback_data='taxi_account' if alias == 'HR' else 'invest_account')
    )
    return kb


def get_edit_text_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton('Отмена❌', callback_data='cancel_edit_text_settings')
    )
    return kb
