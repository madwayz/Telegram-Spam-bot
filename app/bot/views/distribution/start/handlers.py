from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.base.objects import dispatcher, userbot
from bot.models.account import Account
from bot.models.chat import Chat
from bot.utils.get_json_data import get_callback_data


@dispatcher.callback_query_handler(
    lambda call: get_callback_data(call.data, 'action') in ['start_distribution', 'start_mass_distribution']
)
async def start_mass_distribution(callback_query: types.CallbackQuery, state: FSMContext):
    chat_name = get_callback_data(callback_query.data, 'data')
    action = get_callback_data(callback_query.data, 'action')

    is_mass_distribution = action == 'start_mass_distribution'

    account_state = await state.get_data()
    account = Account(account_state.get('type'))
    account_data = account.get()
    text = account_data.get('distribution_text')

    chat = Chat()
    settings = chat.get_settings(chat_name)
    message_interval = settings.get('message_interval')
    message_quantity = settings.get('message_quantity')

    if is_mass_distribution:
        chats_list = account.get_chats()
    else:
        chats_list = [chat_name]

    await userbot.start_distribution(
        chats_list,
        text,
        interval=message_interval,
        quantity=message_quantity,
    )
