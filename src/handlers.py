from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from loader import bot
from db import User


class FSMStates(StatesGroup):
    set_value = State()


async def start_handler(msg: types.Message):
    try:
        user = User.get_by_id(msg.from_user.id)
        time_value = user.notification_time
        text = f'Привіт, {msg.from_user.full_name}!\n\n' \
               f'Сповіщення про початок пари приходитимуть за {time_value} хвилин. Щоб змінити його, напиши /settings.'
    except:
        User.create_user(msg.from_user.id, msg.chat.id, 5)
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


async def settings_handler(msg: types.Message, state: FSMContext):
    await state.set_state(FSMStates.set_value)

    text = 'Вкажи час, за який тебе треба попереджувати про початок пари у хвилинах.'

    await bot.send_message(msg.chat.id, text)


async def set_time_value(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        await state.finish()

        User.update_notification_time(
            id=msg.from_user.id, notification_time=int(msg.text))

        await bot.send_message(msg.chat.id, 'Нове значення записано.')
    else:
        await bot.send_message(msg.chat.id, 'Будь ласка, введіть ціле число.')


def setup(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(help_handler, commands=['help'])
    dp.register_message_handler(settings_handler, commands=['settings'])
    dp.register_message_handler(set_time_value, state=FSMStates.set_value)
