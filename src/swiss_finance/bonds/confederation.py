"""Public API for Swiss Confederation bond yields."""
import pandas as pd
from ..core.providers import ProviderRegistry
from .providers.snb_bonds import SNBBondsProvider, AVAILABLE_MATURITIES

ProviderRegistry.register("snb_bonds", SNBBondsProvider)


class Bonds:
    """Public API for Swiss Confederation government bond yields."""

    DEFAULT_PROVIDER = "snb_bonds"

    @staticmethod
    def list_maturities() -> list:
        """
        List available bond maturities.

        Returns:
            List of maturity strings, e.g. ['2y', '3y', ..., '30y']

        Example:
            >>> from swiss_finance import Bonds
            >>> Bonds.list_maturities()
        """
        return list(AVAILABLE_MATURITIES)

    @staticmethod
    def get_yield(maturity: str = "10y", provider: str = None) -> float:
        """
        Get the latest yield for a given Swiss Confederation bond maturity.

        Args:
            maturity: Bond maturity, e.g. '1y', '2y', '5y', '10y', '30y'. Default: '10y'.
            provider: Data provider (default: 'snb_bonds')

        Returns:
            Yield in percent (e.g. 0.85 means 0.85%)

        Raises:
            ValueError: If maturity is not in the available list
            SNBAPIError: If the SNB API call fails

        Example:
            >>> from swiss_finance import Bonds
            >>> yield_10y = Bonds.get_yield("10y")
            >>> print(f"10y Confederation bond yield: {yield_10y:.2f}%")
        """
        provider = provider or Bonds.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_current_yield(maturity)

    @staticmethod
    def get_yield_curve(provider: str = None) -> pd.DataFrame:
        """
        Get the latest Swiss Confederation yield curve (all maturities).

        Returns:
            DataFrame with one row (latest date) and one column per maturity.
            Columns are '1y', '2y', ..., '30y'. Values are yields in percent.

        Raises:
            SNBAPIError: If the SNB API call fails

        Example:
            >>> from swiss_finance import Bonds
            >>> curve = Bonds.get_yield_curve()
            >>> print(curve)
        """
        provider = provider or Bonds.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_yield_curve()

    @staticmethod
    def get_historical_yields(
        maturity: str = None,
        start: str = None,
        end: str = None,
        provider: str = None,
    ) -> pd.DataFrame:
        """
        Get historical Swiss Confederation bond yields.

        Args:
            maturity: Bond maturity, e.g. '10y'. If None, returns all maturities.
            start: Start date (YYYY-MM-DD), optional.
            end: End date (YYYY-MM-DD), optional.

        Returns:
            DataFrame with date index and maturity column(s). Values in percent.

        Raises:
            ValueError: If maturity is unknown or start > end
            SNBAPIError: If the SNB API call fails

        Example:
            >>> from swiss_finance import Bonds
            >>> hist = Bonds.get_historical_yields(maturity="10y", start="2020-01-01")
            >>> hist_all = Bonds.get_historical_yields(start="2023-01-01")
        """
        if start and end and start > end:
            raise ValueError(f"start date '{start}' must be before end date '{end}'")
        provider = provider or Bonds.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_historical_yields(
            maturity=maturity,
            start_date=start,
            end_date=end,
        )
