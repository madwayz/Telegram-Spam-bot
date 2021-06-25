from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.models.account import Account
import json


def get_delivery_settings_keyboard(account):
    kb = InlineKeyboardMarkup(row_width=1)

    for chat in account.get_chats():
        kb.add(InlineKeyboardButton('@' + chat, callback_data=json.dumps({'action': 'chat_settings', 'data': chat})))

    start_mass_distribution = json.dumps({'action': 'start_mass_distribution'})
    kb.add(
        InlineKeyboardButton('Начать массовую рассылку💬', callback_data=start_mass_distribution),
        InlineKeyboardButton('Назад🔙', callback_data='menu_distribution')
    )
    return kb


def get_chat_settings_keyboard(settings):
    kb = InlineKeyboardMarkup(row_width=1)

    chat_name = settings.get('chat_name')

    add_interval_data = json.dumps({'action': 'set_interval', 'data': chat_name})
    add_message_quantity = json.dumps({'action': 'set_quantity', 'data': chat_name})

    edit_interval_data = json.dumps({'action': 'edit_interval', 'data': chat_name})
    edit_message_quantity = json.dumps({'action': 'edit_quantity', 'data': chat_name})

    start_distribution = json.dumps({'action': 'start_distribution', 'data': chat_name})

    if settings.get('message_interval'):
        kb.add(InlineKeyboardButton('Изменить интервал', callback_data=edit_interval_data))
    else:
        kb.add(InlineKeyboardButton('Установить интервал', callback_data=add_interval_data))

    if settings.get('message_quantity'):
        kb.add(InlineKeyboardButton('Изменить кол-во сообщений', callback_data=edit_message_quantity))
    else:
        kb.add(InlineKeyboardButton('Установить кол-во сообщений', callback_data=add_message_quantity))

    if settings.get('message_interval') and settings.get('message_quantity'):
        kb.add(InlineKeyboardButton('Начать рассылку💬', callback_data=start_distribution))

    kb.add(InlineKeyboardButton('Назад', callback_data='revert_to_chat_settings'))
    return kb
