from webScraping import scrape_headlines
from stock import Stock
from sentimentModel import sentiment_analysis
from trade import *
from portfolio import Portfolio

def main():
    port = Portfolio()
    port.load_from_file()
    port.update_prices()
    headlines = scrape_headlines()
    for stock in headlines:
        stock.sentiment_score = sentiment_analysis(stock.headline)
        if stock.sentiment_score == "positive" and is_valid_ticker(stock.ticker):
            port.buy_stock(stock.ticker, stock.headline, 10)
        elif stock.sentiment_score == "negative" and is_valid_ticker(stock.ticker):
            port.short_stock(stock.ticker, stock.headline, 10)
    print(port.portfolio_value())
    port.save_to_file()
    
           




if __name__ == '__main__':
    main()