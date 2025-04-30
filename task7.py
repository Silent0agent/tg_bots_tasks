from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from config import BOT_TOKEN

POEM = """Я помню чудное мгновенье:
Передо мной явилась ты,
Как мимолетное виденье,
Как гений чистой красоты.
В томленьях грусти безнадежной,
В тревогах шумной суеты,
Звучал мне долго голос нежный
И снились милые черты.
Шли годы. Бурь порыв мятежный
Рассеял прежние мечты,
И я забыл твой голос нежный,
Твои небесные черты.
В глуши, во мраке заточенья
Тянулись тихо дни мои
Без божества, без вдохновенья,
Без слез, без жизни, без любви.
Душе настало пробужденье:
И вот опять явилась ты,
Как мимолетное виденье,
Как гений чистой красоты.
И сердце бьется в упоенье,
И для него воскресли вновь
И божество, и вдохновенье,
И жизнь, и слезы, и любовь."""
poem_list = POEM.split('\n')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_dict = {}


@dp.message(CommandStart())
async def start(message: Message):
    user_dict[message.from_user.id] = 1
    await message.answer(poem_list[user_dict[message.from_user.id] - 1])


@dp.message(Command(commands=['stop']))
async def stop(message: Message):
    del user_dict[message.from_user.id]
    await message.answer('До свидания.')


@dp.message(Command(commands=['suphler']))
async def sufler(message: Message):
    await message.answer(poem_list[user_dict.get(message.from_user.id)])


@dp.message()
async def process(message: Message):
    if user_dict.get(message.from_user.id) and user_dict.get(message.from_user.id) < len(poem_list) - 1:
        if message.text == poem_list[user_dict.get(message.from_user.id)]:
            user_dict[message.from_user.id] += 2
            await message.answer(poem_list[user_dict[message.from_user.id] - 1])
        else:
            await message.answer('Нет, не так')
            await sufler(message)
    if user_dict.get(message.from_user.id) >= len(poem_list) - 1:
        await message.answer(
            'Поздравляю, стихотворение закончилось! Я рад! Если хотите попробовать еще раз, пришлите команду /start')


if __name__ == '__main__':
    dp.run_polling(bot)
