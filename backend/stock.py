class Stock:
    def __init__(self, headline, ticker, sentiment_score=None):
        self.headline = headline
        self.ticker = ticker
        self.sentiment_score = sentiment_score

    def __repr__(self):
        return f"Stock(ticker='{self.ticker}', headline='{self.headline}', sentiment={self.sentiment_score})"
