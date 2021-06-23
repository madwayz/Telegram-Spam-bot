from aiogram.dispatcher import FSMContext
from bot.base.objects import dispatcher, bot
from aiogram import types
from bot.base.states import AccountSettings
from bot.views.account.settings.menu import AccountTextSettingsMenu, EditTextSettingsMenu


@dispatcher.callback_query_handler(lambda call: call.data == 'text_settings')
async def text_settings(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    menu = AccountTextSettingsMenu(await state.get_data())
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )


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


@dispatcher.callback_query_handler(lambda call: call.data == 'cancel_edit_text_settings', state='*')
async def cancel_edit_text_settings(callback_query: types.CallbackQuery, state: FSMContext):
    await state.reset_state(with_data=False)
    await text_settings(callback_query, state)
