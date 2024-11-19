import datetime
from PIL import Image, ImageDraw, ImageFont
from pictures import (filename_time_of_day, filename_moon_phase, color_label, color_days,
                      weather_conditions, filename_interface_big_dict)
from sign_temp import sign_temperature
from weather_descriptions import weather_descriprions_text
from wind_direct import wind_direction
from pprint import pprint
from moon_phase import moon_phase
from time_of_day import time_of_day_big
from lat_lon import lat_lon_label

MODE_FOR_OPEN_PICTURES = 'r'
DIVIDER_SIZE = 3
DIVIDER_SIZE_MOON = 15
DIVIDER_SIZE_INTERFACE = 9

fonts = (
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=24),
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=16),
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=12),
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=55),
    ImageFont.truetype("fonts/PT_Serif/PTSerif-Bold.ttf", size=14),
)

input_list_big = [[[datetime.datetime(2024, 1, 13, 12, 0)],
                   [-17, -13, -17],
                   [763, 89],
                   ['переменная облачность', '03d', 802, 'Clouds'],
                   [303, 12, 6]],
                  [[datetime.datetime(2024, 1, 13, 15, 0)],
                   [-15, -13, -16],
                   [764, 86],
                   ['небольшая облачность', '02d', 801, 'Clouds'],
                   [305, 10, 5]],
                  [[datetime.datetime(2024, 1, 13, 18, 0)],
                   [-19, -18, -19],
                   [766, 95],
                   ['ясно', '01n', 800, 'Clear'],
                   [276, 4, 3]],
                  [[datetime.datetime(2024, 1, 13, 21, 0)],
                   [-20, -20, -21],
                   [766, 97],
                   ['ясно', '01n', 800, 'Clear'],
                   [266, 3, 2]],
                  [[datetime.datetime(2024, 1, 14, 0, 0)],
                   [-21, -21, -22],
                   [768, 97],
                   ['ясно', '01n', 800, 'Clear'],
                   [249, 2, 1]],
                  [[datetime.datetime(2024, 1, 14, 3, 0)],
                   [-21, -20, -21],
                   [768, 99],
                   ['ясно', '01n', 800, 'Clear'],
                   [226, 2, 2]],
                  [[datetime.datetime(2024, 1, 14, 6, 0)],
                   [-21, -20, -21],
                   [768, 100],
                   ['переменная облачность', '03n', 802, 'Clouds'],
                   [207, 3, 2]],
                  [[datetime.datetime(2024, 1, 14, 9, 0)],
                   [-18, -18, -19],
                   [769, 98],
                   ['переменная облачность', '03d', 802, 'Clouds'],
                   [188, 6, 3]],
                  [datetime.datetime(2024, 1, 13, 7, 54, 30),
                   datetime.datetime(2024, 1, 13, 16, 29, 33)],
                  ['Сады Придонья', 'РФ', [49.0562, 44.0345]]]


