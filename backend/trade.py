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
        return -1 # Return -1 for invalid ticker symbols

