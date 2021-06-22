from aiogram.dispatcher import FSMContext

from src.base.objects import dispatcher, bot
from aiogram import types
from src.views.account.switcher.menu import SwitchAccountMenu


@dispatcher.callback_query_handler(lambda call: call.data in ['menu_my_accounts', 'menu_distribution'])
async def account_menu_by_type(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.update_data({'action': callback_query.data})
    account_state = await state.get_data()
    menu = SwitchAccountMenu(account_state)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )
