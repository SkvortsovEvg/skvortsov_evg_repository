import os
from pprint import pprint
import datetime
from datetime import date
from PIL import Image, ImageDraw, ImageFont

DIVIDER_SIZE = 25  # делитель при изменении размера картинок в интерфейсе
DIVIDER_SIZE_TEMPERATURE = 11
DIVIDER_SIZE_MOON = 15
MODE_FOR_OPEN_PICTURES = 'r'

input_list = [['Москва', 'Россия', [55.7522, 37.6156]],
              [3, 2, 751, 98, 'ЮЗ'],
              ['пасмурно', '04n', 804, 'Clouds'],
              [datetime.time(8, 56, 43),
               datetime.time(15, 57, 1),
               datetime.timedelta(seconds=25218),
               datetime.datetime(2023, 12, 20, 8, 56, 43),
               datetime.datetime(2023, 12, 20, 15, 57, 1)],
              ['12:54', '00:23', 372694.6377077178]]

fonts = [
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=24),
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=16),
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=12),
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=55)
]
filename_time_of_day = [
    "images/day.png",
    "images/night.png"
]
filename_temperature = [
    "images/icons/thermometer/very_hot_001.png",
    "images/icons/thermometer/hot_001.png",
    "images/icons/thermometer/cold_001.png",
    "images/icons/thermometer/very_cold_001.png",
]

filename_wind = [
    "images/icons/wind/wind_001.png",
    "images/icons/wind/wind_002.png",
    "images/icons/wind/wind_003.png",
]
weather_conditions = {
    "01d": "images/icons_weather/01d@2x.png",
    "01n": "images/icons_weather/01n@2x.png",
    "02d": "images/icons_weather/02d@2x.png",
    "02n": "images/icons_weather/02n@2x.png",
    "03d": "images/icons_weather/03d@2x.png",
    "03n": "images/icons_weather/03n@2x.png",
    "04d": "images/icons_weather/04d@2x.png",
    "04n": "images/icons_weather/04n@2x.png",
    "09d": "images/icons_weather/09d@2x.png",
    "09n": "images/icons_weather/09n@2x.png",
    "10d": "images/icons_weather/10d@2x.png",
    "10n": "images/icons_weather/10n@2x.png",
    "11d": "images/icons_weather/11d@2x.png",
    "11n": "images/icons_weather/11n@2x.png",
    "13d": "images/icons_weather/13d@2x.png",
    "13n": "images/icons_weather/13n@2x.png",
    "50d": "images/icons_weather/50d@2x.png",
    "50n": "images/icons_weather/50n@2x.png"
}

color_label = {
    0: "black",
    1: "white"
}

filename_interface = [
    "images/icons/barometer/barometer_001.png",  # барометр
    "images/icons/rain/raindrops_001.png",  # капля воды
    "images/icons/sun/sunrise_001.png",  # восход Солнца
    "images/icons/sun/sunset_001.png",  # закат Солнца
    "images/icons/sun/day_and_night_001.png",  # смена дня и ночи (продолжительность дня)
    "images/icons/moon/moonrise_001.png",  # восход Луны
    "images/icons/moon/moonset_002.png"  # закат Луны
]

filename_moon_phase = {
    0: "images/images_moon/moon_001.png",
    1: "images/images_moon/moon_002.png",
    2: "images/images_moon/moon_003.png",
    3: "images/images_moon/moon_004.png",
    4: "images/images_moon/moon_005.png",
    5: "images/images_moon/moon_006.png",
    6: "images/images_moon/moon_007.png",
    7: "images/images_moon/moon_008.png"
}


