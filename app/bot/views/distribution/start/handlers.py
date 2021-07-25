import traceback

from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.base.objects import dispatcher, userbot, bot
from bot.models.account import Account
from bot.utils.get_json_data import get_callback_data


@dispatcher.callback_query_handler(
    lambda call: get_callback_data(call.data, 'action') in ['start_distribution', 'start_mass_distribution'],
    state='*'
)
async def start_distribution(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    action = get_callback_data(callback_query.data, 'action')
    is_mass_distribution = action == 'start_mass_distribution'

    chat_name = None
    if not is_mass_distribution:
        chat_name = get_callback_data(callback_query.data, 'data')

    account_state = await state.get_data()
    account_type = account_state.get('type')
    account = Account(account_type)
    account_data = account.get()

    if account_data.get('in_progress'):
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text='На этом аккаунте рассылка уже запущена.'
        )
        return

    text = account_data.get('distribution_text')

    if text == 'отсутствует':
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text='Добавьте текст для чата. Операция отменена.'
        )
        return

    chats_list = account.get_ready_chats_settings(chat_name if not is_mass_distribution else None)

    if not account.get_chats() or not chats_list:
        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text='Необходимо добавить хотя бы один чат. Операция отменена'
        )
        return

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Конфигурирую воркер...'
    )

    api_id = account_data.get('api_id')
    api_hash = account_data.get('api_hash')
    phone_number = account_data.get('phone_number')
    session_path = account_data.get('session_path')

    try:
        await userbot.preconfigure(api_id, api_hash, phone_number, session_path)
    except Exception:
        traceback.format_exc()

        await bot.send_message(
            chat_id=callback_query.from_user.id,
            text='При преконфигурации бота возникла непредвиденная ошибка'
        )

    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text='Запускаю рассылку на настроенные чаты. '
    )

    await bot.send_chat_action(
        chat_id=callback_query.from_user.id,
        action='typing'
    )

    account.update_distribution_status(True)

    try:
        await userbot.start_distribution(
            chats_list=chats_list,
            text=text
        )
        message = 'Рассылка успешно завершена'
    except Exception:
        traceback.format_exc()

        message = "При рассылке возникла непредвиденная ошибка"

    account.update_distribution_status(False)
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=message
    )