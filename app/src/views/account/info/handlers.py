from aiogram.dispatcher import FSMContext
from src.base.objects import dispatcher, bot
from aiogram import types

from src.models.account import Account
from src.views.account.not_exists.menu import NotAvailableAccountsMenu
from src.views.account.info.menu import AccountInfoMenu
from src.utils.account_type import get_account_type_id


@dispatcher.callback_query_handler(lambda call: call.data in ['taxi_account', 'invest_account'])
async def account_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    account_state = await state.get_data()
    if len(['id', 'alias'] & account_state.keys()) < 3:
        account_type_data = get_account_type_id(callback_query.data)
        account_type = account_type_data.get('id')
        account_type_alias = account_type_data.get('alias')

        await state.update_data(type=account_type, alias=account_type_alias)

    account_state = await state.get_data()
    account = Account(account_state.get('type'))
    if not account.count_all():
        menu = NotAvailableAccountsMenu()
    else:
        menu = AccountInfoMenu(state=account_state)

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )

