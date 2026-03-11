"""Tests for CPI module."""
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from swiss_finance import CPI
from swiss_finance.core.exceptions import DataValidationError


MOCK_CPI_RESPONSE = {
    "timeseries": [{
        "header": [{"dim": "Overview", "dimItem": "National index"}],
        "metadata": {"scale": ""},
        "values": [
            {"date": "2020-01", "value": 101.2},
            {"date": "2020-02", "value": 101.5},
            {"date": "2021-01", "value": 102.0},
            {"date": "2021-02", "value": 102.3},
            {"date": "2022-01", "value": 104.1},
            {"date": "2022-02", "value": 104.5},
            {"date": "2023-01", "value": 106.2},
            {"date": "2023-02", "value": 106.5},
            {"date": "2024-01", "value": 107.0},
            {"date": "2024-02", "value": 107.3},
            {"date": "2025-01", "value": 108.0},
            {"date": "2025-02", "value": 108.2},
            {"date": "2026-01", "value": 99.9},
        ]
    }]
}


class TestCPIGetCurrent:
    def test_returns_float(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_CPI_RESPONSE
            )
            cpi = CPI.get_current()
            assert isinstance(cpi, float)

    def test_returns_last_value(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_CPI_RESPONSE
            )
            cpi = CPI.get_current()
            assert cpi == 99.9


class TestCPIGetHistorical:
    def test_returns_dataframe(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_CPI_RESPONSE
            )
            hist = CPI.get_historical()
            assert isinstance(hist, pd.DataFrame)

    def test_has_cpi_column(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_CPI_RESPONSE
            )
            hist = CPI.get_historical()
            assert "cpi" in hist.columns

    def test_index_is_datetime(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_CPI_RESPONSE
            )
            hist = CPI.get_historical()
            assert hist.index.dtype == "datetime64[ns]"

    def test_start_filter(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_CPI_RESPONSE
            )
            hist = CPI.get_historical(start="2022-01")
            assert hist.index[0] >= pd.Timestamp("2022-01-01")

    def test_end_before_start_raises(self):
        with pytest.raises(ValueError, match="must be before"):
            CPI.get_historical(start="2024-01", end="2020-01")


class TestCPIGetInflationYoY:
    def test_returns_dataframe(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_CPI_RESPONSE
            )
            inflation = CPI.get_inflation_yoy()
            assert isinstance(inflation, pd.DataFrame)

    def test_has_inflation_column(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value = MagicMock(
                status_code=200,
                json=lambda: MOCK_CPI_RESPONSE
            )
            inflation = CPI.get_inflation_yoy()
            assert "inflation_yoy" in inflation.columns

    def test_end_before_start_raises(self):
        with pytest.raises(ValueError, match="must be before"):
            CPI.get_inflation_yoy(start="2024-01", end="2020-01")
