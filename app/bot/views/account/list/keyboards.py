from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json


def get_accounts_list_keyboard(state, account):
    kb = InlineKeyboardMarkup(row_width=1)

    accounts_list = account.list()

    for account in accounts_list:
        callback_data = json.dumps({'action': 'set_current_account', 'data': account.get('id')})
        kb.add(
            InlineKeyboardButton(account.get('phone_number'), callback_data=callback_data),
        )

    kb.add(
        InlineKeyboardButton('Добавить аккаунт💿', callback_data='create_account'),
        InlineKeyboardButton('Назад🔙', callback_data='taxi_account' if state.get('alias') == 'HR' else 'invest_account')
    )

    return kb