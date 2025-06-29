import yfinance as yf
import json
import os


def is_valid_ticker(ticker):
    try:
        data = yf.Ticker(ticker).info
        return bool(data.get("regularMarketPrice"))

    except:
        return False


WATCHLIST_PATH = "data/tickers.json"


def load_watchlist():
    if not os.path.exists(WATCHLIST_PATH):
        return []
    with open(WATCHLIST_PATH, "r") as f:
        data = json.load(f)
    return data.get("user_watchlist", [])


def save_watchlist(tickers):
    tickers = [t.strip().upper() for t in tickers if t.strip()]
    with open(WATCHLIST_PATH, "w") as f:
        json.dump({"user_watchlist": tickers}, f, indent=2)