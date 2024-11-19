def sign_temperature(temperature):
    if temperature > 0:
        return f"+{temperature}°"
    else:
        return f"{temperature}°"