from aiogram.dispatcher import FSMContext
from aiogram import types

from src.base.objects import dispatcher, bot
from src.base.states import InputChatName
from src.views.account.chat_list.menu import ChatListMenu
from src.views.account.info.handlers import account_menu


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
    await InputChatName.waiting_for_chat.set()
    await callback_query.message.answer(
        'Для получения доступа к кнопке "назад" введите любой текст. '
        'Чтобы добавить чаты для рассылки введите @username чата '
        'или отправьте файл с @username чатов, которые хотите добавить➕'
    )


@dispatcher.callback_query_handler(lambda call: call.data == 'cancel_add_chats', state='*')
async def cancel_add_chats(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    await account_menu(callback_query, state)
