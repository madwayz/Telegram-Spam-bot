from app.settings import TOKEN
from aiogram.dispatcher import Dispatcher
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
