import pytest

from vice_intel.analytics import calculate_positive_percentage


def test_positive_percentage():
    result = calculate_positive_percentage(75, 100)
    assert result == 75.0


def test_zero_total_raises_error():
    with pytest.raises(ValueError):
        calculate_positive_percentage(0, 0)


def test_positive_count_cannot_exceed_total():
    with pytest.raises(ValueError):
        calculate_positive_percentage(120, 100)
