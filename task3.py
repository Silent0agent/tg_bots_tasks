import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['set_timer']))
async def set_timer(message: Message):
    full_text = message.text
    parts = full_text.split()
    if len(parts) > 1 and parts[1].isdigit():
        seconds = int(parts[1])
        user_id = message.from_user.id
        await message.reply(f"Таймер установлен на {seconds} секунд")
        task = asyncio.create_task(send_timer_notification(user_id, seconds))


async def send_timer_notification(user_id: int, seconds: int):
    await asyncio.sleep(seconds)
    await bot.send_message(user_id, f'{seconds} секунд прошло')


if __name__ == '__main__':
    dp.run_polling(bot)
