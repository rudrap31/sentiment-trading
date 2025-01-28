from webScraping import scrape_headlines
from sentimentModel import sentiment_analysis
from portfolio import Portfolio
from flask import Flask, jsonify
from flask_cors import CORS
from trade import get_price


app = Flask(__name__)
CORS(app)

port = Portfolio()

def update_portfolio():
    port.load_from_file()
    port.update_prices()
    headlines = scrape_headlines() # Scrape headlines and get all of the sentiment scores

    for stock in headlines:
        stock.sentiment_score = sentiment_analysis(stock.headline)
        price = get_price(stock.ticker)
        if price == -1:
            continue
        if stock.sentiment_score == "positive":
            port.trade_stock(stock.ticker, stock.headline, price, "BUY")
        elif stock.sentiment_score == "negative":
            port.trade_stock(stock.ticker, stock.headline, price, "SHORT")

    port.update_value_log()
    port.save_to_file()

    
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

@app.route('/update_portfolio', methods=['GET']) # For manual updates
def trigger_update():
    update_portfolio()
    return jsonify({"message": "Portfolio updated successfully"})


if __name__ == "__main__":
    app.run(debug=True)