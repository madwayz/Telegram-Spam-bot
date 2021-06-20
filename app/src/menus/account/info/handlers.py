from src.base.database import Database
from src.base.objects import dispatcher, bot
from aiogram import types
from src.menus.account.not_exists.menu import NotAvailableAccountsMenu
from src.menus.account.info.menu import AccountInfoMenu


@dispatcher.callback_query_handler(lambda call: call.data in ['taxi_account', 'invest_account'])
async def account_menu(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    db = Database()

    if not db.get_accounts_quantity():
        menu = NotAvailableAccountsMenu()
    else:
        menu = AccountInfoMenu(initiator=callback_query.data)

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )
