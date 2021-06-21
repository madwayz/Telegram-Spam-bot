from aiogram.dispatcher import FSMContext
from aiogram import types

from src.base.database import Database


async def process_edit_text_settings(message: types.Message, state: FSMContext):
    db = Database()
    user_state = await state.get_data()
    account_type = user_state.get('type')
    db.update_account_text(account_type=account_type, text=message.text)
    await state.finish()
    await message.answer('Текст рассылки успешно обновлен👍')
