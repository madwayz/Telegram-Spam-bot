import json

from aiogram.dispatcher import FSMContext
from aiogram import types

from src.base.helpers import update_base_state
from src.base.objects import dispatcher, bot
from src.models.chat import Chat
from src.utils.get_json_data import get_callback_data
from src.views.distribution.settings.menu import DeliverySettingsMenu, ChatSettings
from src.base.states import ChatSettingsEditQuantity, ChatSettingsEditInterval, InputChatName
from src.base.states import ChatSettingsAddQuantity, ChatSettingsAddInterval


@dispatcher.callback_query_handler(
    lambda call: call.data in ['taxi_delivery_settings', 'invest_delivery_settings'],
    state='*'
)
async def delivery_settings(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    account_state = await state.get_data()
    print(account_state)

    await update_base_state(state, callback_query)

    account_state = await state.get_data()
    menu = DeliverySettingsMenu(account_state)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )
    await InputChatName.waiting_for_chat.set()


@dispatcher.callback_query_handler(
    lambda call: get_callback_data(call.data, 'action') == 'chat_settings',
    state='*'
)
async def chat_settings(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.reset_state(with_data=False)

    chat_name = json.loads(callback_query.data).get('data')

    chat = Chat()
    settings = chat.get_settings(chat_name)

    menu = ChatSettings(settings)

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )


@dispatcher.callback_query_handler(lambda call: call.data == 'revert_to_chat_settings', state='*')
async def cancel_add_chats(callback_query: types.CallbackQuery, state: FSMContext):
    await delivery_settings(callback_query, state)


@dispatcher.callback_query_handler(
    lambda call: get_callback_data(call.data, 'action') in ['set_message_interval', 'edit_message_interval']
)
async def process_message_interval(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    chat_name = json.loads(callback_query.data).get('data')
    await state.set_data({'chat_name': chat_name})
    await bot.send_message(callback_query.from_user.id, 'Введите интервал отправки сообщений(в минутах)⏰')

    action = json.loads(callback_query.data).get('action')
    if action == 'set_message_interval':
        await ChatSettingsAddInterval.waiting_for_interval.set()
    elif action == 'edit_message_interval':
        await ChatSettingsEditInterval.waiting_for_interval.set()


@dispatcher.callback_query_handler(
    lambda call: get_callback_data(call.data, 'action') in ['set_message_quantity', 'edit_message_quantity']
)
async def process_message_quantity(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    chat_name = json.loads(callback_query.data).get('data')
    await state.set_data({'chat_name': chat_name})
    await bot.send_message(callback_query.from_user.id, 'Введите количество сообщений')

    action = json.loads(callback_query.data).get('action')
    if action == 'set_message_interval':
        await ChatSettingsAddQuantity.waiting_for_quantity.set()
    elif action == 'edit_message_interval':
        await ChatSettingsEditQuantity.waiting_for_quantity.set()


@dispatcher.callback_query_handler(
    lambda call: get_callback_data(call.data, 'action') == 'start_distribution'
)
async def start_distribution(callback_query: types.CallbackQuery, state: FSMContext):
    chat_name = json.loads(callback_query.data).get('data')
    await state.set_data({'chat_name': chat_name})
    # TODO: сделать запуск рассылки
