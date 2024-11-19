import os
from dictionaries import open_file_dict, country_domain_dict
from config import FILENAME_COUNTRY_DOMAIN_DICT

def letters(input):
    valids = []
    for character in input:
        if character.isalpha():
            valids.append(character)
    return ''.join(valids)

def convert_string2weather(string):
    output = open_file_dict(FILENAME_COUNTRY_DOMAIN_DICT)
    dict_country_domain = country_domain_dict(output)

    if string.count(",") != 0:
        string_list = string.split(", ")
        key = letters(string_list[1]).lower()
        if dict_country_domain.get(key) is not None:
            return f"{string_list[0]},{dict_country_domain[key]}"
        else:
            return -1
    return string
