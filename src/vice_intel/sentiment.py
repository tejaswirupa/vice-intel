import pandas as pd


def analyze_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sentiment counts and percentages."""

    if "sentiment" not in df.columns:
        raise ValueError("Dataset must contain a sentiment column.")

    valid_sentiments = ["positive", "neutral", "negative"]

    if df["sentiment"].isna().any():
        raise ValueError("Sentiment values cannot be missing.")

    if not df["sentiment"].isin(valid_sentiments).all():
        raise ValueError("Dataset contains invalid sentiment labels.")

    counts = df["sentiment"].value_counts()

    result = pd.DataFrame(
        {
            "sentiment": valid_sentiments,
            "count": [int(counts.get(label, 0)) for label in valid_sentiments],
        }
    )

    total = len(df)

    if total == 0:
        result["percentage"] = 0.0
    else:
        result["percentage"] = (result["count"] / total * 100).round(2)

    return result
