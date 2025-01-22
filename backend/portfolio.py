import json
from datetime import datetime 
from trade import get_price
import math

class Portfolio:
    def __init__(self, initial_cash = 100000):
        self.cash = initial_cash
        self.value = initial_cash
        self.stocks = {} # Format: {"TSLA": {"quantity": 10, "type": "BUY", "buy_price": 650.0, "current_price": 700.0}}
        self.trades = []
        self.value_log = [] # List of {"time": timestamp, "value": portfolio_value}

    def buy_stock(self, ticker, headline):
        price = get_price(ticker)
        amount = math.ceil(1000/price) 
        total_cost = amount * price
        if total_cost > self.cash:
            raise ValueError("Not enough cash to execute this trade.")
        
        if ticker not in self.stocks:
            self.stocks[ticker] = {"quantity": amount, "type": "BUY", "buy_price": price, 
                                   "current_price": price, "headline": headline, "time": datetime.now().isoformat()}
            self.cash -= total_cost


    def short_stock(self, ticker, headline):
        price = get_price(ticker)
        amount = math.ceil(1000/price) 
        total_cost = amount * price
        if total_cost > self.cash:
            raise ValueError("Not enough cash to execute this trade.")
        
        if ticker not in self.stocks:
            self.stocks[ticker] = {"quantity": amount, "type": "SHORT", "buy_price": price, 
                                   "current_price": price, "headline": headline, "time": datetime.now().isoformat()}
            self.cash -= total_cost

            

    def check_take_profit_stop_loss(self, ticker):
        position = self.stocks[ticker]
        entry_price = position["buy_price"]
        current_price = position["current_price"]
        
        if position["type"] == "BUY":
            if current_price >= entry_price * 1.05:  # 5% take profit
                return True
            elif current_price <= entry_price * 0.97:  # 3% stop loss
                return True
        elif position["type"] == "SHORT":
            if current_price <= entry_price * 0.95:  # 5% take profit
                return True
            elif current_price >= entry_price * 1.03:  # 3% stop loss
                return True
        return False
    
    def close_trade(self, ticker, current_price):
        position = self.stocks[ticker]
        if position["type"] == "BUY":
            profit = (current_price - position["buy_price"]) * position["quantity"]
        elif position["type"] == "SHORT":
            profit = (position["buy_price"] - current_price) * position["quantity"]

        self.cash +=  position["buy_price"] * position["quantity"] + profit
        self.trades.append({
            "action": position["type"],
            "ticker": ticker,
            "headline": position["headline"],
            "buy_price": position["buy_price"],
            "sold_price": current_price,
            "amount": position["quantity"],
            "time": datetime.now().isoformat(),
            "profit": profit
        })
        del self.stocks[ticker]

    def update_prices(self):
        tickers_to_close = []
    
        for ticker in self.stocks:
            self.stocks[ticker]["current_price"] = get_price(ticker)
            if self.check_take_profit_stop_loss(ticker):
                tickers_to_close.append(ticker)
        
        for ticker in tickers_to_close:
            self.close_trade(ticker, self.stocks[ticker]["current_price"])

    def update_value_log(self):
        self.value = self.portfolio_value()
        current_time = datetime.now().isoformat()
        self.value_log.append({"time": current_time, "value": self.portfolio_value()})

    def update_trade_history(self):
        for dict in self.trades:
            tick = dict["ticker"]
            dict["current_price"] = get_price(tick)

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
            "value": self.value,
            "stocks": self.stocks,
            "trade_history": self.trades,
            "value_log": self.value_log
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    def load_from_file(self, file_path="portfolio.json"):
        defaults = {
        "cash": 100000,
        "value": 100000,
        "stocks": {},
        "trade_history": [],
        "value_log": []
        }
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # If the file is empty or invalid, start fresh
                if not data:
                    raise ValueError("File is empty. Starting fresh.")
        except (FileNotFoundError, ValueError):
            print("No valid portfolio data found. Starting fresh.")
            data = defaults  # Use default values

        self.cash = data.get("cash", 100000) 
        self.value = data.get("value", 100000)
        self.stocks = data.get("stocks", {})
        self.trades = data.get("trade_history", [])
        self.value_log = data.get("value_log", [])
        


        