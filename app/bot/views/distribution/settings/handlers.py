from aiogram.dispatcher import FSMContext
from aiogram import types

from bot.base.helpers import update_base_state
from bot.base.objects import dispatcher, bot
from bot.models.account import Account
from bot.models.chat import Chat
from bot.utils.get_json_data import get_callback_data
from bot.views.account.info.menu import NotAvailableAccountsMenu
from bot.views.distribution.settings.menu import DeliverySettingsMenu, ChatSettings
from bot.base.states import ChatSettingsEditQuantity, ChatSettingsEditInterval, InputChatName
from bot.base.states import ChatSettingsAddQuantity, ChatSettingsAddInterval


@dispatcher.callback_query_handler(
    lambda call: call.data in ['taxi_delivery_settings', 'invest_delivery_settings'],
    state='*'
)
async def delivery_settings(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await update_base_state(state, callback_query)
    account_state = await state.get_data()

    account = Account(account_state.get('type'))
    if not account.count_all():
        menu = NotAvailableAccountsMenu()
    else:
        menu = DeliverySettingsMenu(account_state)
        await InputChatName.waiting_for_chat.set()

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )


@dispatcher.callback_query_handler(
    lambda call: get_callback_data(call.data, 'action') == 'chat_settings',
    state='*'
)
async def chat_settings(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await state.reset_state(with_data=False)

    chat_name = get_callback_data(callback_query.data, 'data')

    chat = Chat()
    settings = chat.get_settings(chat_name)

    menu = ChatSettings(settings)

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )


@dispatcher.callback_query_handler(lambda call: call.data == 'revert_to_chat_settings', state='*')
async def revert_to_chat_settings(callback_query: types.CallbackQuery, state: FSMContext):
    await delivery_settings(callback_query, state)


@dispatcher.callback_query_handler(
    lambda call: get_callback_data(call.data, 'action') in ['set_interval', 'edit_interval']
)
async def process_message_interval(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    chat_name = get_callback_data(callback_query.data, 'data')
    await state.set_data({'chat_name': chat_name})
    await bot.send_message(callback_query.from_user.id, 'Введите интервал отправки сообщений(в минутах)⏰')

    action = get_callback_data(callback_query.data, 'action')
    if action == 'set_interval':
        await ChatSettingsAddInterval.waiting_for_interval.set()
    elif action == 'edit_interval':
        await ChatSettingsEditInterval.waiting_for_interval.set()


@dispatcher.callback_query_handler(
    lambda call: get_callback_data(call.data, 'action') in ['set_quantity', 'edit_quantity']
)
async def process_message_quantity(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    chat_name = get_callback_data(callback_query.data, 'data')
    await state.set_data({'chat_name': chat_name})
    await bot.send_message(callback_query.from_user.id, 'Введите количество сообщений')

    action = get_callback_data(callback_query.data, 'action')
    if action == 'set_quantity':
        await ChatSettingsAddQuantity.waiting_for_quantity.set()
    elif action == 'edit_quantity':
        await ChatSettingsEditQuantity.waiting_for_quantity.set()
