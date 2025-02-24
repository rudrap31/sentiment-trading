from webScraping import scrape_headlines
from sentimentModel import sentiment_analysis
from portfolio import Portfolio
from flask import Flask, jsonify
from flask_cors import CORS
from trade import get_market_status


app = Flask(__name__)
CORS(app)

port = Portfolio()

def update_portfolio():
    port.load_from_file()
    status = get_market_status()
    print(status)
    if status: # if market is open buy/short the queued stocks
        port.trade_queued()
    port.update_prices()
    headlines = scrape_headlines() # Scrape headlines and get all of the sentiment scores

    for stock in headlines: # if market is closed queue stocks, instead of buyin
        stock.sentiment_score = sentiment_analysis(stock.headline)
        if stock.sentiment_score == "positive":
            if status:
                port.trade_stock(stock.ticker, stock.headline, "BUY")
            else:
                port.queue_trade(stock.ticker, stock.headline, "BUY")
        elif stock.sentiment_score == "negative":
            if status:
                port.trade_stock(stock.ticker, stock.headline, "SHORT")
            else:
                port.queue_trade(stock.ticker, stock.headline, "SHORT")

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