
def get_news_for_ticker(ticker):
    return [
        {
            "title": f"{ticker} Q2 earnings beat expectations",
            "description": f"{ticker} reported 25% revenue growth YoY."
        },
        {
            "title": f"{ticker} announces new product launch",
            "description": f"{ticker} is entering the AI market with a new chip."
        },
        {
            "title": f"Analysts upgrade {ticker} to BUY",
            "description": f"Price target increased to $600."
        }
    ]