def do_pic(input_list):
    def time_of_day():
        datetime_now = datetime.datetime.now()
        if input_list[3][3] <= datetime_now < input_list[3][4]:
            return 0
        else:
            return 1

    def lat_lon_label(lat, lon):
        answer = ""
        if lat > 0:
            answer = f"{str(lat)}°с.ш, "
        else:
            answer = f"{str(abs(lat))}°ю.ш., "
        if lon > 0:
            answer += f"{str(lon)}°в.д."
        else:
            answer += f"{str(abs(lon))}°з.д."
        return answer

    def input_list_2_list_text_label(input_list, i, j_start, j_end, x_pos, y_pos, diff=25):
        i_1 = {
            1: " м/с",
            2: " мм.рт.ст",
            3: "%"
        }
        tmp_list = []
        output_list = []

        for j in range(j_start, j_end + 1):
            tmp_list.append([x_pos, y_pos])
            y_pos += diff
            tmp_string = f"{str(input_list[i][j])}"
            if i == 1:
                tmp_string += i_1[j]
            if i == 1 and j == 1:
                tmp_string += f" {str(input_list[i][4])}"
            tmp_list.append(tmp_string)
            output_list.append(tmp_list.copy())
            tmp_list.clear()
        return output_list

    def moon_phase(year, month, day):
        if month < 3:
            year -= 1
            month += 12
        month += 1
        c = 365.25 * year
        e = 30.6 * month
        jd = c + e + day - 694039.09
        jd /= 29.5305882
        b = int(jd)
        jd -= b
        b = round(jd * 8)
        if b > 8:
            b = 0
        if 0 <= b <= 7:
            return b
        return -1

    def icon_wind(input_list):
        if 0 <= input_list[1][1] < 5:
            return filename_wind[0]
        elif 5 <= input_list[1][1] < 15:
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

    wc_temp = input_list[2][1]
    if wc_temp in weather_conditions:
        filename_weather_conditions = weather_conditions[wc_temp]

    time_of_day_now = time_of_day()
    color = color_label[time_of_day_now]
    img_time_of_day = Image.open(filename_time_of_day[time_of_day_now], MODE_FOR_OPEN_PICTURES)
    img_weather_conditions = Image.open(filename_weather_conditions, MODE_FOR_OPEN_PICTURES)

    all_images = []
    length_filename_interface = len(filename_interface)
    # открытие изображений filename_interface
    for i in range(length_filename_interface):
        all_images.append(Image.open(filename_interface[i], MODE_FOR_OPEN_PICTURES))
        all_images[i] = all_images[i].resize(
            (all_images[i].height // DIVIDER_SIZE, all_images[i].width // DIVIDER_SIZE))

    # создание нового изображения
    text_img = Image.new('RGBA', (340, 240), (0, 0, 0, 0))
    # обои
    text_img.paste(img_time_of_day, (0, 0))
    # сверху
    text_img.paste(img_weather_conditions, (240, 25), mask=img_weather_conditions)

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

    date_now = date.today()
    open_moon_picture = moon_phase(date_now.year, date_now.month, date_now.year)
    if open_moon_picture != -1:
        moon_img = Image.open(filename_moon_phase[open_moon_picture], MODE_FOR_OPEN_PICTURES)
        moon_img = moon_img.resize((moon_img.height // DIVIDER_SIZE_MOON, moon_img.width // DIVIDER_SIZE_MOON))
        text_img.paste(moon_img, (285, 200), moon_img)

    draw_text_img = ImageDraw.Draw(text_img)

    city_text = (f"{str(input_list[0][0])}, {str(input_list[0][1])}, "
                 f"{lat_lon_label(input_list[0][2][0], input_list[0][2][1])}")

    draw_text_img.text(
        (5, 5),
        city_text,
        font=fonts[2],
        fill=color
    )

    temperature_text = f"{input_list[1][0]}°"
    draw_text_img.text(
        (60, 15),
        temperature_text,
        font=fonts[3],
        fill=color
    )

    weather_descriptions_text = f"{str(input_list[2][0].capitalize())}"
    wdt = weather_descriptions_text.split(" ")
    if len(wdt) > 1:
        weather_descriptions_text = f"{wdt[0]}\n"
        for i in range(1, len(wdt)):
            if i == len(wdt) - 1:
                weather_descriptions_text += wdt[i]
            else:
                weather_descriptions_text += f"{wdt[i]} "

    draw_text_img.text(
        (5, 80),
        weather_descriptions_text,
        font=fonts[0],
        fill=color
    )

    list_text_label = input_list_2_list_text_label(input_list, 1, 1, 3, 40, 150)
    my_tmp_list = input_list_2_list_text_label(input_list, 3, 0, 2, 180, 150)
    list_text_label += my_tmp_list
    moon_list = input_list_2_list_text_label(input_list, 4, 0, 1, 290, 150)
    list_text_label += moon_list

    pprint(list_text_label)

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
    return filename_to_save_png


new_img = Image.open(do_pic(input_list))
new_img.show()
