import os
import finnhub

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set.")
finnhub_client = finnhub.Client(api_key=API_KEY)

def get_price(symbol):
    try:
        data = finnhub_client.quote(symbol)
        if data['d'] is None:
            return -1
        return data['c']
    except Exception as e:
        print(f"Error fetching price for {symbol} {e}")
        return -1 # Return -1 for invalid ticker symbols

def get_market_status():
    return finnhub_client.market_status(exchange='US')['isOpen']

def get_open_price(symbol):
    try:
        data = finnhub_client.quote(symbol)
        if data['d'] is None:
            return -1
        return data['o']
    except Exception as e:
        print(f"Error fetching price for {symbol}")
        return -1 # Return -1 for invalid ticker symbols
