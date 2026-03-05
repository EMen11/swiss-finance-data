"""Data validation utilities."""
import pandas as pd
from .exceptions import DataValidationError


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: list,
    min_rows: int = 1
) -> None:
    """
    Validate DataFrame structure.

    Args:
        df: DataFrame to validate
        required_columns: List of required column names
        min_rows: Minimum number of rows required

    Raises:
        DataValidationError: If validation fails
    """
    if not isinstance(df, pd.DataFrame):
        raise DataValidationError("Data must be a pandas DataFrame")

    if df.empty and min_rows > 0:
        raise DataValidationError(
            "No data available for the requested date range. "
            "Check that your dates are not in the future and "
            "that the SNB API has data for this period."
        )

    if len(df) < min_rows:
        raise DataValidationError(
            f"DataFrame has {len(df)} rows, expected at least {min_rows}"
        )

    missing = set(required_columns) - set(df.columns)
    if missing:
        raise DataValidationError(
            f"Missing required columns: {missing}"
        )


def validate_rate(rate: float) -> None:
    """
    Validate interest rate value.

    Args:
        rate: Interest rate (percentage)

    Raises:
        DataValidationError: If rate is unreasonable
    """
    if not isinstance(rate, (int, float)):
        raise DataValidationError(f"Rate must be numeric, got {type(rate)}")

    if not -20 <= rate <= 20:
        raise DataValidationError(
            f"Rate {rate}% seems unreasonable (expected -20% to 20%)"
        )