import string
from enum import Enum
from typing import Any, List, Optional, Tuple

from gspread import ValueRange


def convert_cell_format(col: int, row: int):
    alphabet = list(string.ascii_uppercase)
    return f"{alphabet[col - 1]}{row}"


def str_to_int(raw_price: str) -> int:
    return int(raw_price.replace("$", "").replace(",", ""))


def int_to_price(raw_int: int) -> str:
    return f"${raw_int:,}"


def find_cell_in_values(
    values: ValueRange | List[List[Any]], target: Any
) -> Optional[Tuple[int, int]]:
    for i, v in enumerate(values):
        try:
            if target in v:
                return (i, v.index(target))
        except ValueError:
            continue
    return None


class Sheet(Enum):
    ADDRESS = 1
    PRICE = 5
    LINKS = 8
