import json

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from random import shuffle
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_dict: dict[int, dict[str, str | int | bool]] = {}


def get_tests(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tests = data["test"]
    shuffle(tests)
    return tests


@dp.message(CommandStart())
async def start(message: Message):
    user_dict[message.from_user.id] = {}
    user_dict[message.from_user.id]['num'] = 0
    user_dict[message.from_user.id]['true_sum'] = 0
    user_dict[message.from_user.id]['tests'] = get_tests('questions.json')
    await message.answer(
        f"Здравствуйте. Предлагаю вам пройти тест на знание исторических дат. Давайте начнём.\n{user_dict[message.from_user.id]['tests'][0]['question']}")


@dp.message(Command(commands=['stop']))
async def stop(message: Message):
    del user_dict[message.from_user.id]
    await message.answer('До свидания')


@dp.message()
async def process(message: Message):
    if message.from_user.id in user_dict:
        if user_dict[message.from_user.id]['num'] >= len(user_dict[message.from_user.id]['tests']):
            await message.answer(
                f"Вы прошли тест. Ваш результат: {user_dict[message.from_user.id]['true_sum']} "
                f"правильных ответов из {len(user_dict[message.from_user.id]['tests'])}.\n"
                f"Если хотите пройти тест еще раз введите команду /start.")
            return
        if message.text == user_dict[message.from_user.id]['tests'][user_dict[message.from_user.id]['num']]['response']:
            user_dict[message.from_user.id]['true_sum'] += 1
        user_dict[message.from_user.id]['num'] += 1
        if user_dict[message.from_user.id]['num'] != len(user_dict[message.from_user.id]['tests']):
            await message.answer(
                user_dict[message.from_user.id]['tests'][user_dict[message.from_user.id]['num']]['question'])
        else:
            await message.answer(
                f"Вы прошли тест. Ваш результат: {user_dict[message.from_user.id]['true_sum']} "
                f"правильных ответов из {len(user_dict[message.from_user.id]['tests'])}.\n"
                f"Если хотите пройти тест еще раз введите команду /start.")


if __name__ == '__main__':
    dp.run_polling(bot)
