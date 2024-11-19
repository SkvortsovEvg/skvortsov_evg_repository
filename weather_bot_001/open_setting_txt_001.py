import os
from pprint import pprint

file_name = f"{os.getcwd()}\\txt\\domen_output.txt"
with open(file_name, encoding='', mode='r') as f:
    data = f.read()
    output = data.split('\n')

city_in_country = dict()
for item in output:
    key = item.split(' ')[0]
    value = item[3:]
    city_in_country[key] = value
print(city_in_country)
