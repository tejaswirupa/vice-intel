import pandas as pd
import pytest

from vice_intel.validation import validate_dataset


@pytest.fixture
def valid_dataset():
    """Create a small, valid dataset for testing."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "date": [
                "2026-11-01",
                "2026-11-02",
                "2026-11-03",
            ],
            "source": ["demo", "demo", "demo"],
            "text": [
                "Amazing graphics!",
                "I can't wait to play!",
                "I hope performance is good.",
            ],
            "sentiment": ["positive", "positive", "neutral"],
        }
    )


def test_valid_dataset(valid_dataset):
    result = validate_dataset(valid_dataset)

    assert result["valid"] is True
    assert result["errors"] == []


def test_missing_column(valid_dataset):
    df = valid_dataset.drop(columns=["sentiment"])

    result = validate_dataset(df)

    assert result["valid"] is False
    assert any("Missing required columns" in e for e in result["errors"])


def test_duplicate_ids(valid_dataset):
    df = valid_dataset.copy()
    df.loc[1, "id"] = 1

    result = validate_dataset(df)

    assert result["valid"] is False
    assert "Dataset contains duplicate IDs." in result["errors"]


def test_invalid_sentiment(valid_dataset):
    df = valid_dataset.copy()
    df.loc[0, "sentiment"] = "excited"

    result = validate_dataset(df)

    assert result["valid"] is False
    assert "Dataset contains invalid sentiment labels." in result["errors"]


def test_missing_values(valid_dataset):
    df = valid_dataset.copy()
    df.loc[0, "text"] = None

    result = validate_dataset(df)

    assert result["valid"] is False
    assert "Dataset contains missing values." in result["errors"]


def test_invalid_date(valid_dataset):
    df = valid_dataset.copy()
    df.loc[0, "date"] = "not-a-date"

    result = validate_dataset(df)

    assert result["valid"] is False
    assert "Dataset contains invalid dates." in result["errors"]


def test_empty_dataset(valid_dataset):
    df = valid_dataset.iloc[0:0]

    result = validate_dataset(df)

    assert result["valid"] is False
    assert "Dataset contains no records." in result["errors"]


def test_blank_reaction_text(valid_dataset):
    df = valid_dataset.copy()
    df.loc[0, "text"] = "   "

    result = validate_dataset(df)

    assert result["valid"] is False
    assert "Dataset contains empty reaction text." in result["errors"]
