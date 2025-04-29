from aiogram import Bot, Dispatcher
from aiogram.types import Message
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message()
async def send_echo(message: Message):
    msg_txt = message.text
    await message.answer(f'Я получил сообщение {msg_txt}')


if __name__ == '__main__':
    dp.run_polling(bot)
