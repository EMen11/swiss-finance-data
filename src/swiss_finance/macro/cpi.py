"""Public API for Swiss CPI and inflation data."""
import pandas as pd
from ..core.providers import ProviderRegistry
from .providers.snb_cpi import SNBCPIProvider

ProviderRegistry.register("snb_cpi", SNBCPIProvider)


class CPI:
    """Public API for Swiss Consumer Price Index data."""

    DEFAULT_PROVIDER = "snb_cpi"

    @staticmethod
    def get_current(provider: str = None) -> float:
        """
        Get latest Swiss CPI index value.

        Returns:
            Latest CPI index value (December 2020 = 100)

        Raises:
            SNBAPIError: If the SNB API call fails

        Example:
            >>> from swiss_finance import CPI
            >>> cpi = CPI.get_current()
        """
        provider = provider or CPI.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_current_cpi()

    @staticmethod
    def get_historical(start: str = None, end: str = None, provider: str = None) -> pd.DataFrame:
        """
        Get historical Swiss CPI index values.

        Args:
            start: Start date (YYYY-MM), optional
            end: End date (YYYY-MM), optional

        Returns:
            DataFrame with date index and cpi column

        Raises:
            ValueError: If start > end
            SNBAPIError: If the SNB API call fails

        Example:
            >>> from swiss_finance import CPI
            >>> cpi = CPI.get_historical(start="2020-01")
        """
        if start and end and start > end:
            raise ValueError(f"start date '{start}' must be before end date '{end}'")
        provider = provider or CPI.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_historical_cpi(start_date=start, end_date=end)

    @staticmethod
    def get_inflation_yoy(start: str = None, end: str = None, provider: str = None) -> pd.DataFrame:
        """
        Get Swiss year-over-year inflation rate.

        Args:
            start: Start date (YYYY-MM), optional
            end: End date (YYYY-MM), optional

        Returns:
            DataFrame with date index and inflation_yoy column (percentage)

        Raises:
            ValueError: If start > end
            SNBAPIError: If the SNB API call fails

        Example:
            >>> from swiss_finance import CPI
            >>> inflation = CPI.get_inflation_yoy(start="2020-01")
            >>> print(f"Current inflation: {inflation.iloc[-1, 0]:.2f}%")
        """
        if start and end and start > end:
            raise ValueError(f"start date '{start}' must be before end date '{end}'")
        provider = provider or CPI.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_yoy_inflation(start_date=start, end_date=end)
