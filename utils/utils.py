import string

from datetime import date
from random import randint, choice


def get_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


def get_random_id():
    random_int = randint(20, 100)
    characters = string.digits + string.ascii_letters
    return ''.join(choice(characters) for _ in range(random_int))
