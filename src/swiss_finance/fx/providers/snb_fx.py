"""SNB FX rates provider."""
import requests
import pandas as pd
from ...core.base import BaseFetcher
from ...core.exceptions import SNBAPIError, FetchError
from ...core.validators import validate_dataframe

SUPPORTED_CURRENCIES = {
    "EUR": "EUR1",
    "USD": "USD1",
    "GBP": "GBP1",
    "JPY": "JPY100",
    "CAD": "CAD1",
    "AUD": "AUD1",
    "SEK": "SEK100",
    "NOK": "NOK100",
    "DKK": "DKK100",
}


class SNBFXProvider(BaseFetcher):
    """Fetches CHF exchange rates from SNB official API."""

    BASE_URL = "https://data.snb.ch/api/cube"
    FX_CUBE = "devkum"
    TIMEOUT = 30
    MAX_RETRIES = 3

    def fetch(self, currency: str = "EUR", average: bool = True) -> dict:
        """Fetch raw FX data from SNB API."""
        if currency not in SUPPORTED_CURRENCIES:
            raise ValueError(
                f"Currency '{currency}' not supported. "
                f"Supported: {list(SUPPORTED_CURRENCIES.keys())}"
            )

        dim_type = "M0" if average else "M1"
        currency_code = SUPPORTED_CURRENCIES[currency]
        url = f"{self.BASE_URL}/{self.FX_CUBE}/data/json/en"
        params = {"dimSel": f"D0({dim_type}),D1({currency_code})"}

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

    def get_current_rate(self, currency: str = "EUR") -> float:
        """Get current CHF exchange rate for a currency."""
        data = self.fetch(currency=currency)
        if not self.validate(data):
            raise SNBAPIError(f"Invalid FX data for {currency}")

        values = data["timeseries"][0]["values"]
        if not values:
            raise SNBAPIError(f"No FX data available for {currency}")

        raw = float(values[-1]["value"])
        # JPY, SEK, NOK, DKK are quoted per 100 units
        if SUPPORTED_CURRENCIES[currency].endswith("100"):
            return round(raw / 100, 6)
        return round(raw, 6)

    def get_historical_rates(
        self,
        currency: str = "EUR",
        start_date: str = None,
        end_date: str = None,
    ) -> pd.DataFrame:
        """Get historical CHF exchange rates as DataFrame."""
        data = self.fetch(currency=currency)
        if not self.validate(data):
            raise SNBAPIError(f"Invalid FX data for {currency}")

        values = data["timeseries"][0]["values"]
        df = pd.DataFrame(values)
        df.columns = ["date", "rate"]
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()

        # Normalize per-100 currencies
        if SUPPORTED_CURRENCIES[currency].endswith("100"):
            df["rate"] = df["rate"] / 100

        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]

        validate_dataframe(df, required_columns=["rate"], min_rows=1)
        return df

    @staticmethod
    def list_currencies() -> list:
        """List supported currencies."""
        return list(SUPPORTED_CURRENCIES.keys())