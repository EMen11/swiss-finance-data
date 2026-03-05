"""Swiss CPI provider."""
import requests
import pandas as pd
from ...core.base import BaseFetcher
from ...core.exceptions import SNBAPIError, FetchError
from ...core.validators import validate_dataframe


class SNBCPIProvider(BaseFetcher):
    """Fetches Swiss CPI data from SNB official API."""

    BASE_URL = "https://data.snb.ch/api/cube"
    CPI_CUBE = "plkopr"
    TIMEOUT = 30
    MAX_RETRIES = 3

    def fetch(self) -> dict:
        """Fetch raw CPI data from SNB API."""
        url = f"{self.BASE_URL}/{self.CPI_CUBE}/data/json/en"
        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, timeout=self.TIMEOUT)
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

    def get_current_cpi(self) -> float:
        """Get latest Swiss CPI index value."""
        data = self.fetch()
        if not self.validate(data):
            raise SNBAPIError("Invalid CPI data structure")
        values = data["timeseries"][0]["values"]
        if not values:
            raise SNBAPIError("No CPI data available")
        return float(values[-1]["value"])

    def get_historical_cpi(self, start_date=None, end_date=None) -> pd.DataFrame:
        """Get historical Swiss CPI as DataFrame."""
        data = self.fetch()
        if not self.validate(data):
            raise SNBAPIError("Invalid CPI data structure")
        values = data["timeseries"][0]["values"]
        df = pd.DataFrame(values)
        df.columns = ["date", "cpi"]
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        validate_dataframe(df, required_columns=["cpi"], min_rows=1)
        return df

    def get_yoy_inflation(self, start_date=None, end_date=None) -> pd.DataFrame:
        """Get Swiss YoY inflation rate (percentage change vs same month prior year)."""
        df = self.get_historical_cpi()
        df["inflation_yoy"] = df["cpi"].pct_change(12) * 100
        df = df.dropna()
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        validate_dataframe(df, required_columns=["inflation_yoy"], min_rows=1)
        return df[["inflation_yoy"]]
