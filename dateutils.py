#!/usr/bin/python3
import datetime


def get_date(json_data):
    return format_date(json_data["informacion"]["fecha"])


def format_date(date):
    return datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%d-%m-%Y')


def is_final_date(d):
    if d.day == 1 and d.month == 1 and d.year == 2019:
        return True
    return False


def update_dates(day):
    day = day - datetime.timedelta(days=1)
    final_date = is_final_date(day)
    return day, final_date
