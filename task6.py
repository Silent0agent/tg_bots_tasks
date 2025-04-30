from aiogram import Bot, Dispatcher, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, StateFilter, or_f
from config import BOT_TOKEN

storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=storage)


class FSMHallform(StatesGroup):
    enter = State()
    hall1 = State()
    hall2 = State()
    hall3 = State()
    hall4 = State()
    exit = State()


@dp.message(CommandStart())
async def enter(message: Message, state: FSMContext):
    text = 'Добро пожаловать! Пожалуйста, сдайте верхнюю одежду в гардероб!'
    keyboard = InlineKeyboardMarkup(inline_keyboard=
    [[InlineKeyboardButton(
        text='Пройти в зал 1 - находки X века',
        callback_data='hall1')]
    ])
    await message.answer(text,
                         reply_markup=keyboard)
    await state.set_state(FSMHallform.enter)


@dp.callback_query(or_f(StateFilter(FSMHallform.enter),
                        StateFilter(FSMHallform.hall3), StateFilter(FSMHallform.hall4)),
                   F.data == 'hall1')
async def process_start_command(callback: CallbackQuery, state: FSMContext):
    text = "Зал 1 - находки X века"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Перейти в зал 2 - находки XI века', callback_data='hall2')],
                         [InlineKeyboardButton(text='Пройти к выходу', callback_data='exit')]])
    await callback.answer()
    await callback.message.answer(text=text, reply_markup=keyboard)
    await state.set_state(FSMHallform.hall1)


@dp.callback_query(StateFilter(FSMHallform.hall1), F.data == 'hall2')
async def process_start_command(callback: CallbackQuery, state: FSMContext):
    text = "Зал 2 - находки XI века"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Перейти в зал 3 - находки XII века', callback_data='hall3')]])
    await callback.answer()
    await callback.message.answer(text=text, reply_markup=keyboard)
    await state.set_state(FSMHallform.hall2)


@dp.callback_query(StateFilter(FSMHallform.hall2), F.data == 'hall3')
async def process_start_command(callback: CallbackQuery, state: FSMContext):
    text = "Зал 3 - находки XII века"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Перейти в зал 4 - находки XIII века', callback_data='hall4')],
                         [InlineKeyboardButton(text='Перейти в зал 1 - находки X века', callback_data='hall1')]])
    await callback.answer()
    await callback.message.answer(text=text, reply_markup=keyboard)
    await state.set_state(FSMHallform.hall3)


@dp.callback_query(StateFilter(FSMHallform.hall3), F.data == 'hall4')
async def process_start_command(callback: CallbackQuery, state: FSMContext):
    text = "Зал 4 - находки XIII века"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text='Перейти в зал 1 - находки X века', callback_data='hall1')]])
    await callback.answer()
    await callback.message.answer(text=text, reply_markup=keyboard)
    await state.set_state(FSMHallform.hall4)


@dp.callback_query(StateFilter(FSMHallform.hall1), F.data == 'exit')
async def exit(callback: CallbackQuery, state: FSMContext):
    text = 'Всего доброго, не забудьте забрать верхнюю одежду в гардеробе!'
    await callback.answer()
    await callback.message.answer(text)
    await state.clear()


if __name__ == '__main__':
    dp.run_polling(bot)
