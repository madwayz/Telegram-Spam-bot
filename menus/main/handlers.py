from menus.main.menu import MainMenu
from base.objects import dispatcher
from aiogram.types import Message


@dispatcher.message_handler(commands=['start'])
async def send_welcome_page(message: Message):
    menu = MainMenu()
    await message.answer(
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )
