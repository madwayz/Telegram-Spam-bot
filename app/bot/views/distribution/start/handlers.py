from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.base.objects import dispatcher, userbot
from bot.models.account import Account
from bot.utils.get_json_data import get_callback_data


@dispatcher.callback_query_handler(
    lambda call: call.data in ['start_distribution', 'start_mass_distribution'],
    state='*'
)
async def start_mass_distribution(callback_query: types.CallbackQuery, state: FSMContext):
    action = get_callback_data(callback_query.data, 'action')
    is_mass_distribution = action == 'start_mass_distribution'

    chat_name = None
    if not is_mass_distribution:
        chat_name = get_callback_data(callback_query.data, 'data')

    account_state = await state.get_data()
    account_type = account_state.get('type')
    account = Account(account_type)
    account_data = account.get()
    text = account_data.get('distribution_text')

    chats_list = account.get_ready_chats_settings(chat_name if not is_mass_distribution else None)

    if not account.get_chats():
        await callback_query.answer('Необходимо добавить хотя бы один чат. Операция отменена', show_alert=False)
        return

    if not chats_list:
        await callback_query.answer('Необходимо настроить хотя бы один чат. Операция отменена', show_alert=False)
        return

    await callback_query.answer('Конфигурирую воркер...', show_alert=False)

    api_id = account_data.get('api_id')
    api_hash = account_data.get('api_hash')
    phone_number = account_data.get('phone_number')
    session_path = account_data.get('session_path')

    userbot.preconfigure(api_id, api_hash, phone_number, session_path)

    await callback_query.answer('Запускаю рассылку...')
    status = await userbot.start_distribution(
        chats_list=chats_list,
        text=text
    )

    message = 'Рассылка успешно закончена' if status else "При рассылке возникли непредвиденные ошибки"
    await callback_query.answer(message)
