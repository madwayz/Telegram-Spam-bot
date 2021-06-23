from aiogram import Dispatcher
from aiogram.utils import executor
from bot.base.objects import dispatcher
import bot.views


async def shutdown(dp: Dispatcher):
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dispatcher, on_shutdown=shutdown, skip_updates=True)
