from src.base.objects import dispatcher, bot
from aiogram import types
from src.menus.account.switcher.menu import SwitchAccountMenu


@dispatcher.callback_query_handler(lambda call: call.data in ['menu_my_accounts', 'menu_distribution'])
async def switch_account(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    menu = SwitchAccountMenu(initiator=callback_query.data)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )
