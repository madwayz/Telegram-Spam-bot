from aiogram.dispatcher import FSMContext

from bot.base.objects import dispatcher
from bot.base.states import ChatSettingsEditQuantity, ChatSettingsEditInterval
from bot.base.states import ChatSettingsAddQuantity, ChatSettingsAddInterval
from bot.views.distribution.settings.helpers import update_message_quantity, update_message_interval
from aiogram import types


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=ChatSettingsAddInterval.waiting_for_interval)
async def process_add_interval(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer('Интервал должен быть положительным числом.')
        await state.set_state(ChatSettingsAddInterval.waiting_for_interval)
        return

    await update_message_interval(message, state)
    await message.answer('Интервал успешно установлен!')
    await state.reset_state(with_data=False)


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=ChatSettingsAddQuantity.waiting_for_quantity)
async def process_add_quantity(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer('Интервал должен быть положительным числом.')
        await state.set_state(ChatSettingsAddQuantity.waiting_for_quantity)
        return

    await update_message_quantity(message, state)
    await message.answer('Количество сообщений успешно установлено!')
    await state.reset_state(with_data=False)


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=ChatSettingsEditInterval.waiting_for_interval)
async def process_edit_interval(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer('Интервал должен быть положительным числом.')
        await state.set_state(ChatSettingsEditInterval.waiting_for_interval)
        return

    await update_message_interval(message, state)
    await message.answer('Интервал успешно изменён!')
    await state.reset_state(with_data=False)


@dispatcher.message_handler(content_types=types.ContentTypes.TEXT, state=ChatSettingsEditQuantity.waiting_for_quantity)
async def process_edit_quantity(message: types.Message, state: FSMContext):
    if not message.text.isdigit() or int(message.text) <= 0:
        await message.answer('Интервал должен быть положительным числом.')
        await state.set_state(ChatSettingsEditQuantity.waiting_for_quantity)
        return

    await update_message_quantity(message, state)
    await message.answer('Количество сообщений успешно изменено!')
    await state.reset_state(with_data=False)
