import requests
from config import OPEN_WEATHER_TOKEN
from math import *
from pprint import pprint
import os
import datetime
from dictionaries import open_file_dict, domain_country_dict
from PIL import Image
from do_big_image import do_big_picture
from json_py import data_json
from config import FILENAME_DOMAIN_COUNTRY_DICT

MODE_FOR_OPEN_PICTURES = 'r'


def output_json_big_3h_list(data_json):
    output_file_dict = open_file_dict(FILENAME_DOMAIN_COUNTRY_DICT)
    dict_domain_country = domain_country_dict(output_file_dict)
    tmp_city_list = []
    list_data_json = data_json["list"]
    tmp_city_list = [data_json["city"]["name"]]
    tmp_var = data_json["city"]["country"]
    if tmp_var in dict_domain_country:
        tmp_city_list.append(dict_domain_country[tmp_var])
    else:
        tmp_city_list.append("-1")
    coords_list = [data_json["city"]["coord"]["lat"], data_json["city"]["coord"]["lon"]]
    tmp_city_list.append(coords_list.copy())

    tmp_list = []
    temp_list = []
    for item in range(8):
        temp_list.append(
            [datetime.datetime.fromtimestamp(list_data_json[item]["dt"])])
        temp_list.append([round(list_data_json[item]["main"]["temp"]), ceil(list_data_json[item]["main"]["temp_max"]),
                          floor(list_data_json[item]["main"]["temp_min"])])
        temp_list.append(
            [round(list_data_json[item]["main"]["pressure"] * 0.75), list_data_json[item]["main"]["humidity"]])
        temp_list.append([list_data_json[item]["weather"][0]["description"], list_data_json[item]["weather"][0]["icon"],
                          list_data_json[item]["weather"][0]["id"], list_data_json[item]["weather"][0]["main"]])
        temp_list.append([list_data_json[item]["wind"]["deg"], ceil(list_data_json[item]["wind"]["gust"]),
                          round(list_data_json[item]["wind"]["speed"])])
        tmp_list.append(temp_list.copy())
        temp_list.clear()
    tmp_list.append([datetime.datetime.fromtimestamp(data_json["city"]["sunrise"]),
                     datetime.datetime.fromtimestamp(data_json["city"]["sunset"])])
    tmp_list.append(tmp_city_list.copy())
    return tmp_list

# file_name = do_big_picture(output_json_big_3h_list(data_json))
# img = Image.open(file_name, MODE_FOR_OPEN_PICTURES)
# img.show()
# img.close()
