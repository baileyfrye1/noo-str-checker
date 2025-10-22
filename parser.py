from playwright.async_api import async_playwright
import re

from sheet_client import sheet
from utils import Sheet, str_to_price


async def fetch_and_parse(urls: list[str]):
    bad_keywords = ["Expired", "Cancelled", "Sold"]
    format_requests = []
    pattern = r"\$?\d{1,3}(?:,\d{3})*"
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        for url in urls:
            await page.goto(url, wait_until="networkidle")
            title = await page.title()

            if "Airbnb" in title:
                print(f"Airbnb {title} is available")
                continue

            price_element = await page.query_selector(".price")
            if price_element:
                price_text = await price_element.inner_text()
                match = re.search(pattern, price_text)

                if match:
                    price = str_to_price(match.group())
                    sheet_prices = [
                        str_to_price(str(x))
                        for x in sheet.col_values(Sheet.PRICE.value)
                        if x and x != "Price Each"
                    ]

                if any(keyword for keyword in bad_keywords if keyword in price_text):
                    cell = sheet.find(url)
                    if cell:
                        fmt = {"backgroundColor": {"red": 1, "blue": 0.8, "green": 0.8}}

                        format_requests.append(
                            {"range": f"A{cell.row}:Z{cell.row}", "format": fmt}
                        )

                        # sheet.update_acell(f"J{cell.row}", "Unavailable")
                        print(cell.row)
                    else:
                        print("Could not find url in sheet")
                    continue

                print(f"Price for {title}: {price_text}. URL: {url}")
            else:
                print(f"Price for {title} not found. URL: {url}")

        sheet.batch_format(format_requests)
        await browser.close()
