from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_chat_list_keyboard(state):
    kb = InlineKeyboardMarkup(row_width=2)
    alias = state.get('alias')
    button = InlineKeyboardButton(
        'Назад🔙',
        callback_data='taxi_account' if alias == 'HR' else 'invest_account'
    )
    kb.add(button)
    return kb
