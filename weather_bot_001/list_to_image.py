import datetime
from wind_direct import wind_direction
from dictionaries import open_file_dict, domain_country_dict
from math import *
from config import FILENAME_DOMAIN_COUNTRY_DICT


def output_list_to_image(input_weather_json, input_moon_json):
    output_file_dict = open_file_dict(FILENAME_DOMAIN_COUNTRY_DICT)
    dict_domain_country = domain_country_dict(output_file_dict)
    output_list = []
    # название города, страны, координаты
    tmp_list = [input_weather_json['name']]
    tmp_var = input_weather_json['sys']['country']

    if tmp_var in dict_domain_country:
        tmp_list.append(dict_domain_country[tmp_var])
    else:
        tmp_list.append("-1")
    coords_list = [input_weather_json['coord']['lat'], input_weather_json['coord']['lon']]
    tmp_list.append(coords_list.copy())
    output_list.append(tmp_list.copy())
    tmp_list.clear()

    # температура
    tmp_list = [round(input_weather_json["main"]["temp"]), round(input_weather_json["main"]["feels_like"]),
                ceil(input_weather_json["main"]["temp_max"]), floor(input_weather_json["main"]["temp_min"])]
    output_list.append(tmp_list.copy())
    tmp_list.clear()

    # ветер
    tmp_list = [round(input_weather_json["wind"]["speed"]),
                wind_direction(input_weather_json["wind"]["deg"])]
    output_list.append(tmp_list.copy())
    tmp_list.clear()

    # давление и влажность
    tmp_list = [round(0.75 * input_weather_json["main"]["pressure"]), input_weather_json["main"]["humidity"]]
    output_list.append(tmp_list.copy())
    tmp_list.clear()

    # weather description (про погоду)
    tmp_list = [input_weather_json['weather'][0]['description'], input_weather_json['weather'][0]['icon'],
                input_weather_json['weather'][0]['id'], input_weather_json['weather'][0]['main']]
    output_list.append(tmp_list.copy())
    tmp_list.clear()

    # про Солнце
    tmp_var_sunrise = datetime.datetime.fromtimestamp(input_weather_json["sys"]["sunrise"])
    tmp_list.append(tmp_var_sunrise.time())
    tmp_var_sunset = datetime.datetime.fromtimestamp(input_weather_json["sys"]["sunset"])
    tmp_list.append(tmp_var_sunset.time())
    tmp_var = (datetime.datetime.fromtimestamp(input_weather_json["sys"]["sunset"]) -
               datetime.datetime.fromtimestamp(input_weather_json["sys"]["sunrise"]))
    tmp_list.append(tmp_var)
    tmp_list.append(tmp_var_sunrise)
    tmp_list.append(tmp_var_sunset)
    output_list.append(tmp_list.copy())
    tmp_list.clear()

    # про Луну
    tmp_list = [input_moon_json["moonrise"], input_moon_json["moonset"]]
    output_list.append(tmp_list.copy())
    tmp_list.clear()
    return output_list
