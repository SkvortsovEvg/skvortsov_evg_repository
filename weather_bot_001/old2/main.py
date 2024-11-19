import asyncio
import requests
import os
from aiogram import Bot, types, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import TELEGRAM_BOT_TOKEN, OPEN_WEATHER_TOKEN, MOON_API
from list_to_image import output_list_to_image
from draw_picture import do_image
from pprint import pprint

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

kb = [
    [KeyboardButton(text="С пюрешкой")],
    [KeyboardButton(text="Без пюрешки")]
]

keyboard = ReplyKeyboardMarkup(keyboard=kb,
                               resize_keyboard=True,
                               input_field_placeholder="Выберите способ подачи")

HELP_COMMAND = """
<b>/start</b> - <em>старт бота</em>
<b>/help</b> - <em>список команд</em>
<b>/city</> - <em>по городу</em>
"""


@dp.message(Command("start"))
async def handle_start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Привет! Напиши мне город, а я пришлю погоду в этом городе.",
                                # "Помните о команде /help"
                           parse_mode="HTML",
                           )
    await message.delete()


@dp.message(Command("help"))
async def handle_help_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP_COMMAND,
                           parse_mode="HTML")
    await message.delete()


@dp.message(Command("city"))
async def handle_city_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text=HELP_COMMAND,
                           parse_mode="HTML")
    await message.delete()


@dp.message()
async def handle_get_weather(message: types.Message):
    try:

        weather_request = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&"
            f"appid={OPEN_WEATHER_TOKEN}&units=metric&lang=ru"
        )
        data_weather = weather_request.json()
        # pprint(data_weather)

        # Lat, lon — это сокращение от «latitude» и «longitude» (широта и долгота).
        # с.ш.>0, ю.ш.<0, в.д.>0, з.д.<0
        tmp_request = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={41.902695}&lon={12.496176}&"
            f"appid={OPEN_WEATHER_TOKEN}&units=metric&lang=ru"
        )
        tmp_weather = tmp_request.json()
        pprint(tmp_weather)

        moon_request = requests.get(
            f"https://api.ipgeolocation.io/astronomy?apiKey={MOON_API}&lat={data_weather['coord']['lat']}"
            f"&long={data_weather['coord']['lon']}"
        )
        data_moon = moon_request.json()
        our_weather = output_list_to_image(data_weather, data_moon)
        if our_weather != -1:
            filename_img = do_image(our_weather)
            await message.reply_photo(
                photo=types.FSInputFile(
                    path=filename_img,
                )
            )
        os.remove(filename_img)
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
