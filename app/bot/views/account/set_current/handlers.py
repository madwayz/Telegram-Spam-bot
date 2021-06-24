from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.base.objects import dispatcher, bot
from bot.models.account import Account
from bot.utils.get_json_data import get_callback_data


@dispatcher.callback_query_handler(
    lambda call: get_callback_data(call.data, 'action') == 'set_current_account',
    state='*'
)
async def set_current_account(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.reset_state(with_data=False)

    account_id = get_callback_data(callback_query.data, 'data')
    account_state = await state.get_data()

    account = Account(account_state.get('type'))
    account.set_current(account_id)
    account_data = account.get()
    account_phone_number = account_data.get('phone_number')
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=f'Аккаунт {account_phone_number} установлен как основной'
    )
