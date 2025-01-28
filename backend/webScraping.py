import requests
from bs4 import BeautifulSoup

from stock import Stock


def scrape_headlines():
    URL = "https://finance.yahoo.com/news/" # Use yahoo to scrape news
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    headlines = soup.find('ul', class_ = 'story-items pb-small yf-o0ewvr')
    stories = headlines.find_all('li', class_='story-item')

    list = []
    for story in stories: # Only uses headlines which have the stock ticker included (span)
        span = story.find('span', class_='symbol')
        if span:
            span_text = span.text.strip()
            headline = story.find('h3')
            headline_text = headline.text
            list.append(Stock(headline_text, span_text, None))
    return list


        
