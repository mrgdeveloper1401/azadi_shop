from random import choices
from string import digits


def generate_random_code():
    return int(''.join(choices(digits, k=9)))
