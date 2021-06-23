from aiogram.contrib.fsm_storage.redis import RedisStorage
from settings import TOKEN, REDIS_HOST
from aiogram.dispatcher import Dispatcher
from aiogram import Bot

from worker.model import UserBot

userbot = UserBot()
bot = Bot(TOKEN)
storage = RedisStorage(REDIS_HOST, 6379, db=5)
dispatcher = Dispatcher(bot, storage=storage)
