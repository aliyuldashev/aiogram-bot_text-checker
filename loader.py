from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import config
bot = Bot(token=config.BOT_TOKEN)
storage = MemoryStorage()
db = Dispatcher(bot, storage=storage)