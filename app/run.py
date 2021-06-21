from aiogram import Dispatcher
from aiogram.utils import executor
from src.base.objects import dispatcher
from src.menus.account.chat_settings.handler_registers import register_handlers_edit_text
import src.menus


async def shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()

register_handlers_edit_text(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dispatcher, on_shutdown=shutdown(dispatcher))
