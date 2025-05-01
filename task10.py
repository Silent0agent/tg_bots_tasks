import requests
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.types import BufferedInputFile
from config import BOT_TOKEN

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_apikey = "8013b162-6b42-4997-9691-77b7074026e0"
map_api_server = "https://static-maps.yandex.ru/v1"
map_apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Здравствуйте. Введите топоним или адрес объекта, который вы хотите найти.')


@dp.message()
async def process(message: Message):
    toponym = message.text

    geocoder_params = {
        "apikey": geocoder_apikey,
        "geocode": toponym,
        "format": "json"}
    geocoder_response = requests.get(geocoder_api_server, params=geocoder_params)
    if not geocoder_response:
        await message.answer(
            f"Ошибка выполнения запроса:\n{geocoder_response.url}\nHttp статус: {geocoder_response.status_code} ( {geocoder_response.reason} )")
        return
    json_geocoder_response = geocoder_response.json()
    if not json_geocoder_response["response"]["GeoObjectCollection"]["featureMember"]:
        await message.answer('Ничего не найдено')
        return
    toponym = json_geocoder_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coordinates = ','.join(toponym["Point"]["pos"].split())
    full_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]

    map_params = {"apikey": map_apikey,
                  "ll": toponym_coordinates,
                  "z": "16",
                  "pt": f"{toponym_coordinates},pm2rdm"}
    map_response = requests.get(map_api_server, params=map_params)
    if not map_response:
        await message.answer(
            f"Ошибка выполнения запроса:\n{map_response.url}\nHttp статус: {map_response.status_code} ( {map_response.reason} )")
        return
    im = map_response.content
    image_file = BufferedInputFile(
        file=im,
        filename="map.jpg"
    )
    await message.answer_photo(photo=image_file,
                               caption=full_address)


if __name__ == '__main__':
    dp.run_polling(bot)
