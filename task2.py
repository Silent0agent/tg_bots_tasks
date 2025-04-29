from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands='time'))
async def send_time(message: Message):
    current_time = datetime.now().time()
    time_str = current_time.strftime("%H:%M:%S")
    await message.answer(f'{time_str}')


@dp.message(Command(commands='date'))
async def send_date(message: Message):
    current_date = datetime.now().date()
    date_str = current_date.strftime("%Y-%m-%d")
    await message.answer(f'{date_str}')


if __name__ == '__main__':
    dp.run_polling(bot)
