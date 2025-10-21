import asyncio
from parser import fetch_and_parse

from sheet_client import sheet


async def main():
    urls = [str(x) for x in sheet.col_values(9) if x and x != "Link"]
    await fetch_and_parse(urls)


if __name__ == "__main__":
    asyncio.run(main())
