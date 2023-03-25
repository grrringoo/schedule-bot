from aiogram import executor
import logging

from handlers import setup
from loader import dp, ADMINS


async def on_startup(dp):
    setup(dp)
    await notify_admins()


async def notify_admins():
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, 'Бота запущено.')
        except Exception as e:
            logging.exception(e)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
