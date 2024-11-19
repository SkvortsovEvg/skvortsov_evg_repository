import asyncio
import requests
import os
from aiogram import Bot, types, Dispatcher
from aiogram.filters import Command, CommandObject
from config import TELEGRAM_BOT_TOKEN, OPEN_WEATHER_TOKEN, MOON_API
from list_to_image import output_list_to_image
from draw_picture import do_image
from weather_3h import output_json_big_3h_list
from do_big_image import do_big_picture
from convert_string import convert_string2weather
#from coord_to_lat_lon import coord_to_lat_lon
#from pprint import pprint

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

HELP_COMMAND = """
<b>/start</b> - <em>старт бота</em>
<b>/help</b> - <em>список команд</em>
<b>/coords</b> - <em>по координатам через запятую: /coords широта, долгота</em>
<b>/weather3h</b> - <em>погода через каждые 3 часа на 24 часа: /weather3h Москва</em>

Можно просто узнать о погоде в городе, написав его название.
"""

COORDINATES_WORD = """
\nНеобходимо поступить так: /coords широта, долгота (через запятую)
"""


@dp.message(Command("start"))
async def handle_start_command(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text="Привет! Напиши мне город, а я пришлю погоду в этом городе.\nПомните о команде /help",
                           parse_mode="HTML",
                           )
    await message.delete()


@dp.message(Command("help"))
async def handle_104220209_75535(message: types.Message):
    #help_command(message: types.Message):
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


@dp.message(Command("coords"))
async def handle_coords_command(message: types.Message,
                                command: CommandObject):
    if command.args is None:
        await message.answer("Введите координаты" + COORDINATES_WORD)
        return
    try:
        message_list = command.args.split(', ')
        if len(message_list) != 2:
            await message.answer("Вы ввели одну координату." + COORDINATES_WORD)
            return
        else:
            try:
                lat = float(message_list[0])
                lon = float(message_list[1])
            # lat, lon — это сокращение от «latitude» и «longitude» (широта и долгота).
            # с.ш.>0, ю.ш.<0, в.д.>0, з.д.<0
            except ValueError:
                await message.answer("Неправильно введены координаты." + COORDINATES_WORD)
                return
        data_request = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&"
            f"appid={OPEN_WEATHER_TOKEN}&units=metric&lang=ru"
        )

        data_weather = data_request.json()
        if data_weather["name"] != "":
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
        else:
            await message.answer("Такого города нет! Правильно запишите координаты." + COORDINATES_WORD)
            return
    except ValueError:
        await message.answer("Неправильно введены координаты." + COORDINATES_WORD)
        return


@dp.message(Command("weather3h"))
async def handle_weather3h_command(message: types.Message,
                                   command: CommandObject):
    if command.args.strip() is None:
        await message.answer("Введите город:\n/weather3h Москва")
        return
    else:
        try:
            city = convert_string2weather(command.args.strip())
            if city != -1:
                # print(command.args)
                # city = command.args.islower()
                weather_request = requests.get(
                    f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPEN_WEATHER_TOKEN}"
                    f"&units=metric&lang=ru"
                )
                data_weather = weather_request.json()
                # pprint(data_weather)
                filename_img = do_big_picture(output_json_big_3h_list(data_weather))
                await message.reply_photo(
                    photo=types.FSInputFile(
                        path=filename_img,
                    )
                )
                os.remove(filename_img)
                return
            else:
                await message.reply("\U00002620 Проверьте название города или страны. "
                                    "Незабудьте про запятую. \U00002620\nПосмотрите в /help",
                                    parse_mode="HTML")
        except:
            await message.reply("\U00002620 Проверьте название города \U00002620\nПосмотрите в /help",
                                parse_mode="HTML")
            return


@dp.message()
async def handle_get_weather(message: types.Message):
    try:
        city = convert_string2weather(message.text.strip())
        if city != -1:
            weather_request = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={city}&"
                f"appid={OPEN_WEATHER_TOKEN}&units=metric&lang=ru"
            )
            data_weather = weather_request.json()
            # pprint(data_weather)

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
        else:
            await message.reply("\U00002620 Проверьте название города или страны. "
                                "Незабудьте про запятую. \U00002620\nПосмотрите в /help",
                                parse_mode="HTML")
    except:
        await message.reply("\U00002620 Проверьте название города \U00002620\nПосмотрите в /help",
                            parse_mode="HTML")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
