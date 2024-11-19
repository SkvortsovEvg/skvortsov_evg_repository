def weather_descriprions_text(weather_description):
    wdt = weather_description.split(" ")
    if len(wdt) > 1:
        weather_description = f"{wdt[0]}\n"
        for i in range(1, len(wdt)):
            if i == len(wdt) - 1:
                weather_description += f"{wdt[i]}"
            else:
                weather_description += f"{wdt[i]} "
    return weather_description