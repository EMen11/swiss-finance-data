"""Tests for SMI module."""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from swiss_finance import SMI
from swiss_finance.core.exceptions import FetchError


class TestSMIGetConstituents:
    def test_returns_dict(self):
        result = SMI.get_constituents()
        assert isinstance(result, dict)

    def test_has_20_constituents(self):
        result = SMI.get_constituents()
        assert len(result) == 20

    def test_contains_key_tickers(self):
        result = SMI.get_constituents()
        assert "NESN.SW" in result
        assert "ROG.SW" in result
        assert "NOVN.SW" in result

    def test_values_are_strings(self):
        result = SMI.get_constituents()
        for name in result.values():
            assert isinstance(name, str)


MOCK_HISTORY = pd.DataFrame(
    {"Close": [80.0, 81.0, 80.5]},
    index=pd.date_range("2026-03-03", periods=3)
)

MOCK_MULTI_HISTORY = pd.DataFrame(
    {
        ("Close", "NESN.SW"): [80.0, 81.0, 80.5],
        ("Close", "ROG.SW"): [350.0, 352.0, 351.0],
    },
    index=pd.date_range("2026-03-03", periods=3)
)
MOCK_MULTI_HISTORY.columns = pd.MultiIndex.from_tuples(MOCK_MULTI_HISTORY.columns)


class TestSMIGetPrices:
    def test_returns_dataframe(self):
        with patch("yfinance.Ticker") as mock_ticker:
            mock_ticker.return_value.history.return_value = MOCK_HISTORY
            prices = SMI.get_prices()
            assert isinstance(prices, pd.DataFrame)

    def test_has_price_column(self):
        with patch("yfinance.Ticker") as mock_ticker:
            mock_ticker.return_value.history.return_value = MOCK_HISTORY
            prices = SMI.get_prices()
            assert "price" in prices.columns

    def test_has_name_column(self):
        with patch("yfinance.Ticker") as mock_ticker:
            mock_ticker.return_value.history.return_value = MOCK_HISTORY
            prices = SMI.get_prices()
            assert "name" in prices.columns


class TestSMIGetHistoricalPrices:
    def test_invalid_ticker_raises(self):
        with pytest.raises(ValueError, match="Unknown tickers"):
            SMI.get_historical_prices(tickers=["FAKE.SW"])

    def test_end_before_start_raises(self):
        with pytest.raises(ValueError, match="must be before"):
            SMI.get_historical_prices(start="2025-01-01", end="2024-01-01")

    def test_returns_dataframe(self):
        with patch("yfinance.download") as mock_dl:
            mock_dl.return_value = MOCK_MULTI_HISTORY
            result = SMI.get_historical_prices(
                tickers=["NESN.SW", "ROG.SW"], period="1mo"
            )
            assert isinstance(result, pd.DataFrame)


class TestSMIGetReturns:
    def test_returns_dataframe(self):
        with patch("yfinance.download") as mock_dl:
            mock_dl.return_value = MOCK_MULTI_HISTORY
            result = SMI.get_returns(
                tickers=["NESN.SW", "ROG.SW"], period="1mo"
            )
            assert isinstance(result, pd.DataFrame)

    def test_returns_one_row_less_than_prices(self):
        with patch("yfinance.download") as mock_dl:
            mock_dl.return_value = MOCK_MULTI_HISTORY
            prices = SMI.get_historical_prices(
                tickers=["NESN.SW", "ROG.SW"], period="1mo"
            )
            returns = SMI.get_returns(
                tickers=["NESN.SW", "ROG.SW"], period="1mo"
            )
            assert len(returns) == len(prices) - 1
