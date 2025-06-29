from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()


def analyze_news(articles):
    total_score = 0
    summary = []

    for article in articles:
        text = f"{article.get('title', '')} {article.get('description', '')}"
        score = analyzer.polarity_scores(text)["compound"]
        total_score += score

        sentiment = (
            "🟢 Positive" if score > 0.2 else
            "🔴 Negative" if score < -0.2 else
            "🟡 Neutral"
        )

        summary.append(f"{sentiment} — [{article['title']}]({article.get('link', '')})")

    # Overall recommendation
    avg_score = total_score / len(articles) if articles else 0
    if avg_score > 0.2:
        recommendation = "Overall: Bullish tone -- Signs of positive outlook"
    elif avg_score < -0.2:
        recommendation = "Overall: Bearish tone -- be cautious"
    else:
        recommendation = "Overall: Mixed/Neutral tone -- No clear direction yet"

    return recommendation, summary
