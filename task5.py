from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State, default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import Command, CommandStart, StateFilter
from config import BOT_TOKEN

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)


class FSMFillForm(StatesGroup):
    fill_city = State()
    fill_weather = State()


@dp.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text="Привет. Пройдите небольшой опрос, пожалуйста!\n"
                              "Вы можете прервать опрос, послав команду /stop.\n"
                              "В каком городе вы живёте?")
    await state.set_state(FSMFillForm.fill_city)


@dp.message(Command(commands=['stop']), ~StateFilter(default_state))
async def stop(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Всего доброго!")


@dp.message(StateFilter(FSMFillForm.fill_city), F.text.isalpha())
async def process_city_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=f"Какая погода в городе {message.text}?")
    await state.set_state(FSMFillForm.fill_weather)


@dp.message(StateFilter(FSMFillForm.fill_weather))
async def process_weather_sent(message: Message, state: FSMContext):
    await state.update_data(weather=message.text)
    await message.answer(text="Спасибо за участие в опросе! Всего доброго!")
    await state.clear()


@dp.message(Command(commands=['skip']), StateFilter(FSMFillForm.fill_city))
async def process_city_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=f"Какая погода у вас за окном?")
    await state.set_state(FSMFillForm.fill_weather)


if __name__ == '__main__':
    dp.run_polling(bot)
