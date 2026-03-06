"""Swiss Confederation bond yields provider (SNB official API)."""
import re
import requests
import pandas as pd
from ...core.base import BaseFetcher
from ...core.exceptions import SNBAPIError, FetchError
from ...core.validators import validate_dataframe

# SNB rendoblid cube returns all series; we filter by this substring in dimItem
_CONFEDERATION_MARKER = "CHF Swiss Confederation bond issues"

# Ordered list of available maturities (derived from SNB data)
AVAILABLE_MATURITIES = [
    "1y", "2y", "3y", "4y", "5y", "6y", "7y",
    "8y", "9y", "10y", "15y", "20y", "30y",
]


def _dimitem_to_label(dim_item: str) -> str | None:
    """
    Extract maturity label from SNB dimItem string.

    E.g. '... - CHF Swiss Confederation bond issues - 10 years' → '10y'
         '... - CHF Swiss Confederation bond issues - 1 year'  → '1y'
    Returns None if not a Confederation bond series.
    """
    if _CONFEDERATION_MARKER not in dim_item:
        return None
    match = re.search(r"(\d+) years?$", dim_item)
    if not match:
        return None
    return f"{match.group(1)}y"


class SNBBondsProvider(BaseFetcher):
    """Fetches Swiss Confederation bond yields from SNB official API."""

    BASE_URL = "https://data.snb.ch/api/cube"
    BONDS_CUBE = "rendoblid"
    TIMEOUT = 30
    MAX_RETRIES = 3

    def fetch(self, start_date: str = None, end_date: str = None) -> dict:
        """Fetch raw bond yield data from SNB API (all series)."""
        url = f"{self.BASE_URL}/{self.BONDS_CUBE}/data/json/en"
        params = {}
        if start_date:
            params["fromDate"] = start_date
        if end_date:
            params["toDate"] = end_date

        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, params=params, timeout=self.TIMEOUT)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if response.status_code < 500:
                    raise SNBAPIError(f"SNB API error: {e}") from e
                last_error = e
            except requests.exceptions.RequestException as e:
                last_error = e
        raise FetchError(f"SNB API unavailable after {self.MAX_RETRIES} attempts") from last_error

    def validate(self, data: dict) -> bool:
        """Validate SNB API response structure."""
        return (
            isinstance(data, dict)
            and "timeseries" in data
            and len(data["timeseries"]) > 0
            and "values" in data["timeseries"][0]
        )

    def _parse_confederation_series(self, data: dict) -> pd.DataFrame:
        """
        Parse SNB response into a wide DataFrame.
        Only keeps CHF Swiss Confederation bond series.
        Columns are maturity labels ('1y', '2y', ..., '30y').
        """
        frames = {}
        for ts in data["timeseries"]:
            header = ts.get("header", [])
            dim_item = header[0].get("dimItem", "") if header else ""
            label = _dimitem_to_label(dim_item)
            if label is None:
                continue
            values = ts.get("values", [])
            if not values:
                continue
            df_ts = pd.DataFrame(values)
            df_ts.columns = ["date", label]
            df_ts["date"] = pd.to_datetime(df_ts["date"])
            df_ts = df_ts.set_index("date")
            frames[label] = df_ts[label]

        if not frames:
            raise SNBAPIError("No Swiss Confederation bond data found in SNB response")

        df = pd.concat(frames.values(), axis=1)
        df.index.name = "date"
        df = df.sort_index()
        # Sort columns in maturity order
        ordered = [m for m in AVAILABLE_MATURITIES if m in df.columns]
        return df[ordered]

    def get_current_yield(self, maturity: str) -> float:
        """Get the latest yield for a given maturity."""
        if maturity not in AVAILABLE_MATURITIES:
            raise ValueError(
                f"Unknown maturity '{maturity}'. Available: {AVAILABLE_MATURITIES}"
            )
        data = self.fetch()
        if not self.validate(data):
            raise SNBAPIError("Invalid bond data structure from SNB API")
        df = self._parse_confederation_series(data)
        if maturity not in df.columns:
            raise SNBAPIError(f"No data available for maturity '{maturity}'")
        series = df[maturity].dropna()
        if series.empty:
            raise SNBAPIError(f"No data available for maturity '{maturity}'")
        return float(series.iloc[-1])

    def get_yield_curve(self) -> pd.DataFrame:
        """
        Get the latest yield curve (one row, all maturities).

        Returns:
            DataFrame with one row (latest date) and one column per maturity.
        """
        data = self.fetch()
        if not self.validate(data):
            raise SNBAPIError("Invalid bond data structure from SNB API")
        df = self._parse_confederation_series(data)
        return df.iloc[[-1]]

    def get_historical_yields(
        self,
        maturity: str = None,
        start_date: str = None,
        end_date: str = None,
    ) -> pd.DataFrame:
        """
        Get historical bond yields.

        Args:
            maturity: Single maturity key (e.g. '10y'). If None, returns all maturities.
            start_date: Start date (YYYY-MM-DD), optional.
            end_date: End date (YYYY-MM-DD), optional.

        Returns:
            DataFrame with date index and maturity columns (% yield).
        """
        if maturity and maturity not in AVAILABLE_MATURITIES:
            raise ValueError(
                f"Unknown maturity '{maturity}'. Available: {AVAILABLE_MATURITIES}"
            )
        data = self.fetch(start_date=start_date, end_date=end_date)
        if not self.validate(data):
            raise SNBAPIError("Invalid bond data structure from SNB API")
        df = self._parse_confederation_series(data)
        if maturity:
            df = df[[maturity]]
        validate_dataframe(df, required_columns=list(df.columns), min_rows=1)
        return df
