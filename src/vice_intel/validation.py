import pandas as pd

REQUIRED_COLUMNS = {"id", "date", "source", "text", "sentiment"}
VALID_SENTIMENTS = {"positive", "neutral", "negative"}


def validate_dataset(df: pd.DataFrame) -> dict:
    """Validate a GTA VI sentiment dataset."""

    errors = []

    # Check required columns
    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        errors.append(f"Missing required columns: {sorted(missing_columns)}")

        return {"valid": False, "errors": errors}

    # Check for empty datasets
    if df.empty:
        errors.append("Dataset contains no records.")

    # Check for missing values
    if df[list(REQUIRED_COLUMNS)].isna().any().any():
        errors.append("Dataset contains missing values.")

    # Check for duplicate IDs
    if df["id"].duplicated().any():
        errors.append("Dataset contains duplicate IDs.")

    # Validate sentiment labels
    if not df["sentiment"].dropna().isin(VALID_SENTIMENTS).all():
        errors.append("Dataset contains invalid sentiment labels.")

    # Check for empty text
    if df["text"].dropna().astype(str).str.strip().eq("").any():
        errors.append("Dataset contains empty reaction text.")

    # Check date format (YYYY-MM-DD)
    invalid_dates = pd.to_datetime(
        df["date"],
        format="%Y-%m-%d",
        errors="coerce",
    ).isna()

    if invalid_dates.any():
        errors.append("Dataset contains invalid dates.")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
    }
