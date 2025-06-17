import yfinance as yf


def is_valid_ticker(ticker):
    try:
        data = yf.Ticker(ticker).info
        return bool(data.get("regularMarketPrice"))

    except:
        return False