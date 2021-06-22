from aiogram.dispatcher import FSMContext
from aiogram import types

from src.base.database import Database
from src.base.objects import dispatcher
from src.base.states import AccountSettings


@dispatcher.message_handler(state=AccountSettings.waiting_for_text)
async def process_edit_text_settings(message: types.Message, state: FSMContext):
    db = Database()
    user_state = await state.get_data()
    account_type = user_state.get('type')
    db.update_account_text(account_type=account_type, text=message.text)
    await state.reset_state(with_data=False)
    await message.answer('Текст рассылки успешно обновлен👍')
