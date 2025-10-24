# Real Estate Listing Short-Term-Rental Price Updater & Availabilty Checker

This project automates checking and updating property prices and availability from Realtracs and Airbnb links in a Google Sheet. It uses Playwright for web scraping, asyncio for concurrency, and gspread for batch updates — allowing efficient, large-scale price monitoring with minimal API calls.

## Features

• Automated Price Checking — Scrapes live Realtracs and Airbnb listings to verify and update prices and availability.
• Concurrency — Uses async tasks and semaphores to process 5 URLs concurrently.
• In-Memory Updates — Modifies data locally before batch updating to reduce Google Sheets API calls from hundreds to just 3.
• Automatic Formatting — Highlights unavailable listings (e.g., expired, cancelled, sold, expired URL for Realtracs, and 404 error from Airbnb).

## Tech Stack & Tools

• Python
• Playwright
• gspread
• asyncio
• re (regex) for price parsing

### Example Output

```Python
PRICE UPDATE - 293 Plus Park Blvd #113
OLD PRICE: $1,000 NEW PRICE: $260,000
Price for 803 Hillview Hts #106: $314,900. URL: https://go.realtracs.com/1btKRBi
UNAVAILABLE - 707 26th Ave N #204
```
