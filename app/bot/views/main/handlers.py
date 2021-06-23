from aiogram.dispatcher import FSMContext

from bot.views.main.menu import MainMenu
from bot.base.objects import dispatcher
from aiogram import types


@dispatcher.message_handler(commands=['start'], state='*')
async def send_welcome_page(message: types.Message, state: FSMContext):
    menu = MainMenu()
    await message.answer(
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )
    await state.finish()


@dispatcher.callback_query_handler(lambda call: call.data == 'main_menu', state='*')
async def main_menu(callback_query: types.CallbackQuery, state: FSMContext):
    await send_welcome_page(callback_query.message, state)
