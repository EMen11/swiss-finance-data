"""Public API for SMI Swiss Market Index data."""
import pandas as pd
from .providers.yfinance_provider import YFinanceProvider


class SMI:
    """Public API for Swiss Market Index (SMI) equity data."""

    @staticmethod
    def get_constituents() -> dict:
        """
        Get SMI constituents as {ticker: company_name} dict.

        Returns:
            dict mapping yfinance ticker to company name

        Example:
            >>> from swiss_finance import SMI
            >>> constituents = SMI.get_constituents()
            >>> print(constituents["NESN.SW"])  # Nestle
        """
        return YFinanceProvider().get_constituents()

    @staticmethod
    def get_prices() -> pd.DataFrame:
        """
        Get current prices for all 20 SMI constituents.

        Returns:
            DataFrame with ticker index, name and price columns

        Example:
            >>> from swiss_finance import SMI
            >>> prices = SMI.get_prices()
            >>> print(prices)
        """
        return YFinanceProvider().get_current_prices()

    @staticmethod
    def get_historical_prices(
        tickers=None,
        period="1y",
        start=None,
        end=None
    ) -> pd.DataFrame:
        """
        Get historical closing prices for SMI constituents.

        Args:
            tickers: List of tickers (default: all 20 SMI constituents)
            period: Period string e.g. "1y", "6mo", "2y" (ignored if start/end provided)
            start: Start date (YYYY-MM-DD), optional
            end: End date (YYYY-MM-DD), optional

        Returns:
            DataFrame with date index and ticker columns

        Raises:
            ValueError: If unknown tickers provided
            FetchError: If data fetch fails

        Example:
            >>> from swiss_finance import SMI
            >>> prices = SMI.get_historical_prices(period="1y")
            >>> prices = SMI.get_historical_prices(
            ...     tickers=["NESN.SW", "ROG.SW", "NOVN.SW"],
            ...     start="2023-01-01"
            ... )
        """
        if start and end and start > end:
            raise ValueError(f"start date '{start}' must be before end date '{end}'")

        return YFinanceProvider().get_historical_prices(
            tickers=tickers,
            period=period,
            start_date=start,
            end_date=end
        )

    @staticmethod
    def get_returns(
        tickers=None,
        period="1y",
        start=None,
        end=None
    ) -> pd.DataFrame:
        """
        Get daily returns for SMI constituents.

        Args:
            tickers: List of tickers (default: all 20 SMI constituents)
            period: Period string e.g. "1y", "6mo", "2y" (ignored if start/end provided)
            start: Start date (YYYY-MM-DD), optional
            end: End date (YYYY-MM-DD), optional

        Returns:
            DataFrame with date index and ticker columns (daily % returns as decimals)

        Raises:
            ValueError: If unknown tickers provided or start > end
            FetchError: If data fetch fails

        Example:
            >>> from swiss_finance import SMI, SNB
            >>> returns = SMI.get_returns(period="1y")
            >>> rf = SNB.get_saron_daily() / 100 / 252
        """
        prices = SMI.get_historical_prices(
            tickers=tickers,
            period=period,
            start=start,
            end=end
        )
        return prices.pct_change().dropna()
