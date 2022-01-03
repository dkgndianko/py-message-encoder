from itertools import cycle


ZERO = ord("0")


def multiply(base: int, multiplier: int) -> int:
    result = (base * multiplier)
    if result > 10:
        result %= 9
    return result


def calculate_luhn(_input: str) -> int:
    _sum = sum(map(lambda zipped: multiply(ord(zipped[0]) - ZERO, zipped[1]), zip(_input, cycle([2, 1]))))
    return -_sum % 100
