import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dotenv import load_dotenv

load_dotenv()

storage = MemoryStorage()

API_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = [562821454, 923231397]

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,
                    )

bot = Bot(token=API_TOKEN, disable_web_page_preview=True)
dp = Dispatcher(bot, storage=storage)
