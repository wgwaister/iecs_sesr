from django import template
import datetime
import pytz

register = template.Library()


@register.filter()
def replace_str(value):
    return value.replace('Mail', '信件')


@register.filter()
def date_time(input_date_time):
    taipei_time_zone = pytz.timezone('Asia/Taipei')
    input_taipei_time_zone = input_date_time.astimezone(taipei_time_zone)
    input_time = input_taipei_time_zone.strftime('%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    now_time = now.astimezone(taipei_time_zone)
    now_time_str = now_time.strftime('%Y-%m-%d %H:%M:%S')
    return input_taipei_time_zone < now_time


@register.filter()
def boolean_trans(boolean_value):
    if boolean_value:
        return '有'
    else:
        return '無'
