import requests
import datetime
from pprint import pprint
from config import OPEN_WEATHER_TOKEN
from config import MOON_API


def get_weather(city, open_weather_token, moon_api):
    def wind_direction(deg):
        if 0 < deg < 90:
            return "СВ"
        if deg == 90:
            return "С"
        if 90 < deg < 180:
            return "СЗ"
        if deg == 180:
            return "З"
        if 180 < deg < 270:
            return "ЮЗ"
        if deg == 270:
            return "Ю"
        if 270 < deg < 360:
            return "ЮВ"
        if deg == 0:
            return "В"
        return "Не могу определить направление ветра!"


    countryCity = {
        "RU": "Россия",
        "MX": "Мексика",
        "US": "США",
        "KZ": "Казахстан",
        "FR": "Франция",
        "DE": "Германия",
        "BR": "Бразилия",
        "ES": "Испания",
        "GB": "Великобритания",
        "AU": "Австралия",
        "GR": "Греция",
        "TR": "Турция",
        "EG": "Египет",
        "AR": "Аргентина"
    }
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    try:
        weather_request = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric&lang=ru"
        )
        # r = requests.get(
        #     f"https://api.openweathermap.org/data/2.5/weather?lat=49.644646&lon=44.289797&appid={open_weathen_token}&units=metric&lang=ru"
        # )
        data = weather_request.json()
        pprint(data)

        our_weather = []
        city_list = []
        weather_list = []
        city = data["name"]
        city_list.append(city)

        city_coords = []
        city_lat = data["coord"]["lat"]
        city_lon = data["coord"]["lon"]
        country = data["sys"]["country"]

        if country in countryCity:
            city += ', ' + countryCity[country]
            city_list.append(countryCity[country])
        else:
            city_list.append("Error")
        city_coords.append(city_lat)
        city_coords.append(city_lon)
        city_list.append(city_coords)

        our_weather.append(city_list)

        temp = round(data["main"]["temp"])
        weather_description = data["weather"][0]["main"]
        weather_description_list = []

        weather_description_list.append(data["weather"][0]["description"])
        weather_description_list.append(data["weather"][0]["icon"])
        weather_description_list.append(data["weather"][0]["id"])
        weather_description_list.append(data["weather"][0]["main"])

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Лучше посмотри в окно"

        humidity = data["main"]["humidity"]
        pressure = round(data["main"]["pressure"] * 0.75)
        wind = round(data["wind"]["speed"])
        wind_direct = wind_direction(data["wind"]["deg"])
        weather_list.append(temp)
        weather_list.append(wind)
        weather_list.append(pressure)
        weather_list.append(humidity)
        weather_list.append(wind_direct)

        our_weather.append(weather_list)
        our_weather.append(weather_description_list)
        sun_list = []
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        sun_list.append(sunrise_timestamp.time())
        sun_list.append(sunset_timestamp.time())
        sun_list.append(length_of_the_day)
        sun_list.append(sunrise_timestamp)
        sun_list.append(sunset_timestamp)
        our_weather.append(sun_list)


        moon_request = requests.get(
            f"https://api.ipgeolocation.io/astronomy?apiKey={moon_api}&lat={our_weather[0][2][0]}&long={our_weather[0][2][1]}"
        )
        data_moon = moon_request.json()

        pprint(data_moon)
        about_moon = []
        about_moon.append(data_moon['moonrise'])
        about_moon.append(data_moon['moonset'])
        about_moon.append(data_moon['moon_distance'])
        our_weather.append(about_moon)

        print(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}\n"
              f"Погода в городе: {city}\nТемпература: {temp}°С {wd}\nВлажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n"
              f"Ветер: {wind} м/с\nВремя восхода: {sunrise_timestamp}\nВремя заката: {sunset_timestamp}\n"
              f"Продолжительность дня: {length_of_the_day}\n"
              f"Луна поднимается в {about_moon[0]}\n"
              f"Луна садится в {about_moon[1]}"
              )
        pprint(weather_list)
        pprint(our_weather)
    except Exception as ex:
        print(ex)
        print('Проверьте название города')


def main():
    city = input("Введите город: ")
    get_weather(city, OPEN_WEATHER_TOKEN, MOON_API)


if __name__ == '__main__':
    main()
