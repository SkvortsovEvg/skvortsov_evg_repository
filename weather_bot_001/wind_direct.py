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
    if deg == 0 or deg == 360:
        return "В"
    return -1