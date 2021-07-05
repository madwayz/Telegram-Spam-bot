from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_switch_account_keyboard(state):
    kb = InlineKeyboardMarkup(row_width=2)
    action = state.get('action')

    taxi_button_data = 'taxi_account' if action == 'menu_my_accounts' else 'taxi_delivery_settings'
    invest_button_data = 'invest_account' if action == 'menu_my_accounts' else 'invest_delivery_settings'
    pawnshop_button_data = 'pawnshop_account' if action == 'menu_my_accounts' else 'pawnshop_delivery_settings'
    wagons_button_data = 'wagons_account' if action == 'menu_my_accounts' else 'wagons_delivery_settings'
    kb.add(
        InlineKeyboardButton('Такси📞', callback_data=taxi_button_data),
        InlineKeyboardButton('Инвест📊', callback_data=invest_button_data),
        InlineKeyboardButton('Ломбард', callback_data=pawnshop_button_data),
        InlineKeyboardButton('Фуры', callback_data=wagons_button_data),
        InlineKeyboardButton('Назад🔙', callback_data='main_menu'),
    )
    return kb
