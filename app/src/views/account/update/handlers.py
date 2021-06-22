from aiogram import types

from src.base.objects import dispatcher, bot


@dispatcher.callback_query_handler(lambda call: call.data == 'edit_text_settings')
async def edit_text_settings(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    menu = EditTextSettingsMenu()
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )
    await AccountSettings.waiting_for_text.set()