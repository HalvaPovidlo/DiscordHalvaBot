from enum import Enum


class Status(Enum):
    NO_SONG = -1
    ERROR = 0
    SUCCESS = 1


def digit_as_emoji(digit):
    return {
        1: '1️⃣',
        2: '2️⃣',
        3: '3️⃣',
        4: '4️⃣',
        5: '5️⃣',
        6: '6️⃣',
        7: '7️⃣',
        8: '8️⃣',
        9: '9️⃣',
        0: '0️⃣',
    }[digit]


def number_as_emojis(number):
    digits = []
    number = round(int(number))
    if number < 0:
        return []

    while number != 0:
        digits.append(number % 10)
        number //= 10

    result = []
    digits.reverse()
    for d in digits:
        result.append(digit_as_emoji(d))

    return result
