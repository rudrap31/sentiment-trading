import json
from datetime import datetime 
from trade import get_price

class Portfolio:
    def __init__(self, initial_cash = 100000):
        self.cash = initial_cash
        self.stocks = {} # Format: {"TSLA": {"quantity": 10, "type": "BUY", "buy_price": 650.0, "current_price": 700.0}}
        self.trades = []

    def buy_stock(self, ticker, headline, amount):
        price = get_price(ticker)
        total_cost = amount * price
        if total_cost > self.cash:
            raise ValueError("Not enough cash to execute this trade.")
        
        if ticker not in self.stocks:
            self.stocks[ticker] = {"quantity": amount, "type": "BUY", "buy_price": price, "current_price": price}
            self.cash -= total_cost
            self.trades.append({"action": "BUY", 
                                "ticker": ticker, 
                                "price": price, 
                                "amount": amount,
                                "time": datetime.now().isoformat(),
                                "headline": headline})

    def short_stock(self, ticker, headline, amount):
        price = get_price(ticker)
        total_cost = amount * price
        if total_cost > self.cash:
            raise ValueError("Not enough cash to execute this trade.")
        
        if ticker not in self.stocks:
            self.stocks[ticker] = {"quantity": amount, "type": "SHORT", "buy_price": price, "current_price": price}
            self.trades.append({"action": "SHORT", 
                                "ticker": ticker, 
                                "price": price, 
                                "amount": amount,
                                "time": datetime.now().isoformat(),
                                "headline": headline})


    def update_prices(self):
        for ticker in self.stocks:
            self.stocks[ticker]["current_price"] = get_price(ticker)

    def portfolio_value(self):
        sum = self.cash
        for ticker in self.stocks:
            if self.stocks[ticker]["type"] == "BUY":
                sum += self.stocks[ticker]["quantity"] * self.stocks[ticker]["current_price"]
            else:
                sum += self.stocks[ticker]["quantity"] * (self.stocks[ticker]["buy_price"] - self.stocks[ticker]["current_price"])
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


        