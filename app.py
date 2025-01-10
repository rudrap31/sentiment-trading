from scraping.webScraping import scrape_headlines
from models.stock import Stock
from models.sentimentModel import sentiment_analysis
from trading.trade import get_price

def main():
    headlines = scrape_headlines()
    for stock in headlines:
        stock.sentiment_score = sentiment_analysis(stock.headline)
        print(stock)
        if (stock.sentiment_score != "neutral"):
            print(get_price(stock.ticker))




if __name__ == '__main__':
    main()