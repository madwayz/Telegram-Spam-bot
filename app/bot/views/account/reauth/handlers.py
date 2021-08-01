from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.base.objects import dispatcher, bot, userbot
from bot.base.states import AccountReauth
from bot.models.account import Account


@dispatcher.callback_query_handler(lambda call: call.data == 'account_reauth', state='*')
async def account_reauth(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Введите код подтверждения, который отправил вам телеграм✉️',
    )

    account_state = await state.get_data()
    account_type = account_state.get('type')
    account = Account(account_type)
    account_data = account.get()

    status = await userbot.authorize(
        phone_number=account_data.get('phone_number'),
        api_id=account_data.get('api_id'),
        api_hash=account_data.get('api_hash'),
    )

    if status == 'SecurityCodeNeeded':
        account.update_info(
            session_name=userbot.session_name,
            in_progress=False
        )
        await AccountReauth.register_security_code.set()