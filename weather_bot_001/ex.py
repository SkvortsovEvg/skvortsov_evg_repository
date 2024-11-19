from config import YANDEX_API_GEOCODER
import requests
from pprint import pprint

# 49.644657, 44.289940 - Солодча, Россия (lat, lon)
# 41.887064, 12.504809 - Рим, Италия (lat, lon)

# Солодча, Россия
lat = 49.644657
lon = 44.289940

# Рим, Италия
# lat = 41.887064
# lon = 12.504809

# data_request = requests.get(
#     f"https://geocode-maps.yandex.ru/1.x/?apikey={YANDEX_API_GEOCODER}&geocode={lon},{lat}&format=json"
# )
# data = data_request.json()
# city = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['description']
city = "село Солодча, Ольховский район, Волгоградская область, Россия"
city = city.split(', ')
pprint(city[0])
pprint(dir(requests))
