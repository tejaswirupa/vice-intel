import pandas as pd
import pytest

from vice_intel.data_loader import load_validated_dataset


def test_load_valid_dataset(tmp_path):
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "date": ["2026-11-01", "2026-11-02"],
            "source": ["demo", "demo"],
            "text": ["Great graphics!", "Looking forward to it!"],
            "sentiment": ["positive", "positive"],
        }
    )

    file_path = tmp_path / "valid.csv"
    df.to_csv(file_path, index=False)

    result = load_validated_dataset(file_path)

    assert len(result) == 2
    assert pd.api.types.is_datetime64_any_dtype(result["date"])


def test_load_invalid_dataset(tmp_path):
    df = pd.DataFrame(
        {
            "id": [1, 1],
            "date": ["2026-11-01", "2026-11-02"],
            "source": ["demo", "demo"],
            "text": ["Amazing!", "Fantastic!"],
            "sentiment": ["positive", "positive"],
        }
    )

    file_path = tmp_path / "invalid.csv"
    df.to_csv(file_path, index=False)

    with pytest.raises(ValueError, match="duplicate IDs"):
        load_validated_dataset(file_path)


def test_missing_dataset(tmp_path):
    file_path = tmp_path / "nonexistent.csv"

    with pytest.raises(FileNotFoundError):
        load_validated_dataset(file_path)
