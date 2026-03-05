"""Public API for CHF exchange rates."""
import pandas as pd
from ..core.providers import ProviderRegistry
from .providers.snb_fx import SNBFXProvider

# Auto-register provider
ProviderRegistry.register("snb_fx", SNBFXProvider)


class FX:
    """Public API for CHF foreign exchange rates."""

    DEFAULT_PROVIDER = "snb_fx"

    @staticmethod
    def get_rate(currency: str, provider: str = None) -> float:
        """
        Get current CHF exchange rate.

        Args:
            currency: Currency code (EUR, USD, GBP, JPY, CAD, AUD, SEK, NOK, DKK)
            provider: Data provider (default: 'snb_fx')

        Returns:
            Current exchange rate (units of currency per 1 CHF)

        Raises:
            ValueError: If currency not supported
            FetchError: If data fetch fails

        Example:
            >>> from swiss_finance import FX
            >>> eur_chf = FX.get_rate("EUR")
            >>> print(f"EUR/CHF: {eur_chf}")
        """
        provider = provider or FX.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_current_rate(currency=currency)

    @staticmethod
    def get_historical_rates(
        currency: str,
        start: str = None,
        end: str = None,
        provider: str = None
    ) -> pd.DataFrame:
        """
        Get historical CHF exchange rates.

        Args:
            currency: Currency code (EUR, USD, GBP, JPY, CAD, AUD, SEK, NOK, DKK)
            start: Start date (YYYY-MM), optional
            end: End date (YYYY-MM), optional
            provider: Data provider (default: 'snb_fx')

        Returns:
            DataFrame with date index and 'rate' column

        Raises:
            ValueError: If currency not supported or start > end
            FetchError: If data fetch fails

        Example:
            >>> from swiss_finance import FX
            >>> rates = FX.get_historical_rates("EUR", start="2020-01")
        """
        if start and end and start > end:
            raise ValueError(
                f"start date '{start}' must be before end date '{end}'"
            )

        provider = provider or FX.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_historical_rates(
            currency=currency,
            start_date=start,
            end_date=end
        )

    @staticmethod
    def list_currencies(provider: str = None) -> list:
        """
        List supported currencies.

        Returns:
            List of supported currency codes

        Example:
            >>> FX.list_currencies()
            ['EUR', 'USD', 'GBP', 'JPY', 'CAD', 'AUD', 'SEK', 'NOK', 'DKK']
        """
        provider = provider or FX.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.list_currencies()