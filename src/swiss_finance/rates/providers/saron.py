"""SARON (Swiss Average Rate Overnight) provider."""
import requests
import pandas as pd
from datetime import datetime, timedelta
from ...core.base import BaseFetcher
from ...core.exceptions import SNBAPIError, FetchError
from ...core.validators import validate_dataframe


class SARONProvider(BaseFetcher):
    """Fetches SARON data from SNB official API."""

    BASE_URL = "https://data.snb.ch/api/cube"
    SARON_CUBE = "zimoma"
    SARON_DAILY_CUBE = "snbgwdzid"
    SARON_DIM = "SARON"
    TIMEOUT = 30
    MAX_RETRIES = 3

    def fetch(self) -> dict:
        """Fetch raw SARON monthly data from SNB API."""
        url = f"{self.BASE_URL}/{self.SARON_CUBE}/data/json/en"
        params = {"dimSel": f"D0({self.SARON_DIM})"}
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, params=params, timeout=self.TIMEOUT)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if response.status_code < 500:
                    raise SNBAPIError(f"SNB API error: {e}") from e
                if attempt == self.MAX_RETRIES - 1:
                    raise FetchError(f"SNB API unavailable after {self.MAX_RETRIES} attempts") from e
            except requests.exceptions.RequestException as e:
                if attempt == self.MAX_RETRIES - 1:
                    raise FetchError(f"Network error: {e}") from e

    def validate(self, data: dict) -> bool:
        """Validate SNB API response structure."""
        return (
            isinstance(data, dict)
            and "timeseries" in data
            and len(data["timeseries"]) > 0
            and "values" in data["timeseries"][0]
        )

    def get_current_saron(self) -> float:
        """Get current SARON monthly rate."""
        data = self.fetch()
        if not self.validate(data):
            raise SNBAPIError("Invalid SARON data structure")
        values = data["timeseries"][0]["values"]
        if not values:
            raise SNBAPIError("No SARON data available")
        return float(values[-1]["value"])

    def get_historical_saron(self, start_date=None, end_date=None):
        """Get historical SARON monthly rates as DataFrame."""
        data = self.fetch()
        if not self.validate(data):
            raise SNBAPIError("Invalid SARON data structure")
        values = data["timeseries"][0]["values"]
        df = pd.DataFrame(values)
        df.columns = ["date", "rate"]
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        validate_dataframe(df, required_columns=["rate"], min_rows=1)
        return df

    def get_current_saron_daily(self) -> float:
        """Get latest SARON daily fixing."""
        today = datetime.today()
        from_date = (today - timedelta(days=10)).strftime("%Y-%m-%d")
        to_date = today.strftime("%Y-%m-%d")
        url = f"{self.BASE_URL}/{self.SARON_DAILY_CUBE}/data/json/en"
        params = {"dimSel": "D0(SARON)", "fromDate": from_date, "toDate": to_date}
        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, params=params, timeout=self.TIMEOUT)
                response.raise_for_status()
                data = response.json()
                values = data["timeseries"][0]["values"]
                if not values:
                    raise SNBAPIError("No daily SARON data available")
                return float(values[-1]["value"])
            except requests.exceptions.HTTPError as e:
                if response.status_code < 500:
                    raise SNBAPIError(f"SNB API error: {e}") from e
                last_error = e
            except requests.exceptions.RequestException as e:
                last_error = e
        raise FetchError(f"SNB API unavailable after {self.MAX_RETRIES} attempts") from last_error

    def get_historical_saron_daily(self, start_date=None, end_date=None):
        """Get historical daily SARON fixings."""
        url = f"{self.BASE_URL}/{self.SARON_DAILY_CUBE}/data/json/en"
        params = {"dimSel": "D0(SARON)"}
        if start_date:
            params["fromDate"] = start_date
        if end_date:
            params["toDate"] = end_date
        last_error = None
        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(url, params=params, timeout=self.TIMEOUT)
                response.raise_for_status()
                data = response.json()
                values = data["timeseries"][0]["values"]
                df = pd.DataFrame(values)
                df.columns = ["date", "rate"]
                df["date"] = pd.to_datetime(df["date"])
                df = df.set_index("date").sort_index()
                validate_dataframe(df, required_columns=["rate"], min_rows=1)
                return df
            except requests.exceptions.HTTPError as e:
                if response.status_code < 500:
                    raise SNBAPIError(f"SNB API error: {e}") from e
                last_error = e
            except requests.exceptions.RequestException as e:
                last_error = e
        raise FetchError(f"SNB API unavailable after {self.MAX_RETRIES} attempts") from last_error
