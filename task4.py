import asyncio
from random import randint
from typing import Union
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_tasks = {}


@dp.message(Command(commands=['start']))
@dp.callback_query(F.data == 'back')
async def start(event: Union[Message, CallbackQuery]):
    keyboard = InlineKeyboardMarkup(inline_keyboard=
                                    [[InlineKeyboardButton(text='Бросить кубик', callback_data='dice')],
                                     [InlineKeyboardButton(text='Поставить таймер', callback_data='timer')]])
    if isinstance(event, Message):
        await event.answer('Выберите команду', reply_markup=keyboard)
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer('Выберите команду', reply_markup=keyboard)


@dp.message(Command(commands=['dice']))
@dp.callback_query(F.data == 'dice')
async def dice(event: Union[Message, CallbackQuery]):
    keyboard = InlineKeyboardMarkup(inline_keyboard=
                                    [[InlineKeyboardButton(text='кинуть один шестигранный кубик',
                                                           callback_data='one_six')],
                                     [InlineKeyboardButton(text='кинуть 2 шестигранных кубика одновременно',
                                                           callback_data='two_six')],
                                     [InlineKeyboardButton(text='кинуть 20-гранный кубик', callback_data='one_twenty')],
                                     [InlineKeyboardButton(text='вернуться назад', callback_data='back')]])
    if isinstance(event, Message):
        await event.answer('Какой кубик бросить?', reply_markup=keyboard)
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer('Какой кубик бросить?',
                                   reply_markup=InlineKeyboardMarkup(inline_keyboard=
                                   [[InlineKeyboardButton(
                                       text='Кинуть один шестигранный кубик',
                                       callback_data='one_six')],
                                       [InlineKeyboardButton(
                                           text='Кинуть 2 шестигранных кубика одновременно',
                                           callback_data='two_six')],
                                       [InlineKeyboardButton(
                                           text='Кинуть 20-гранный кубик',
                                           callback_data='one_twenty')],
                                       [InlineKeyboardButton(
                                           text='Вернуться назад',
                                           callback_data='back')]]))


@dp.callback_query(F.data.in_(['one_six', 'two_six', 'one_twenty']))
async def cube(callback: CallbackQuery):
    mode = callback.data
    await callback.answer()
    if mode == 'one_six':
        await callback.message.answer(str(randint(1, 6)), reply_markup=callback.message.reply_markup)
    elif mode == 'two_six':
        await callback.message.answer(str(randint(1, 6)) + ' ' + str(randint(1, 6)),
                                      reply_markup=callback.message.reply_markup)
    elif mode == 'one_twenty':
        await callback.message.answer(str(randint(1, 20)), reply_markup=callback.message.reply_markup)


@dp.message(Command(commands=['timer']))
@dp.callback_query(F.data == 'timer')
async def timer(event: Union[Message, CallbackQuery]):
    keyboard = InlineKeyboardMarkup(inline_keyboard=
                                    [[InlineKeyboardButton(text='30 секунд',
                                                           callback_data='thirty_sec')],
                                     [InlineKeyboardButton(text='1 минута',
                                                           callback_data='one_min')],
                                     [InlineKeyboardButton(text='5 минут',
                                                           callback_data='five_min')],
                                     [InlineKeyboardButton(
                                         text='вернуться назад',
                                         callback_data='back')]])
    if isinstance(event, Message):
        await event.answer('Выберите время', reply_markup=keyboard)
    elif isinstance(event, CallbackQuery):
        await event.answer()
        await event.message.answer('Выберите время', reply_markup=keyboard)


@dp.callback_query(F.data.in_(['thirty_sec', 'one_min', 'five_min']))
async def cube(callback: CallbackQuery):
    mode = callback.data
    user_id = callback.from_user.id
    if mode == 'thirty_sec':
        seconds = 30
    elif mode == 'one_min':
        seconds = 60
    elif mode == 'five_min':
        seconds = 300
    times = {'thirty_sec': 'тридцать секунд',
             'one_min': 'одну минуту',
             'five_min': 'пять минут'}
    task = asyncio.create_task(send_timer_notification(user_id, seconds))
    user_tasks[user_id] = task
    await callback.answer()
    await callback.message.answer(f'Засек {times[mode]}', reply_markup=InlineKeyboardMarkup(inline_keyboard=
    [[InlineKeyboardButton(
        text='Отменить',
        callback_data='cancel')]]))


@dp.message(Command(commands=['cancel']))
@dp.callback_query(F.data == 'cancel')
async def cancel_timer(event: Union[Message, CallbackQuery]):
    user_id = event.from_user.id
    # if isinstance(event, Message):
    if user_id in user_tasks:
        user_tasks[user_id].cancel()
        del user_tasks[user_id]
        if isinstance(event, Message):
            await event.answer("Таймер отменен!")
        else:
            await event.answer()
            await event.message.answer("Таймер отменен!")
    else:
        if isinstance(event, Message):
            await event.answer("Нет активных таймеров.")
        else:
            await event.answer()
            await event.message.answer("Нет активных таймеров.")


async def send_timer_notification(user_id: int, seconds: int):
    await asyncio.sleep(seconds)
    times = {30: 'Тридцать секунд прошло',
             60: 'Одна минута прошла',
             300: 'Пять минут прошло'}
    await bot.send_message(user_id, f'{times[seconds]}')


if __name__ == '__main__':
    dp.run_polling(bot)
