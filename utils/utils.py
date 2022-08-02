import string

from datetime import date
from random import randint, choice


def get_random_id():
    random_int = randint(20, 100)
    characters = string.digits + string.ascii_letters
    return ''.join(choice(characters) for _ in range(random_int))


def convert_date(str_date):
    day, month, year = str_date.split('/')
    return f'{year}-{month}-{day}'


def format_water(water):
    water = int(water)
    formatted_water = ''
    if water >= 1000:
        formatted_water += f'{str(water)[0]}L '
    hundred = water % 1000
    if hundred > 0:
        formatted_water += f'{hundred}ml'

    if formatted_water == '':
        return '0'

    return formatted_water


def get_date(str_date):
    year, month, day = str_date.split('-')
    return date(year=int(year), month=int(month), day=int(day))
