def analyze_news(articles):
    # Rating numbers
    rating = {"BUY": 0, "HOLD": 0, "SELL": 0}

    for article in articles:
        # Combine title + desc and lowercase
        text = (article.get("title", "") + " " + article.get("description", "")).lower()

        # Scoring based on buzzwords lol
        if any(word in text for word in ["beats expectations", "upgrade", "record revenue", "strong growth"]):
            rating["BUY"] += 1
        elif any(word in text for word in ["missed earnings", "downgrade", "lawsuit", "decline"]):
            rating["SELL"] += 1
        else:
            rating["HOLD"] += 1

    # Pick the most common rating
    recommended_action = max(rating, key=rating.get)
    return f"Recommended action: {recommended_action}"
