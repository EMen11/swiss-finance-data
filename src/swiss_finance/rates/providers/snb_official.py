"""Official SNB data provider."""
import time
import requests
import pandas as pd
from typing import Any, Dict
from ...core.base import BaseFetcher
from ...core.exceptions import SNBAPIError, DataValidationError
from ...core.validators import validate_rate, validate_dataframe


class SNBOfficialProvider(BaseFetcher):
    """Fetcher for Swiss National Bank official API."""

    BASE_URL = "https://data.snb.ch/api/cube"
    POLICY_RATE_CUBE = "snboffzisa"
    TIMEOUT = 30

    def fetch(
        self,
        cube: str,
        params: Dict[str, Any] = None,
        retries: int = 3
    ) -> Dict[str, Any]:
        """
        Fetch data from SNB API with retry logic.

        Args:
            cube: Cube ID (e.g., 'snboffzisa')
            params: Optional query parameters (fromDate, toDate)
            retries: Number of retry attempts

        Returns:
            Parsed JSON response

        Raises:
            SNBAPIError: If API call fails after all retries
        """
        url = f"{self.BASE_URL}/{cube}/data/json/en"
        last_error = None

        for attempt in range(retries):
            try:
                response = requests.get(
                    url,
                    params=params,
                    timeout=self.TIMEOUT,
                    headers={"User-Agent": "swiss-finance-data/0.1.0"}
                )
                response.raise_for_status()
                return response.json()

            except requests.Timeout as e:
                last_error = e
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue

            except requests.HTTPError as e:
                # Ne pas retry sur les erreurs client 4xx
                raise SNBAPIError(
                    f"SNB API HTTP error: {e}. "
                    "Check https://data.snb.ch/"
                )

            except requests.RequestException as e:
                last_error = e
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue

            except ValueError as e:
                raise SNBAPIError(f"Invalid JSON response from SNB: {e}")

        raise SNBAPIError(
            f"SNB API failed after {retries} attempts. "
            f"Last error: {last_error}. "
            "Check https://data.snb.ch/ or try again later."
        )

    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Validate SNB API response structure.

        Args:
            data: API response to validate

        Returns:
            True if valid

        Raises:
            DataValidationError: If validation fails
        """
        if not isinstance(data, dict):
            raise DataValidationError("Response must be a dict")

        if "timeseries" not in data:
            raise DataValidationError("Missing 'timeseries' in response")

        if not data["timeseries"]:
            raise DataValidationError("Empty timeseries in response")

        if "values" not in data["timeseries"][0]:
            raise DataValidationError("Missing 'values' in timeseries")

        return True

    def get_current_policy_rate(self) -> float:
        """
        Get current SNB policy rate.

        Returns:
            Current policy rate (percentage)

        Raises:
            SNBAPIError: If fetch fails
            DataValidationError: If data invalid
        """
        data = self.fetch(self.POLICY_RATE_CUBE)
        self.validate(data)

        values = data["timeseries"][0]["values"]
        if not values:
            raise DataValidationError("No values in response")

        latest = values[-1]
        rate = float(latest["value"])
        validate_rate(rate)

        return rate

    def get_historical_policy_rates(
        self,
        start_date: str = None,
        end_date: str = None
    ) -> pd.DataFrame:
        """
        Get historical SNB policy rates.

        Args:
            start_date: Start date (YYYY-MM), optional
            end_date: End date (YYYY-MM), optional

        Returns:
            DataFrame with date index and 'rate' column

        Raises:
            SNBAPIError: If fetch fails
            DataValidationError: If data invalid
        """
        params = {}
        if start_date:
            params["fromDate"] = start_date
        if end_date:
            params["toDate"] = end_date

        data = self.fetch(self.POLICY_RATE_CUBE, params=params)
        self.validate(data)

        values = data["timeseries"][0]["values"]

        records = [
            {
                "date": pd.to_datetime(v["date"], format="%Y-%m"),
                "rate": float(v["value"])
            }
            for v in values
        ]

        df = pd.DataFrame(records)
        validate_dataframe(df, required_columns=["date", "rate"], min_rows=1)

        return df.set_index("date").sort_index()