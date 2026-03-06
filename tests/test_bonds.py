"""Tests for Bonds module (Swiss Confederation bond yields)."""
import pytest
import requests
from unittest.mock import Mock, patch
import pandas as pd
from swiss_finance import Bonds
from swiss_finance.core.exceptions import SNBAPIError, DataValidationError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_BASE_DIM = (
    "Spot interest rates with different maturities for Confederation bond issues "
    "and euro-denominated bond issues - CHF Swiss Confederation bond issues"
)


def _make_ts(maturity_text: str, values: list) -> dict:
    """Build a mock SNB timeseries entry using the real dimItem format."""
    dim_item = f"{_BASE_DIM} - {maturity_text}"
    return {
        "header": [{"dim": "D0", "dimItem": dim_item}],
        "metadata": {"key": "rendoblid", "frequency": "P1M", "unit": "In percent"},
        "values": values,
    }


def _make_unrelated_ts(values: list) -> dict:
    """Non-Confederation series (should be ignored by the parser)."""
    return {
        "header": [{"dim": "D0", "dimItem": "EUR German government bond issues - 10 years"}],
        "metadata": {},
        "values": values,
    }


@pytest.fixture
def mock_bonds_single_response():
    """SNB response mimicking the real rendoblid cube for 10y only (+ unrelated series)."""
    return {
        "timeseries": [
            _make_ts("10 years", [
                {"date": "2024-01-31", "value": 0.75},
                {"date": "2024-02-29", "value": 0.80},
                {"date": "2024-03-31", "value": 0.85},
            ]),
            _make_unrelated_ts([{"date": "2024-03-31", "value": 2.5}]),
        ]
    }


@pytest.fixture
def mock_bonds_curve_response():
    """SNB response with four Confederation maturities + one unrelated series."""
    return {
        "timeseries": [
            _make_ts("2 years",  [{"date": "2024-03-31", "value": 0.30}]),
            _make_ts("5 years",  [{"date": "2024-03-31", "value": 0.55}]),
            _make_ts("10 years", [{"date": "2024-03-31", "value": 0.85}]),
            _make_ts("30 years", [{"date": "2024-03-31", "value": 1.10}]),
            _make_unrelated_ts([{"date": "2024-03-31", "value": 2.5}]),
        ]
    }


# ---------------------------------------------------------------------------
# Bonds.list_maturities()
# ---------------------------------------------------------------------------

class TestBondsListMaturities:
    def test_returns_list(self):
        maturities = Bonds.list_maturities()
        assert isinstance(maturities, list)

    def test_contains_standard_maturities(self):
        maturities = Bonds.list_maturities()
        for m in ["2y", "5y", "10y", "30y"]:
            assert m in maturities

    def test_all_strings(self):
        for m in Bonds.list_maturities():
            assert isinstance(m, str)


# ---------------------------------------------------------------------------
# Bonds.get_yield()
# ---------------------------------------------------------------------------

class TestBondsGetYield:
    def test_returns_float(self, mock_bonds_single_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_single_response),
                raise_for_status=Mock(),
            )
            result = Bonds.get_yield("10y")
            assert isinstance(result, float)

    def test_returns_last_value(self, mock_bonds_single_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_single_response),
                raise_for_status=Mock(),
            )
            result = Bonds.get_yield("10y")
            assert result == 0.85

    def test_raises_on_unknown_maturity(self):
        with pytest.raises(ValueError, match="Unknown maturity"):
            Bonds.get_yield("99y")

    def test_raises_on_http_error(self):
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.HTTPError("404")
            mock_response.status_code = 404
            mock_get.return_value = mock_response
            with pytest.raises(SNBAPIError):
                Bonds.get_yield("10y")

    def test_raises_on_network_error(self):
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.ConnectionError("Network error")
            with pytest.raises(Exception):
                Bonds.get_yield("10y")


# ---------------------------------------------------------------------------
# Bonds.get_yield_curve()
# ---------------------------------------------------------------------------

class TestBondsGetYieldCurve:
    def test_returns_dataframe(self, mock_bonds_curve_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_curve_response),
                raise_for_status=Mock(),
            )
            curve = Bonds.get_yield_curve()
            assert isinstance(curve, pd.DataFrame)

    def test_has_one_row(self, mock_bonds_curve_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_curve_response),
                raise_for_status=Mock(),
            )
            curve = Bonds.get_yield_curve()
            assert len(curve) == 1

    def test_has_maturity_columns(self, mock_bonds_curve_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_curve_response),
                raise_for_status=Mock(),
            )
            curve = Bonds.get_yield_curve()
            for col in ["2y", "5y", "10y", "30y"]:
                assert col in curve.columns

    def test_index_is_datetime(self, mock_bonds_curve_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_curve_response),
                raise_for_status=Mock(),
            )
            curve = Bonds.get_yield_curve()
            assert pd.api.types.is_datetime64_any_dtype(curve.index)


# ---------------------------------------------------------------------------
# Bonds.get_historical_yields()
# ---------------------------------------------------------------------------

class TestBondsGetHistoricalYields:
    def test_returns_dataframe(self, mock_bonds_single_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_single_response),
                raise_for_status=Mock(),
            )
            hist = Bonds.get_historical_yields(maturity="10y")
            assert isinstance(hist, pd.DataFrame)

    def test_has_correct_column(self, mock_bonds_single_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_single_response),
                raise_for_status=Mock(),
            )
            hist = Bonds.get_historical_yields(maturity="10y")
            assert "10y" in hist.columns

    def test_index_is_datetime(self, mock_bonds_single_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_single_response),
                raise_for_status=Mock(),
            )
            hist = Bonds.get_historical_yields(maturity="10y")
            assert pd.api.types.is_datetime64_any_dtype(hist.index)
            assert hist.index.name == "date"

    def test_sorted_by_date(self, mock_bonds_single_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_single_response),
                raise_for_status=Mock(),
            )
            hist = Bonds.get_historical_yields(maturity="10y")
            assert hist.index.is_monotonic_increasing

    def test_correct_number_of_rows(self, mock_bonds_single_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_single_response),
                raise_for_status=Mock(),
            )
            hist = Bonds.get_historical_yields(maturity="10y")
            assert len(hist) == 3

    def test_all_maturities_when_no_maturity_specified(self, mock_bonds_curve_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_bonds_curve_response),
                raise_for_status=Mock(),
            )
            hist = Bonds.get_historical_yields()
            assert len(hist.columns) == 4

    def test_raises_on_invalid_date_range(self):
        with pytest.raises(ValueError, match="must be before"):
            Bonds.get_historical_yields(start="2024-12-01", end="2024-01-01")

    def test_raises_on_unknown_maturity(self):
        with pytest.raises(ValueError, match="Unknown maturity"):
            Bonds.get_historical_yields(maturity="99y")
