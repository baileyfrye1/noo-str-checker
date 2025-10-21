import string


def convert_cell_format(col: int, row: int):
    alphabet = list(string.ascii_uppercase)
    return f"{alphabet[col - 1]}{row}"
