import asyncio
import os
import requests
import datetime
from aiogram import Bot, types, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import ContentType, Message
from config import TELEGRAM_BOT_TOKEN, OPEN_WEATHER_TOKEN, MOON_API

from images_pillow import do_pic

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


def read_weather_list(city_text):
    def wind_direction(deg):
        if 0 < deg < 90:
            return "СВ"
        if deg == 90:
            return "С"
        if 90 < deg < 180:
            return "СЗ"
        if deg == 180:
            return "З"
        if 180 < deg < 270:
            return "ЮЗ"
        if deg == 270:
            return "Ю"
        if 270 < deg < 360:
            return "ЮВ"
        if deg == 0:
            return "В"
        return "Error"

    city_in_country = {
        "RU": "РФ",
        "MX": "Мексика",
        "US": "США",
        "KZ": "Казахстан",
        "FR": "Франция",
        "DE": "Германия",
        "BR": "Бразилия",
        "ES": "Испания",
        "GB": "Великобритания",
        "AU": "Австралия",
        "GR": "Греция",
        "TR": "Турция",
        "AT": "Австрия",
        "UA": "Украина",
        "BY": "Беларусь",
        "CZ": "Чехия",
        "CN": "Китай",
        "KR": "Юж.Корея",
        "KP": "Сев.Корея",
        "AR": "Аргентина",
    }
    try:
        weather_request = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city_text}&appid={OPEN_WEATHER_TOKEN}&units=metric&lang=ru"
        )
        data = weather_request.json()

        our_weather = []
        city_list = []
        weather_list = []
        city = data["name"]
        city_list.append(city)

        city_coords = []
        city_lat = data["coord"]["lat"]
        city_lon = data["coord"]["lon"]
        country = data["sys"]["country"]

        if country in city_in_country:
            city += ', ' + city_in_country[country]
            city_list.append(city_in_country[country])
        else:
            city_list.append("Error")
        city_coords.append(city_lat)
        city_coords.append(city_lon)
        city_list.append(city_coords)

        our_weather.append(city_list)

        temp = round(data["main"]["temp"])
        weather_description = data["weather"][0]["main"]
        weather_description_list = []

        weather_description_list.append(data["weather"][0]["description"])
        weather_description_list.append(data["weather"][0]["icon"])
        weather_description_list.append(data["weather"][0]["id"])
        weather_description_list.append(data["weather"][0]["main"])

        humidity = data["main"]["humidity"]
        pressure = round(data["main"]["pressure"] * 0.75)
        wind = round(data["wind"]["speed"])
        wind_direct = wind_direction(data["wind"]["deg"])
        weather_list.append(temp)
        weather_list.append(wind)
        weather_list.append(pressure)
        weather_list.append(humidity)
        weather_list.append(wind_direct)

        our_weather.append(weather_list)
        our_weather.append(weather_description_list)
        sun_list = []
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(
            data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        sun_list.append(sunrise_timestamp.time())
        sun_list.append(sunset_timestamp.time())
        sun_list.append(length_of_the_day)
        sun_list.append(sunrise_timestamp)
        sun_list.append(sunset_timestamp)
        our_weather.append(sun_list)

        moon_request = requests.get(
            f"https://api.ipgeolocation.io/astronomy?apiKey={MOON_API}&lat={our_weather[0][2][0]}&long={our_weather[0][2][1]}"
        )
        data_moon = moon_request.json()
        about_moon = []
        about_moon.append(data_moon['moonrise'])
        about_moon.append(data_moon['moonset'])
        about_moon.append(data_moon['moon_distance'])
        our_weather.append(about_moon)

        return our_weather
    except:
        return -1
        # await message.reply("\U00002620 Проверьте название города \U00002620")


@dp.message(Command("start"))
async def handle_start_command(message: types.Message):
    # await message.reply("Привет! Напиши мне город, а я пришлю погоду в этом городе.")
    await bot.send_message(chat_id=message.chat.id,
                           text="Привет! Напиши мне город из России, а я пришлю погоду в этом городе.")


# @dp.message(Command("pics"))
# async def handle_send_image(message: types.Message):
#     file_path = "images/output/output_001.jpg"
#     await message.reply_photo(
#         photo=types.FSInputFile(
#             path=file_path,
#         )
#     )

@dp.message()
async def handle_get_weather(message: types.Message):
    input_list = read_weather_list(message.text)
    if input_list != -1:
        filename_pic = do_pic(input_list)
        await message.reply_photo(
            photo=types.FSInputFile(
                path=filename_pic,
            )
        )
        os.remove(filename_pic)
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text="Что-то с названием города не так, напишите его правильно")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
