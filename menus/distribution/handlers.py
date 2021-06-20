from base.objects import dispatcher, bot
from aiogram import types


@dispatcher.callback_query_handler(lambda call: call.data == 'menu_distribution')
async def distribution(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Меню рассылок')