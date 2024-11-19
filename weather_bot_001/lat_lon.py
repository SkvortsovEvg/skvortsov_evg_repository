def lat_lon_label(lat, lon):
    answer = ""
    if lat > 0:
        answer = f"{str(lat)}°с.ш, "
    else:
        answer = f"{str(abs(lat))}°ю.ш., "
    if lon > 0:
        answer += f"{str(lon)}°в.д."
    else:
        answer += f"{str(abs(lon))}°з.д."
    return answer