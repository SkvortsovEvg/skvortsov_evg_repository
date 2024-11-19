def moon_phase(year, month, day):
    if month < 3:
        year -= 1
        month += 12
    month += 1
    c = 365.25 * year
    e = 30.6 * month
    jd = c + e + day - 694039.09
    jd /= 29.5305882
    b = int(jd)
    jd -= b
    b = round(jd * 8)
    if b >= 8:
        b = 0
    if 0 <= b <= 7:
        return b
    return -1
