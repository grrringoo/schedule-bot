from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp, CommandSettings
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot import bot


class FSMStates(StatesGroup):
    set_value = State()


async def start_handler(msg: types.Message):
    users = None  # беремо усіх користувачів з бази даних
    if msg.from_user.id in users:
        time_value = None  # беремо значення часу для нагадування
        text = f'Привіт, {msg.from_user.full_name}!\n\n' \
               f'Сповіщення про початок пари приходитимуть за {time_value} хвилин. Щоб змінити його, напиши /settings.'
    else:
        # записуємо у бд нового користувача
        text = f'Вітаю, {msg.from_user.full_name}!\n' \
               f'Я бот, який може нагадувати про початок наступної пари з посиланням на неї.\n\n' \
               f'Ти можеш налаштувати за який час тобі надсилати нагадування. Для цього напиши /settings.\n' \
               f'Початкове значення — 5 хвилин.'
    await bot.send_message(msg.chat.id, text)


async def help_handler(msg: types.Message):
    text = 'Список команд:\n' \
           '/start — виведення заданого часу для нагадування\n' \
           '/settings — зміна часу для нагадування'
    await bot.send_message(msg.chat.id, text)


async def settings_handler(msg: types.Message):
    await FSMStates.set_value.set()
    text = 'Вкажи час, за який тебе треба попереджувати про початок пари у хвилинах.'
    await bot.send_message(msg.chat.id, text)


async def set_time_value(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        await state.finish()
        # записуємо значення у бд
        await bot.send_message(msg.chat.id, 'Нове значення записано.')
    else:
        await bot.send_message(msg.chat.id, 'Будь ласка, введіть ціле число.')


def setup(dp: Dispatcher):
    dp.register_message_handler(start_handler, CommandStart)
    dp.register_message_handler(help_handler, CommandHelp)
    dp.register_message_handler(settings_handler, CommandSettings)
    dp.message_handler(set_time_value, state=FSMStates.set_value)
