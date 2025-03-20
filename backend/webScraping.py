import requests
from bs4 import BeautifulSoup

from stock import Stock


def scrape_headlines():
    URL = "https://finance.yahoo.com/news/" # Use yahoo to scrape news
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.content, 'html.parser')

    headlines = soup.find('ul', class_ = 'stream-items yf-1usaaz9')
    stories = headlines.find_all('li', class_='stream-item story-item yf-1usaaz9')

    list = []
    for story in stories: # Only uses headlines which have the stock ticker included (span)
        span = story.find('span', class_='symbol')
        if span:
            span_text = span.text.strip()
            headline = story.find('h3')
            headline_text = headline.text
            list.append(Stock(headline_text, span_text, None))
    return list


        
