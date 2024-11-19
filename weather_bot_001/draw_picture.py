import datetime
from datetime import date
from PIL import Image, ImageDraw, ImageFont
from list_to_draw import list_2_text_in_draw
from moon_phase import moon_phase
from time_of_day import time_of_day
from lat_lon import lat_lon_label
from pictures import (filename_temperature, filename_time_of_day, filename_wind, filename_interface,
                      filename_moon_phase, color_label, weather_conditions)
from sign_temp import sign_temperature
from weather_descriptions import weather_descriprions_text

DIVIDER_SIZE = 25  # делитель при изменении размера картинок в интерфейсе
DIVIDER_SIZE_WC = 1.75
DIVIDER_SIZE_TEMPERATURE = 11
DIVIDER_SIZE_MOON = 15
MODE_FOR_OPEN_PICTURES = 'r'

input_list = [['Буэнос-Айрес', 'Аргентина', [-34.6132, -58.3772]],
              [22, 22, 24, 22],
              [3, 'СВ'],
              [762, 72],
              ['облачно с прояснениями', '01d', 800, 'Clear'],
              [datetime.time(11, 37, 39),
               datetime.time(2, 6, 12),
               datetime.timedelta(seconds=52113),
               datetime.datetime(2023, 12, 22, 11, 37, 39),
               datetime.datetime(2023, 12, 23, 2, 6, 12)],
              ['16:00', '02:10']]

fonts = (
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=24),
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=16),
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=12),
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=55),
)


