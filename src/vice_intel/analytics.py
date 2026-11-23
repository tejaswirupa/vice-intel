def calculate_positive_percentage(
    positive_count: int,
    total_count: int,
) -> float:
    """Calculate the percentage of positive reactions."""

    if total_count <= 0:
        raise ValueError("Total count must be greater than zero.")

    if positive_count < 0 or positive_count > total_count:
        raise ValueError("Positive count must be between 0 and total.")

    return round((positive_count / total_count) * 100, 2)
