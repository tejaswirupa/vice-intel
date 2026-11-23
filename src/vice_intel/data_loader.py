from pathlib import Path

import pandas as pd

from vice_intel.validation import validate_dataset


def load_validated_dataset(file_path: str | Path) -> pd.DataFrame:
    """Read a CSV dataset and validate it before returning it."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path, dtype={"date": "string"})

    result = validate_dataset(df)

    if not result["valid"]:
        error_message = "; ".join(result["errors"])
        raise ValueError(f"Dataset validation failed: {error_message}")

    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")

    return df