def do_image(input_list):
    def icon_wind(input_list):
        if 0 <= input_list[2][0] < 5:
            return filename_wind[0]
        elif input_list[2][0] < 15:
            return filename_wind[1]
        else:
            return filename_wind[2]
        return -1

    def icon_temperature(input_list):
        if input_list[1][0] >= 35:
            return filename_temperature[0]
        elif 0 < input_list[1][0] < 35:
            return filename_temperature[1]
        elif -25 < input_list[1][0] <= 0:
            return filename_temperature[2]
        else:
            return filename_temperature[3]
        return -1

    # определяем иконку погоды
    weather_icon = input_list[4][1]
    if weather_icon in weather_conditions:
        filename_weather_conditions = weather_conditions[weather_icon]
    # день или ночь: 0 или 1
    time_of_day_now = time_of_day(input_list)
    # выбор цвета
    color = color_label[time_of_day_now]
    # грузим фон и иконку погоды
    img_time_of_day = Image.open(filename_time_of_day[time_of_day_now], MODE_FOR_OPEN_PICTURES)
    img_weather_conditions = Image.open(filename_weather_conditions, MODE_FOR_OPEN_PICTURES)
    img_weather_conditions = img_weather_conditions.resize((
        int(img_weather_conditions.width // DIVIDER_SIZE_WC), int(img_weather_conditions.height // DIVIDER_SIZE_WC)))

    all_images = []
    length_filename_interface = len(filename_interface)
    # открытие изображений filename_interface
    for i in range(length_filename_interface):
        all_images.append(Image.open(filename_interface[i], MODE_FOR_OPEN_PICTURES))
        all_images[i] = all_images[i].resize(
            (all_images[i].height // DIVIDER_SIZE, all_images[i].width // DIVIDER_SIZE))

    # создание нового изображения
    text_img = Image.new('RGBA', (img_time_of_day.width, img_time_of_day.height), (0, 0, 0, 0))
    # обои
    text_img.paste(img_time_of_day, (0, 0))
    # сверху
    text_img.paste(img_weather_conditions, (280, 25), mask=img_weather_conditions)

    # вставляем из all_images картинки интерфейса
    length_all_images = len(all_images)
    all_images_weight = 175
    for i in range(length_all_images):
        if i < 2:
            text_img.paste(all_images[i], (10, all_images_weight), all_images[i])
            all_images_weight += 25
        if 2 <= i < 5:
            if i == 2:
                all_images_weight = 150
            text_img.paste(all_images[i], (150, all_images_weight), all_images[i])
            all_images_weight += 25
        if 5 <= i < length_all_images:
            if i == 5:
                all_images_weight = 150
            text_img.paste(all_images[i], (260, all_images_weight), all_images[i])
            all_images_weight += 25

    # значок температуры
    img_temperature = Image.open(icon_temperature(input_list), MODE_FOR_OPEN_PICTURES)
    img_temperature = img_temperature.resize((img_temperature.height // DIVIDER_SIZE_TEMPERATURE,
                                              img_temperature.width // DIVIDER_SIZE_TEMPERATURE))
    text_img.paste(img_temperature, (10, 30), img_temperature)

    # значок флага ветра
    img_wind = Image.open(icon_wind(input_list), MODE_FOR_OPEN_PICTURES)
    img_wind = img_wind.resize((img_wind.height // DIVIDER_SIZE, img_wind.width // DIVIDER_SIZE))
    text_img.paste(img_wind, (10, 150), img_wind)

    # работа с Луной (фазу Луны показывает)
    date_now = date.today()
    open_moon_picture = moon_phase(date_now.year, date_now.month, date_now.day)
    if open_moon_picture != -1:
        moon_img = Image.open(filename_moon_phase[open_moon_picture], MODE_FOR_OPEN_PICTURES)
        moon_img = moon_img.resize((moon_img.height // DIVIDER_SIZE_MOON, moon_img.width // DIVIDER_SIZE_MOON))
        text_img.paste(moon_img, (325, 200), moon_img)

    # пошли подписи и линия
    draw_text_img = ImageDraw.Draw(text_img)

    # название города, страны, координаты
    city_text = (f"{str(input_list[0][0])}, {str(input_list[0][1])}, "
                 f"{lat_lon_label(input_list[0][2][0], input_list[0][2][1])}")
    draw_text_img.text(
        (5, 5),
        city_text,
        font=fonts[2],
        fill=color
    )

    # температура
    temperature_text = f"{sign_temperature(input_list[1][0])}"
    draw_text_img.text(
        (60, 15),
        temperature_text,
        font=fonts[3],
        fill=color
    )

    temperature_text = (f"Ощущается {sign_temperature(input_list[1][1])}\n"
                        f"{sign_temperature(input_list[1][2])}..{sign_temperature(input_list[1][3])}")
    draw_text_img.text(
        (5, 85),
        temperature_text,
        font=fonts[1],
        fill=color
    )

    # подпись про погоду
    wdt = weather_descriprions_text(str(input_list[4][0].capitalize()))
    # weather_descriptions_text = f"{str(input_list[4][0].capitalize())}"
    # wdt = weather_descriptions_text.split(" ")
    # if len(wdt) > 1:
    #     weather_descriptions_text = f"{wdt[0]}\n"
    #     for i in range(1, len(wdt)):
    #         if i == len(wdt) - 1:
    #             weather_descriptions_text += f"{wdt[i]}"
    #         else:
    #             weather_descriptions_text += f"{wdt[i]} "
    draw_text_img.line((145, 80, 145, 145), fill=color, width=2)
    draw_text_img.text(
        (155, 80),
        wdt,
        font=fonts[0],
        fill=color
    )

    list_text_label = list_2_text_in_draw(input_list)
    for i in range(len(list_text_label)):
        draw_text_img.text(
            (list_text_label[i][0][0], list_text_label[i][0][1]),
            list_text_label[i][1],
            font=fonts[1],
            fill=color
        )

    data_time_now = datetime.datetime.now()
    filename_to_save_png = f"images/output/pic{data_time_now.strftime('%m%d%y_%H_%M_%S_%f')}.png"
    text_img.save(filename_to_save_png, format="png")
    text_img.close()
    return filename_to_save_png

# img_wind = Image.open(do_image(input_list), MODE_FOR_OPEN_PICTURES)
# img_wind.show()
