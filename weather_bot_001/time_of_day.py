import datetime


def time_of_day(input_list):
    datetime_now = datetime.datetime.now()
    if input_list[5][3] <= datetime_now < input_list[5][4]:
        return 0
    else:
        return 1


def time_of_day_big(input_list_big):
    datetime_now = datetime.datetime.now()
    if input_list_big[8][0] <= datetime_now < input_list_big[8][1]:
        return 2
    else:
        return 3
