from enum import Enum
import string


def convert_cell_format(col: int, row: int):
    alphabet = list(string.ascii_uppercase)
    return f"{alphabet[col - 1]}{row}"


def str_to_price(raw_price: str):
    return int(raw_price.replace("$", "").replace(",", ""))


class Sheet(Enum):
    PRICE = 6
    LINKS = 9
