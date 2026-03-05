"""Tests for SARON module."""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from swiss_finance import SNB
from swiss_finance.core.exceptions import DataValidationError


MOCK_SARON_RESPONSE = {
    "timeseries": [{
        "header": [{"dim": "Overview", "dimItem": "SARON 1 day"}],
        "metadata": {"unit": "In percent"},
        "values": [
            {"date": "2024-01", "value": 1.720},
            {"date": "2024-02", "value": 1.718},
            {"date": "2024-03", "value": 1.500},
            {"date": "2024-04", "value": 1.498},
            {"date": "2024-05", "value": 1.250},
            {"date": "2024-06", "value": -0.076},
        ]
    }]
}


class TestSNBGetSaron:
    def test_returns_float(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_SARON_RESPONSE
            )
            saron = SNB.get_saron()
            assert isinstance(saron, float)

    def test_returns_last_value(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_SARON_RESPONSE
            )
            saron = SNB.get_saron()
            assert saron == -0.076


class TestSNBGetHistoricalSaron:
    def test_returns_dataframe(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_SARON_RESPONSE
            )
            rates = SNB.get_historical_saron()
            assert isinstance(rates, pd.DataFrame)

    def test_dataframe_has_rate_column(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_SARON_RESPONSE
            )
            rates = SNB.get_historical_saron()
            assert "rate" in rates.columns

    def test_index_is_datetime(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_SARON_RESPONSE
            )
            rates = SNB.get_historical_saron()
            assert rates.index.dtype == "datetime64[ns]"

    def test_start_filter(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_SARON_RESPONSE
            )
            rates = SNB.get_historical_saron(start="2024-03")
            assert rates.index[0] >= pd.Timestamp("2024-03-01")

    def test_end_before_start_raises(self):
        with pytest.raises(ValueError, match="must be before"):
            SNB.get_historical_saron(start="2024-06", end="2024-01")