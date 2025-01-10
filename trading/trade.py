import requests
from apikeys import API_KEY

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

print(get_price("M "))
