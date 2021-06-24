from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.base.objects import dispatcher, bot
from bot.base.states import AccountRegister
from bot.models.account import Account
from bot.views.account.list.menu import AccountListMenu


@dispatcher.callback_query_handler(lambda call: call.data == 'create_account', state='*')
async def create_account(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    account_state = await state.get_data()

    account_type = account_state.get('type')
    account = Account(account_type)
    if account.count_all():
        menu = AccountListMenu(account_type)
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=menu.get_text(),
            reply_markup=menu.get_keyboard()
        )

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Чтобы добавить новый аккаунт, введите номер телефона',
    )
    await AccountRegister.register_phone_number.set()
