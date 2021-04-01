from enum import Enum


class Status(Enum):
    NO_SONG = -1
    ERROR = 0
    SUCCESS = 1


def digit_as_emoji(digit: int):
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


def number_to_digit_list(number: int):
    digits = []
    number = round(int(number))
    if number < 0:
        return []

    while number != 0:
        digits.append(number % 10)
        number //= 10

    digits.reverse()
    return digits


def number_as_emojis(number: int):
    digits = number_to_digit_list(number)
    result = []
    for d in digits:
        result.append(digit_as_emoji(d))

    return result


def number_to_emojis(number: int) -> str:
    digits = number_to_digit_list(number)
    result = ""
    for d in digits:
        result += digit_as_emoji(d)

    return result
