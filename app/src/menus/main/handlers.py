from src.menus.main.menu import MainMenu
from src.base.objects import dispatcher, bot
from aiogram import types


@dispatcher.message_handler(commands=['start'])
async def send_welcome_page(message: types.Message):
    menu = MainMenu()
    await message.answer(
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )


@dispatcher.callback_query_handler(lambda call: call.data == 'back_to_main_menu')
async def switch_account(callback_query: types.CallbackQuery):
    menu = MainMenu()
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text=menu.get_text(),
        reply_markup=menu.get_keyboard()
    )