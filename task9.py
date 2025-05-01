from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import CommandStart
from translator_funcs import translate_text
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_dict: dict[int, dict[str, str | int | bool]] = {}

languages = {'ru': 'русский',
             'en': 'английский'}
switch_language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Переводить с английского на русский', callback_data='en_ru')],
                     [InlineKeyboardButton(text='Переводить с русского на английский', callback_data='ru_en')]])


@dp.message(CommandStart())
async def start(message: Message):
    user_dict[message.from_user.id] = {}
    user_dict[message.from_user.id]['source'] = 'ru'
    user_dict[message.from_user.id]['target'] = 'en'
    await message.answer(
        f"Здравствуйте. Введите текст для перевода. Сейчас текст переводится с языка "
        f"{languages[user_dict[message.from_user.id]['source']]} на язык "
        f"{languages[user_dict[message.from_user.id]['target']]}.", reply_markup=switch_language_keyboard)


@dp.callback_query(F.data.in_(['en_ru', 'ru_en']))
async def switch_language(callback: CallbackQuery):
    if user_dict.get(callback.from_user.id):
        user_dict[callback.from_user.id]['source'] = callback.data.split('_')[0]
        user_dict[callback.from_user.id]['target'] = callback.data.split('_')[1]
        await callback.answer()
        await callback.message.answer(
            f"Теперь текст переводится с языка {languages[user_dict[callback.from_user.id]['source']]} "
            f"на язык {languages[user_dict[callback.from_user.id]['target']]}.",
            reply_markup=switch_language_keyboard)
    else:
        await callback.answer()


@dp.message()
async def translate(message: Message):
    if user_dict.get(message.from_user.id):
        text_to_translate = message.text
        source_language = user_dict[message.from_user.id]['source']
        target_language = user_dict[message.from_user.id]['target']
        translation = translate_text(text_to_translate, source_language, target_language)
        if translation:
            await message.answer(translation, reply_markup=switch_language_keyboard)
        else:
            await message.answer('Не удалось перевести')


if __name__ == '__main__':
    dp.run_polling(bot)
