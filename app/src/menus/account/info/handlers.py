from aiogram.dispatcher import FSMContext
from src.base.database import Database
from src.base.objects import dispatcher, bot
from aiogram import types
from src.menus.account.not_exists.menu import NotAvailableAccountsMenu
from src.menus.account.info.menu import AccountInfoMenu
from src.utils import get_account_type_id


@dispatcher.callback_query_handler(lambda call: call.data in ['taxi_account', 'invest_account'])
async def account_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    db = Database()

    account_type = get_account_type_id(callback_query.data)
    if not db.get_account_quantity(account_type=account_type):
        menu = NotAvailableAccountsMenu()
    else:
        menu = AccountInfoMenu(account_type=account_type)

    await state.update_data(type=account_type)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )
