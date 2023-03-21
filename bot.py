import logging
import os

from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

from handlers import setup

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def on_startup():
    setup(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup())
