import os


def open_file_dict(filename):
    with open(filename, encoding='utf-8', mode='r') as f:
        data = f.read()
        output = data.split('\n')
    return output


def domain_country_dict(output):
    temp_dict = dict()
    for item in output:
        key = item.split(' ')[0]
        value = item[3:]
        if temp_dict.get(key) is None:
            temp_dict[key] = value
    return temp_dict


def country_domain_dict(output):
    temp_dict = dict()
    for item in output:
        value = item.split(' ')[0].lower()
        key = item[3:].lower()
        if temp_dict.get(key) is None:
            temp_dict[key] = value
    return temp_dict
