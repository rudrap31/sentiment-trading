import json
from datetime import datetime 
from trade import get_price, get_open_price
import math

class Portfolio:
    def __init__(self, initial_cash = 100000):
        self.cash = initial_cash
        self.value = initial_cash
        self.stocks = {} # Current Active Trades
        self.queued_trades = {} # Current Queued Trades
        self.trades = [] # Completed Closed Trades
        self.value_log = [] # List of {"time": timestamp, "value": portfolio_value}

    def queue_trade(self, ticker, headline, type):
        if ticker not in self.queued_trades:
            self.queued_trades[ticker] = {"headline": headline, "type": type}

    def trade_queued(self):
        tickers_to_close = []
        for ticker, trade in self.queued_trades.items():
            open_price = get_open_price(ticker)
            if open_price == -1:
                tickers_to_close.append(ticker)
                continue
            
            self.trade_stock(ticker, trade["headline"], trade["type"], open_price)
            tickers_to_close.append(ticker)

        for ticker in tickers_to_close:
            del self.queued_trades[ticker]

    
    def trade_stock(self, ticker, headline, type, price=None):
        price = price if price else get_price(ticker)
        if price == -1:
            return
        
        amount = math.ceil(1000/price) # Buy around $1000 worth of the stock
        total_cost = amount * price
        if total_cost > self.cash:
            raise ValueError("Not enough cash to execute this trade.")
        
        if ticker not in self.stocks:
            self.stocks[ticker] = {"quantity": amount, "type": type, "buy_price": price, 
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
    
        for ticker in self.stocks: # Update prices and check for stop loss/ take profits
            price = get_price(ticker)
            if price != -1: # If api call limit reached, keeps the price the same
                self.stocks[ticker]["current_price"] = price 
            if self.check_take_profit_stop_loss(ticker):
                tickers_to_close.append(ticker)
        
        for ticker in tickers_to_close: # Close trades
            self.close_trade(ticker, self.stocks[ticker]["current_price"])
        self.value = self.portfolio_value()

    def update_value_log(self):
        current_time = datetime.now().isoformat()
        self.value_log.append({"time": current_time, "value": self.value})


    def portfolio_value(self):
        sum = self.cash
        for ticker in self.stocks:
            if self.stocks[ticker]["type"] == "BUY":
                sum += self.stocks[ticker]["quantity"] * self.stocks[ticker]["current_price"]
            else:
                reserved_margin = self.stocks[ticker]["quantity"] * self.stocks[ticker]["buy_price"]
                profit_or_loss = self.stocks[ticker]["quantity"] * (self.stocks[ticker]["buy_price"] - self.stocks[ticker]["current_price"])
                sum += reserved_margin + profit_or_loss
        return sum

    def save_to_file(self, file_path="portfolio.json"):
        data = {
            "cash": self.cash,
            "value": self.value,
            "stocks": self.stocks,
            "queued_trades": self.queued_trades,
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
        "queued_trades": {},
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
        self.queued_trades = data.get("queued_trades", {})
        self.trades = data.get("trade_history", [])
        self.value_log = data.get("value_log", [])