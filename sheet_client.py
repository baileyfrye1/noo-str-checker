import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_file("creds.json", scopes=scopes)

client = gspread.authorize(creds)

wb_id = "1w5r33ciXqFddzX8HFMjaVui4X2ydN1QPYh0OAoxKScg"

wb = client.open_by_key(wb_id)

sheet = wb.sheet1
