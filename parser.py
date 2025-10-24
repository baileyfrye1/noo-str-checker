import asyncio
import re
from typing import Any, Dict, List

from gspread.worksheet import ValueRange
from playwright.async_api import Browser

from utils import Sheet, find_cell_in_values, int_to_price, str_to_int

bad_keywords = ["Expired", "Cancelled", "Sold"]
pattern = r"\$?\d{1,3}(?:,\d{3})*"
fmt = {"backgroundColor": {"red": 1, "blue": 0.8, "green": 0.8}}


async def fetch_and_parse(
    semaphore: asyncio.Semaphore,
    url: str,
    browser: Browser,
    all_formats: List,
    is_modified: Dict[str, bool],
    values: ValueRange | List[List[Any]],
):
    async with semaphore:
        try:
            page = await browser.new_page()
            await asyncio.sleep(0.5)

            current_cell = find_cell_in_values(values, url)
            if not current_cell:
                print("Could not find url in worksheet")
                return

            row, _ = current_cell

            await page.goto(url, wait_until="networkidle")
            title = await page.title()

            if "404" in title or "Realtracs" in title:
                all_formats.append(
                    {
                        "range": f"A{row + 1}:K{row + 1}",
                        "format": fmt,
                    }
                )

                print(f"UNAVAILABLE - {values[row][Sheet.ADDRESS.value]}")
                return

            if "Airbnb" in title:
                print(f"Airbnb {title} is available")
                return

            price_element = await page.query_selector(".price")
            if not price_element:
                print(f"Price for {title} not found. URL: {url}")
                return

            price_text = await price_element.inner_text()
            if any(keyword for keyword in bad_keywords if keyword in price_text):
                all_formats.append(
                    {
                        "range": f"A{row + 1}:K{row + 1}",
                        "format": fmt,
                    }
                )

                print(f"UNAVAILABLE - {values[row][Sheet.ADDRESS.value]}")
                return

            match = re.search(pattern, price_text)
            if match:
                price = str_to_int(match.group())
                property_price = str_to_int(values[row][Sheet.PRICE.value])
                if property_price != price:
                    formatted_price = int_to_price(price)
                    values[row][Sheet.PRICE.value] = formatted_price

                    if not is_modified["changed"]:
                        is_modified["changed"] = True

                    print(
                        f"PRICE UPDATE - {title}\n OLD PRICE: {int_to_price(property_price)} NEW PRICE: {formatted_price}"
                    )
                    return

            print(f"Price for {title}: {property_price}. URL: {url}")
        except TimeoutError:
            print(f"Navigation timed out for {url}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        finally:
            await page.close()
