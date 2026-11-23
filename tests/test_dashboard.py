from pathlib import Path

from streamlit.testing.v1 import AppTest

APP_PATH = (
    Path(__file__).resolve().parents[1] / "src" / "vice_intel" / "dashboard" / "app.py"
)


def test_dashboard_loads_valid_data():
    """Dashboard should load our valid demo dataset."""
    app = AppTest.from_file(str(APP_PATH)).run()

    assert not app.exception
    assert len(app.metric) == 4
    assert app.metric[0].value == "12"


def test_dashboard_has_demo_disclaimer():
    """Dashboard should clearly identify synthetic data."""
    app = AppTest.from_file(str(APP_PATH)).run()

    assert not app.exception
    assert any("DEMO MODE" in message.value for message in app.info)


def test_invalid_csv_is_rejected(tmp_path):
    """Verify that an invalid CSV fails data validation."""
    import pandas as pd

    from vice_intel.validation import validate_dataset

    invalid_data = pd.DataFrame(
        {
            "id": [1, 1],
            "date": ["2026-11-01", "2026-11-02"],
            "source": ["demo", "demo"],
            "text": ["Great graphics!", "Amazing trailer!"],
            "sentiment": ["positive", "negative"],
        }
    )

    # Create a temporary file without modifying real data.
    test_csv = tmp_path / "invalid_sentiment.csv"
    invalid_data.to_csv(test_csv, index=False)

    # Read the CSV exactly as a real data pipeline would.
    loaded_data = pd.read_csv(test_csv)

    # Verify that duplicate IDs are detected.
    result = validate_dataset(loaded_data)

    assert result["valid"] is False
    assert "Dataset contains duplicate IDs." in result["errors"]
