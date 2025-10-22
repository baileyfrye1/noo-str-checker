import asyncio
from parser import fetch_and_parse

from playwright.async_api import async_playwright

from sheet_client import sheet
from utils import Sheet


async def main():
    values = sheet.get_all_values()
    is_modified = {"changed": False}
    all_formats = []

    semaphore = asyncio.Semaphore(5)

    urls = [str(row[Sheet.LINKS.value]) for row in values[1:] if row[Sheet.LINKS.value]]
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        tasks = [
            fetch_and_parse(semaphore, url, browser, all_formats, is_modified, values)
            for url in urls
        ]
        await asyncio.gather(*tasks, return_exceptions=True)
        await browser.close()

    if is_modified["changed"]:
        sheet.batch_update([{"range": f"A1:K{len(values)}", "values": values}])
    if all_formats:
        sheet.batch_format(all_formats)


if __name__ == "__main__":
    asyncio.run(main())
