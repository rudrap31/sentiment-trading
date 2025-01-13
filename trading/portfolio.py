import json
from trading.trade import get_price

class Portfolio:
    def __init__(self, initial_cash = 100000):
        self.cash = initial_cash
        self.stocks = {} # Format: {"TSLA": {"quantity": 10, "buy_price": 650.0, "current_price": 700.0}}
        self.trades = []

    def buy_stock(self, ticker, price, amount):
        total_cost = amount * price
        if total_cost > self.cash:
            raise ValueError("Not enough cash to execute this trade.")
        
        if ticker not in self.stocks:
            self.stocks[ticker] = {"quantity": amount, "buy_price": price, "current_price": price}
            self.cash -= total_cost
            self.trades.append({"action": "BUY", "ticker": ticker, "price": price, "amount": amount})

    def sell_stock(self, ticker, price, amount): #unfinished
        if ticker not in self.stocks or self.stocks[ticker]["quantity"] < amount:
            raise ValueError("Not enough stock to sell.")

        stock = self.stocks[ticker]
        total_value = amount * price
        stock["quantity"] -= amount

        if stock["quantity"] == 0:
            del self.stocks[ticker] 

        self.cash += total_value
        self.trades.append({"action": "SELL", "ticker": ticker, "price": price, "amount": amount})

    def update_prices(self):
        for ticker in self.stocks:
            self.stocks[ticker]["current_price"] = get_price(ticker)

    def portfolio_value(self):
        sum = self.cash
        for ticker in self.stocks:
            sum += self.stocks[ticker]["quantity"] * self.stocks[ticker]["current_price"]
        return sum

    def save_to_file(self, file_path="portfolio.json"):
        data = {
            "cash": self.cash,
            "stocks": self.stocks,
            "trade_history": self.trades,
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def load_from_file(self, file_path="portfolio.json"):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                self.cash = data["cash"]
                self.stocks = data["stocks"]
                self.trades = data["trade_history"]
        except FileNotFoundError:
            print("No saved portfolio found. Starting fresh.")


        