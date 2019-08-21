import time

def convert_the_date(year: int, month: int, day: int):
    if year < 10:
        year = "200" + str(year)
    elif year<100:
        year = '20' + str(year)
    else:
        year = str(year)
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)
    return year + month + day


def get_the_calendar(start, end):
    month_day = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31,
                 9: 30, 10: 31, 11: 30, 12: 31}
    month_day_leap = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31,
                      9: 30, 10: 31, 11: 30, 12: 31}
    key_list = []
    for year in range(start, end):
        if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
            tmp_month_day = month_day_leap
        else:
            tmp_month_day = month_day
        for month in range(1, 13):
            for day in range(1, tmp_month_day[month] + 1):
                key_list.append(convert_the_date(year % 1000, month, day))
    return key_list

def get_today_date():
    localtime = time.localtime(time.time())
    # # 拼接年月日
    return convert_the_date(localtime.tm_year, localtime.tm_mon, localtime.tm_mday)

def get_n_date(offset):
    calendar = get_the_calendar(2019,2020)
    now_date = get_today_date()
    return calendar[calendar.index(now_date) + offset]
