import requests
import os

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set.")


def get_price(symbol):
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        return data['c']
    except Exception as e:
        print(f"Error fetching price for {symbol}")
        return None

def is_valid_ticker(symbol):
    price = get_price(symbol)
    if price is None or price == 0:
        return False
    else:
        return True

