from aiogram.dispatcher import FSMContext

from bot.base.helpers import update_base_state
from bot.base.objects import dispatcher, bot
from aiogram import types

from bot.models.account import Account
from bot.views.account.info.menu import AccountInfoMenu, NotAvailableAccountsMenu


@dispatcher.callback_query_handler(
    lambda call: call.data in ['taxi_account',
                               'invest_account',
                               'pawnshop_account',
                               'wagons_delivery_settings'],
    state='*')
async def account_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.reset_state(with_data=False)
    await update_base_state(state, callback_query.data)

    account_state = await state.get_data()
    account_type = account_state.get('type')
    account = Account(account_type)
    if not account.count_all():
        menu = NotAvailableAccountsMenu()
    else:
        menu = AccountInfoMenu(state=account_state)

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )
