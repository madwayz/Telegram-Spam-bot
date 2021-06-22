import os

from aiogram.dispatcher import FSMContext

from settings import BASE_DIR
from src.base.objects import dispatcher, bot
from aiogram import types

from src.base.states import ChatList
from src.models.chat import Chat
from src.models.file import ChatsFile
from src.views.account.chat_list.menu import ChatListMenu


@dispatcher.callback_query_handler(lambda call: call.data == 'chat_list')
async def chat_list(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    menu = ChatListMenu(await state.get_data())
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )
    user_id = callback_query.from_user.id
    await bot.send_document(user_id, menu.get_document())
    await ChatList.waiting_for_chats.set()
    await callback_query.message.answer(
        'Для получения доступа к кнопке "назад" введите любой текст. '
        'Чтобы добавить чаты для рассылки введите @username чата '
        'или отправьте файл с @username чатов, которые хотите добавить➕'
    )


@dispatcher.message_handler(content_types=types.ContentTypes.DOCUMENT, state=ChatList.waiting_for_chats)
async def process_add_chats_file(message: types.Message, state: FSMContext):
    account_state = await state.get_data()
    document = ChatsFile()
    chat = Chat(account_state.get('type'))

    file_id = message.document.file_id
    file_path = f'/tmp/{os.urandom(10). hex()}.xlsx'
    await bot.download_file_by_id(file_id, file_path)

    data = document.parse_file(file_path)
    chat.add_chat_list(data)
    await message.answer('База чатов успешно обновлена👍')
    await state.reset_state(with_data=False)


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=ChatList.waiting_for_chats)
async def process_add_chat(message: types.Message, state: FSMContext):
    account_state = await state.get_data()
    chat = Chat(account_state.get('type'))

    if not message.text.startswith('@'):
        await message.answer('Чат должен начинаться с @. Пример: @test')
        await state.reset_state(with_data=False)
        return

    chat.add_chat_id(message.text)
    await message.answer('База чатов успешно обновлена👍')
    await state.reset_state(with_data=False)
