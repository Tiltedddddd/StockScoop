import feedparser


def get_news_for_ticker(ticker):
    ticker = ticker.upper()
    FEEDS = [

        f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US",
        "https://www.investing.com/rss/news_25.rss",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "https://www.marketwatch.com/rss/topstories"

    ]

    CLICKBAIT_KEYWORDS = [
        "millionaire", "next tesla", "explode", "hidden gem", "buy now",
        "must-buy", "could soar", "trillion-dollar", "1 stock", "unstoppable",
        "rule them all", "undervalued gem", "secret pick", "top stock to own",
        "motley fool", "investorplace", "seeking alpha", "double your money"
    ]

    articles = []

    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            summary = entry.get("summary", "")
            combined_text = (title + " " + summary).upper()

            # Skip if clickbait detected
            if any(bad_word in combined_text.lower() for bad_word in CLICKBAIT_KEYWORDS):
                continue

            # Add articles that only mention the ticker
            if ticker in combined_text:
                articles.append({
                    "title": title,
                    "description": summary,
                    "link": entry.link
                })

            # Limit to max 5 articles
            if len(articles) >= 5:
                break
        if len(articles) >= 5:
            break

    if not articles:
        articles.append({
            "title": f"No recent news found for {ticker}",
            "description": "Try again later or check your ticker"
        })

    return articles

