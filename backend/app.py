from webScraping import scrape_headlines
from stock import Stock
from sentimentModel import sentiment_analysis
from trade import *
from portfolio import Portfolio
from flask import Flask, jsonify
from flask_cors import CORS
from datetime import datetime


app = Flask(__name__)
CORS(app)

port = Portfolio()

def update_portfolio():
    port.load_from_file()
    port.update_prices()
    headlines = scrape_headlines()
    for stock in headlines:
        stock.sentiment_score = sentiment_analysis(stock.headline)
        if stock.sentiment_score == "positive" and is_valid_ticker(stock.ticker):
            port.buy_stock(stock.ticker, stock.headline)
        elif stock.sentiment_score == "negative" and is_valid_ticker(stock.ticker):
            port.short_stock(stock.ticker, stock.headline)

    port.update_value_log()
    port.save_to_file()

def safe_update_portfolio():
    try:
        update_portfolio()
        print("Portfolio updated successfully.")
    except Exception as e:
        print(f"An error occurred during portfolio update: {e}")
    
@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    port.load_from_file()
    return jsonify({
        "cash": port.cash,
        "value": port.value,
        "stocks": port.stocks,
        "trade_history": port.trades,
        "value_log": port.value_log
    })

@app.route('/update_portfolio', methods=['GET'])
def trigger_update():
    update_portfolio()
    return jsonify({"message": "Portfolio updated successfully"})



if __name__ == "__main__":
    app.run(debug=True)