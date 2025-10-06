from datetime import datetime, timedelta
import re
from django import template

register = template.Library()


@register.simple_tag
def date_format(date):
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+03:00').strftime('%d.%m.%Y')
    else:
        date = date.strftime('%d.%m.%Y')
    return date


@register.simple_tag
def time_format(time):
    if isinstance(time, str):
        time = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S+03:00').strftime('%H:%M')
    else:
        time = time.strftime('%H:%M')
    return time


@register.simple_tag
def get_timezone(date):
    timezone = re.search(r'\+\d{2}:\d{2}', date)
    return timezone.group(0)


@register.simple_tag
def date_diff(date, seconds):
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+03:00')
    return date + timedelta(minutes=seconds)


@register.simple_tag
def minutes_diff(first_value, second_value):
    return first_value - second_value


@register.simple_tag
def minutes_to_hours(minutes):
    return int(minutes / 60)


@register.simple_tag
def split_item(item):
    return item.split('|')


@register.simple_tag
def text_join(lst):
    return ', '.join(lst)


@register.simple_tag
def full_address(country, city, street):
    address = (country, city, street)
    return ', '.join(filter(None, address))


@register.simple_tag
def unit_to_hundred(num):
    return int(num) / 100


@register.simple_tag
def get_employee_status(status):
    return {'ok': 'Лайкнут в ТТ'}


@register.simple_tag
def get_last_item(items):
    return items[-1]
