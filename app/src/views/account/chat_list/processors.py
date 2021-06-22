import os

from aiogram.dispatcher import FSMContext

from src.base.filters import is_chat_tag
from src.base.objects import dispatcher, bot
from aiogram import types

from src.base.states import InputChatName
from src.models.account import Account
from src.models.file import ChatsFile


@dispatcher.message_handler(content_types=types.ContentTypes.DOCUMENT, state=InputChatName.waiting_for_chat)
async def process_add_chats_file(message: types.Message, state: FSMContext):
    account_state = await state.get_data()
    document = ChatsFile()
    account = Account(account_state.get('type'))

    file_id = message.document.file_id
    file_path = f'/tmp/{os.urandom(10). hex()}.xlsx'
    await bot.download_file_by_id(file_id, file_path)

    data = document.parse_file(file_path)
    account.add_chat_list(data)
    await message.answer('База чатов успешно обновлена👍')
    await state.reset_state(with_data=False)


@dispatcher.message_handler(
    content_types=types.ContentTypes.TEXT,
    state=InputChatName.waiting_for_chat
)
async def process_add_chat(message: types.Message, state: FSMContext):
    account_state = await state.get_data()
    account = Account(account_state.get('type'))

    if not await is_chat_tag(message):
        await state.reset_state(with_data=False)
        return

    account.add_chat_name(message.text)
    await message.answer('База чатов успешно обновлена👍')
    await state.reset_state(with_data=False)
