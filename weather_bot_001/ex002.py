import datetime
import os
from pprint import pprint
from dictionaries import open_file_dict, country_domain_dict


def letters(input):
    valids = []
    for character in input:
        if character.isalpha():
            valids.append(character)
    return ''.join(valids)


# print(int(datetime.date.today().strftime("%j")))


# this_date_in_list = datetime.datetime(2021, 12, 31)
# yesterday = 2021
# print(int(this_date_in_list.strftime("%j")))
# print((bool((int(this_date_in_list.strftime("%j")) + 1) % 2) or bool(yesterday == this_date_in_list.year)) * 1)

# output = open_file_dict(f"{os.getcwd()}\\txt\\country_domain.txt")
# temp_dict = country_domain_dict(output)
#
# string = "Мир, Россия,".strip()
# # print(string)
# coma_in_string = string.count(",")
# str_list = string.split(", ") if coma_in_string != 0 else string.split(" ")
# print(str_list)
# tmp_str = letters(str_list[1])
# key = tmp_str.lower()
# print(key)
#
#
# if temp_dict.get(key) is not None:
#     newstring = f"{str_list[0]},{temp_dict[key]}"
# else:
#     newstring = -1
# print(newstring)

one = '1'.isalpha()
print(one.real)
