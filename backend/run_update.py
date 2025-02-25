from webScraping import scrape_headlines
from sentimentModel import sentiment_analysis
from portfolio import Portfolio
from trade import get_market_status

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

if __name__ == "__main__": # Handles any potential errors
    try:
        update_portfolio()
        print("Portfolio updated successfully.")
    except Exception as e:
        print(f"An error occurred during portfolio update: {e}")