def do_big_picture(input_list_big):
    time_of_day_now = time_of_day_big(input_list_big)
    # time_of_day_now = 3
    # фон
    # img_time_of_day = Image.open(filename_time_of_day[3], MODE_FOR_OPEN_PICTURES)
    img_time_of_day = Image.open(filename_time_of_day[time_of_day_now], MODE_FOR_OPEN_PICTURES)
    # цвет
    color = color_label[time_of_day_now % 2]
    # color = color_label[1]

    filename_interface_big = filename_interface_big_dict[time_of_day_now % 2]

    text_img = Image.new('RGBA', (img_time_of_day.width, img_time_of_day.height), (0, 0, 0, 0))
    text_img.paste(img_time_of_day, (0, 0))

    draw_text_img = ImageDraw.Draw(text_img)
    # строки
    for item in range(1, len(input_list_big)):
        if item != 1:
            draw_text_img.line((10, 35 + 40 * item, 780, 35 + 40 * item), fill=color, width=2)
    # столбцы
    for item in range(1, 11):
        if item != 0 and item != 1 and item != 3 and item != 8 and item != 7 and item != 9:
            draw_text_img.line((10 + 70 * item, 35, 10 + 70 * item, 436), fill=color, width=2)
        elif item == 7:
            draw_text_img.line((10 + 71 * item, 35, 10 + 71 * item, 436), fill=color, width=2)
        elif item == 9:
            draw_text_img.line((10 + 71 * item, 115, 10 + 71 * item, 436), fill=color, width=2)

    all_images = []
    for item in range(len(filename_interface_big)):
        all_images.append(Image.open(filename_interface_big[item], MODE_FOR_OPEN_PICTURES))
        all_images[item] = all_images[item].resize(
            (all_images[item].width // DIVIDER_SIZE_INTERFACE,
             all_images[item].height // DIVIDER_SIZE_INTERFACE))

    for item in range(len(all_images)):
        if item != 1 and item != 3 and item != (len(all_images) - 2) and item != (len(all_images) - 1):
            text_img.paste(all_images[item], (200 + item * 84, 50), all_images[item])
        elif item == 1:
            text_img.paste(all_images[item], (200 + item * 98, 50), all_images[item])
        elif item == 3:
            text_img.paste(all_images[item], (200 + item * 80, 50), all_images[item])
        elif item == (len(all_images) - 2):
            text_img.paste(all_images[item], (200 + item * 95, 50), all_images[item])
        elif item == (len(all_images) - 1):
            text_img.paste(all_images[item], (200 + item * 104, 50), all_images[item])

    # город, координаты
    draw_text_img.text(
        (10, 10),
        f"{input_list_big[9][0]}, {input_list_big[9][1]}, "
        f"{lat_lon_label(input_list_big[9][2][0], input_list_big[9][2][1])}",
        font=fonts[4],
        fill=color
    )

    for item in range(len(input_list_big) - 2):
        this_date_in_list = input_list_big[item][0][0]
        # last_year_in_list = datetime.datetime(2024, 1, 31)
        last_year_in_list = input_list_big[item][0][0].year if item == 0 else input_list_big[item - 1][0][0].year
        color = color_days[time_of_day_now % 2][((int(this_date_in_list.strftime("%j")) + 1) % 2 and
                                                 last_year_in_list == this_date_in_list.year) * 1]

        draw_text_img.text(
            (15, 125 + item * 40),
            input_list_big[item][0][0].strftime('%d.%m.%y %H:%M'),
            font=fonts[1],
            fill=color
        )
        # вывод: температура
        draw_text_img.text(
            (155, 125 + item * 40),
            sign_temperature(input_list_big[item][1][0]),
            font=fonts[1],
            fill=color
        )
        # вывод: температура мах, температура мин
        draw_text_img.text(
            (200, 125 + item * 40),
            f"{sign_temperature(input_list_big[item][1][1])}..{sign_temperature(input_list_big[item][1][2])}",
            font=fonts[1],
            fill=color
        )
        # вывод: давление
        draw_text_img.text(
            (309, 125 + item * 40),
            str(input_list_big[item][2][0]),
            font=fonts[1],
            fill=color
        )
        # вывод: влажность
        draw_text_img.text(
            (387, 125 + item * 40),
            str(input_list_big[item][2][1]),
            font=fonts[1],
            fill=color
        )
        # вывод: ветер скорость, порывы, направление
        draw_text_img.text(
            (435, 125 + item * 40),
            f"{input_list_big[item][4][2]} {input_list_big[item][4][1]} {wind_direction(input_list_big[item][4][0])}",
            font=fonts[1],
            fill=color
        )
        # вывод: погода
        draw_text_img.text(
            (512, 117 + item * 40),
            weather_descriprions_text(str(input_list_big[item][3][0]).capitalize()),
            font=fonts[4],
            fill=color
        )
        # вывод: картинки погоды
        weather_icon = input_list_big[item][3][1]
        if weather_icon in weather_conditions:
            filename_weather_condition_icon = weather_conditions[weather_icon]
            img_weather_conditions = Image.open(filename_weather_condition_icon, MODE_FOR_OPEN_PICTURES)
            img_weather_conditions = img_weather_conditions.resize(
                (img_weather_conditions.width // DIVIDER_SIZE,
                 img_weather_conditions.height // DIVIDER_SIZE))
            text_img.paste(img_weather_conditions, (665, 120 + item * 40), img_weather_conditions)

        # вывод: Луна
        if item == 0 or yesterday_moon != this_date_in_list.day:
            open_moon_picture = moon_phase(this_date_in_list.year, this_date_in_list.month, this_date_in_list.day)
            yesterday_moon = this_date_in_list.day
            if open_moon_picture != -1:
                moon_img = Image.open(filename_moon_phase[open_moon_picture], MODE_FOR_OPEN_PICTURES)
                moon_img = moon_img.resize(
                    (moon_img.width // DIVIDER_SIZE_MOON, moon_img.height // DIVIDER_SIZE_MOON))
                text_img.paste(moon_img, (730, 120 + item * 40), moon_img)
    data_time_now = datetime.datetime.now()
    filename_to_save_png = f"images/output/pic{data_time_now.strftime('%d%m%y_%H_%M_%S_%f')}.png"
    text_img.save(filename_to_save_png, format="png")
    # text_img.show()
    text_img.close()

    return filename_to_save_png


# img = Image.open(do_big_picture(input_list_big), MODE_FOR_OPEN_PICTURES)
# img.show()
# img.close()
