
from scraping.webScraping import scrape_headlines
from models.stock import Stock


def main():
    headlines = scrape_headlines()
    for stock in headlines:
        print(stock)



if __name__ == '__main__':
    main()