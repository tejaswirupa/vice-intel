import pandas as pd
import pytest

from vice_intel.sentiment import analyze_sentiment


def test_sentiment_counts_and_percentages():
    df = pd.DataFrame({"sentiment": ["positive", "positive", "negative", "neutral"]})

    result = analyze_sentiment(df)

    assert result["count"].tolist() == [2, 1, 1]
    assert result["percentage"].tolist() == [50.0, 25.0, 25.0]


def test_missing_sentiment_column():
    df = pd.DataFrame({"text": ["Great game!"]})

    with pytest.raises(ValueError):
        analyze_sentiment(df)


def test_invalid_sentiment_label():
    df = pd.DataFrame({"sentiment": ["positive", "unknown"]})

    with pytest.raises(ValueError):
        analyze_sentiment(df)


def test_empty_dataset():
    df = pd.DataFrame({"sentiment": []})

    result = analyze_sentiment(df)

    assert result["count"].sum() == 0
    assert result["percentage"].sum() == 0
