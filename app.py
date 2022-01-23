from aiogram import executor
from loader import db
from main.main import *
if __name__ == "__main__":
    executor.start_polling(db)