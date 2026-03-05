"""Tests for FX module."""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from swiss_finance import FX
from swiss_finance.core.exceptions import DataValidationError


MOCK_FX_RESPONSE = {
    "timeseries": [{
        "header": [{"dim": "Currency", "dimItem": "EUR 1"}],
        "metadata": {"unit": "Rates at 11 am. in CHF"},
        "values": [
            {"date": "2024-01", "value": 0.9320},
            {"date": "2024-02", "value": 0.9410},
            {"date": "2024-03", "value": 0.9550},
            {"date": "2024-04", "value": 0.9480},
            {"date": "2024-05", "value": 0.9390},
            {"date": "2024-06", "value": 0.9300},
        ]
    }]
}


class TestFXGetRate:
    def test_returns_float(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_FX_RESPONSE
            )
            rate = FX.get_rate("EUR")
            assert isinstance(rate, float)

    def test_returns_last_value(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_FX_RESPONSE
            )
            rate = FX.get_rate("EUR")
            assert rate == 0.9300

    def test_unsupported_currency_raises(self):
        with pytest.raises(ValueError, match="not supported"):
            FX.get_rate("XYZ")


class TestFXGetHistoricalRates:
    def test_returns_dataframe(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_FX_RESPONSE
            )
            rates = FX.get_historical_rates("EUR")
            assert isinstance(rates, pd.DataFrame)

    def test_dataframe_has_rate_column(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_FX_RESPONSE
            )
            rates = FX.get_historical_rates("EUR")
            assert "rate" in rates.columns

    def test_index_is_datetime(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_FX_RESPONSE
            )
            rates = FX.get_historical_rates("EUR")
            assert rates.index.dtype == "datetime64[ns]"

    def test_start_filter(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_FX_RESPONSE
            )
            rates = FX.get_historical_rates("EUR", start="2024-03")
            assert rates.index[0] >= pd.Timestamp("2024-03-01")

    def test_end_before_start_raises(self):
        with pytest.raises(ValueError, match="must be before"):
            FX.get_historical_rates("EUR", start="2024-06", end="2024-01")


class TestFXListCurrencies:
    def test_returns_list(self):
        currencies = FX.list_currencies()
        assert isinstance(currencies, list)

    def test_contains_major_currencies(self):
        currencies = FX.list_currencies()
        for c in ["EUR", "USD", "GBP"]:
            assert c in currencies