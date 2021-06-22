from src.views.main.menu import MainMenu
from src.base.objects import dispatcher
from aiogram import types


@dispatcher.message_handler(commands=['start'])
async def send_welcome_page(message: types.Message):
    menu = MainMenu()
    await message.answer(
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )


@dispatcher.callback_query_handler(lambda call: call.data == 'main_menu')
async def main_menu(callback_query: types.CallbackQuery):
    await send_welcome_page(callback_query.message)
