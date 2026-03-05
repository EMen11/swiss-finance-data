"""Swiss National Bank (SNB) rates API."""
import pandas as pd
from ..core.providers import ProviderRegistry


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

        Raises:
            ProviderNotFoundError: If provider not found
            SNBAPIError: If data fetch fails

        Example:
            >>> from swiss_finance import SNB
            >>> rate = SNB.get_policy_rate()
            >>> print(f"SNB Rate: {rate}%")
            SNB Rate: 0.5%
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
            ProviderNotFoundError: If provider not found
            SNBAPIError: If data fetch fails
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
    def list_providers() -> list:
        """
        List available SNB data providers.

        Returns:
            List of provider names

        Example:
            >>> SNB.list_providers()
            ['snb_official']
        """
        return ProviderRegistry.list_providers()