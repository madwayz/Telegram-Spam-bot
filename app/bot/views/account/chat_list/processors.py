import os
import re

from aiogram.dispatcher import FSMContext

from bot.base.objects import dispatcher, bot
from aiogram import types

from bot.base.states import InputChatName
from bot.models.account import Account
from bot.models.file import ChatsFile


@dispatcher.message_handler(
    content_types=types.ContentTypes.DOCUMENT,
    state=InputChatName.waiting_for_chat
)
async def process_add_chats_file(message: types.Message, state: FSMContext):
    account_state = await state.get_data()
    document = ChatsFile()
    account = Account(account_state.get('type'))

    file_id = message.document.file_id
    file_path = f'/tmp/{os.urandom(10).hex()}.xlsx'
    await bot.download_file_by_id(file_id, file_path)

    data = set(document.parse_file(file_path))
    chat_tags_list = set(filter(lambda x: re.search(r'^@(\w+)$', x), data))

    if len(data) != len(chat_tags_list):
        await message.answer('Ошибка при загрузке чатов из файла. '
                             'Каждый чат должен быть в одной колонке и первом столбце.'
                             'Попробуйте ещё раз. Пример формата чата: @some_chat_123')
        await state.set_state(InputChatName.waiting_for_chat)
        return

    chat_list = set(map(lambda x: x[1:], chat_tags_list))
    account.add_chat_list(chat_list)
    await message.answer('База чатов успешно обновлена👍')
    await state.reset_state(with_data=False)


@dispatcher.message_handler(
    content_types=types.ContentTypes.TEXT,
    state=InputChatName.waiting_for_chat
)
async def process_add_chat(message: types.Message, state: FSMContext):
    account_state = await state.get_data()
    account = Account(account_state.get('type'))

    chat_tag_search = re.search(r'^@(\w+)$', message.text)
    if not chat_tag_search:
        await message.answer('Ошибка при добавлении чата. Попробуйте ещё раз. Пример: @some_test_123')
        await state.set_state(InputChatName.waiting_for_chat)
        return

    chat_tag = chat_tag_search.group()
    chat_name = chat_tag[1:]
    account.add_chat_name(chat_name)
    await message.answer('База чатов успешно обновлена👍')
    await state.reset_state(with_data=False)
