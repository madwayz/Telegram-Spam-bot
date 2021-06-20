from aiogram.utils import executor
from src.base.objects import dispatcher
import src.menus

if __name__ == '__main__':
    executor.start_polling(dispatcher)
