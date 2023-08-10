#!/usr/bin/python3
import datetime


def get_date(json_data):
    return format_date(json_data["informacion"]["fecha"])


def format_date(date):
    return datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%d-%m-%Y')


def is_final_date(d, first_day):
    if d.day == first_day.day and d.month == first_day.month and d.year == first_day.year:
        return True
    return False


def update_dates(day, first_day):
    day = day - datetime.timedelta(days=1)
    final_date = is_final_date(day, first_day)
    return day, final_date
