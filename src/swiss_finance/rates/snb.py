"""Swiss National Bank (SNB) rates API."""
import pandas as pd
from ..core.providers import ProviderRegistry
from .providers.snb_official import SNBOfficialProvider
from .providers.saron import SARONProvider

# Auto-register providers
ProviderRegistry.register("snb_official", SNBOfficialProvider)
ProviderRegistry.register("saron", SARONProvider)


class SNB:
    """Public API for Swiss National Bank data."""

    DEFAULT_PROVIDER = "snb_official"

    @staticmethod
    def get_policy_rate(provider: str = None) -> float:
        """
        Get current SNB policy rate.

        Args:
            provider: Data provider to use (default: 'snb_official')

        Returns:
            Current policy rate (percentage)

        Example:
            >>> from swiss_finance import SNB
            >>> rate = SNB.get_policy_rate()
            >>> print(f"SNB Rate: {rate}%")
        """
        provider = provider or SNB.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_current_policy_rate()

    @staticmethod
    def get_historical_rates(
        start: str = None,
        end: str = None,
        provider: str = None
    ) -> pd.DataFrame:
        """
        Get historical SNB policy rates.

        Args:
            start: Start date (YYYY-MM), optional
            end: End date (YYYY-MM), optional
            provider: Data provider to use (default: 'snb_official')

        Returns:
            DataFrame with date index and 'rate' column

        Raises:
            ValueError: If start > end

        Example:
            >>> from swiss_finance import SNB
            >>> rates = SNB.get_historical_rates(start='2020-01')
        """
        if start and end and start > end:
            raise ValueError(
                f"start date '{start}' must be before end date '{end}'"
            )

        provider = provider or SNB.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_historical_policy_rates(
            start_date=start,
            end_date=end
        )

    @staticmethod
    def get_saron(provider: str = None) -> float:
        """
        Get current SARON monthly average.

        The SARON is the risk-free reference rate for CHF,
        replacing LIBOR CHF since 2021.

        Returns:
            Current SARON monthly average (percentage)

        Example:
            >>> from swiss_finance import SNB
            >>> rf = SNB.get_saron() / 100  # as decimal for Sharpe ratio
        """
        fetcher = SARONProvider()
        return fetcher.get_current_saron()

    @staticmethod
    def get_historical_saron(
        start: str = None,
        end: str = None
    ) -> pd.DataFrame:
        """
        Get historical SARON monthly averages.

        Args:
            start: Start date (YYYY-MM), optional
            end: End date (YYYY-MM), optional

        Returns:
            DataFrame with date index and 'rate' column

        Example:
            >>> from swiss_finance import SNB
            >>> saron = SNB.get_historical_saron(start='2021-01')
        """
        if start and end and start > end:
            raise ValueError(
                f"start date '{start}' must be before end date '{end}'"
            )

        fetcher = SARONProvider()
        return fetcher.get_historical_saron(
            start_date=start,
            end_date=end
        )

    @staticmethod
    def get_saron_daily() -> float:
        """
        Get latest SARON daily fixing.

        Published at the close of each business day.
        More granular than monthly average — use for daily risk calculations.

        Returns:
            Latest SARON daily fixing (percentage)

        Example:
            >>> from swiss_finance import SNB
            >>> saron = SNB.get_saron_daily()
            >>> rf_daily = saron / 100 / 252  # daily risk-free rate
        """
        fetcher = SARONProvider()
        return fetcher.get_current_saron_daily()

    @staticmethod
    def get_historical_saron_daily(
        start: str = None,
        end: str = None
    ) -> pd.DataFrame:
        """
        Get historical daily SARON fixings.

        Args:
            start: Start date (YYYY-MM-DD), optional
            end: End date (YYYY-MM-DD), optional

        Returns:
            DataFrame with date index and 'rate' column (business days only)

        Example:
            >>> from swiss_finance import SNB
            >>> saron = SNB.get_historical_saron_daily(start='2024-01-01')
        """
        if start and end and start > end:
            raise ValueError(
                f"start date '{start}' must be before end date '{end}'"
            )

        fetcher = SARONProvider()
        return fetcher.get_historical_saron_daily(
            start_date=start,
            end_date=end
        )

    @staticmethod
    def list_providers() -> list:
        """List available SNB data providers."""
        return ProviderRegistry.list_providers()