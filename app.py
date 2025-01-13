from scraping.webScraping import scrape_headlines
from models.stock import Stock
from models.sentimentModel import sentiment_analysis
from trading.trade import *
from trading.portfolio import Portfolio

def main():
    port = Portfolio()
    port.load_from_file()
    headlines = scrape_headlines()
    for stock in headlines:
        stock.sentiment_score = sentiment_analysis(stock.headline)
        if stock.sentiment_score == "positive" and is_valid_ticker(stock.ticker):
            port.buy_stock(stock.ticker, get_price(stock.ticker), 10)
    port.update_prices()
    print(port.portfolio_value())
    port.save_to_file()
    
           




if __name__ == '__main__':
    main()