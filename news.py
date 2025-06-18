import feedparser


def get_news_for_ticker(ticker):
    ticker = ticker.upper()
    FEEDS = [
        "https://investorplace.com/feed/",
        f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={ticker}&region=US&lang=en-US",
        "https://www.investing.com/rss/news_25.rss"
    ]

    articles = []

    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            title = entry.title
            summary = entry.get("summary", "")
            combined_text = (title + " " + summary).upper()

            # Add articles that only mention the ticker
            if ticker in combined_text:
                articles.append({
                    "title": title,
                    "description": summary
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

