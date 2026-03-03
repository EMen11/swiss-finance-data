"""Tests for SNB module."""
import pytest
import requests
from unittest.mock import Mock, patch
import pandas as pd
from swiss_finance import SNB
from swiss_finance.core.exceptions import SNBAPIError, ProviderNotFoundError


class TestSNBGetPolicyRate:
    """Tests for SNB.get_policy_rate()"""

    def test_returns_float(self, mock_snb_response):
        """get_policy_rate() doit retourner un float."""
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_snb_response),
                raise_for_status=Mock()
            )
            rate = SNB.get_policy_rate()
            assert isinstance(rate, float)

    def test_returns_last_value(self, mock_snb_response):
        """get_policy_rate() doit retourner la dernière valeur."""
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_snb_response),
                raise_for_status=Mock()
            )
            rate = SNB.get_policy_rate()
            assert rate == 0.0

    def test_raises_on_timeout(self):
        """get_policy_rate() doit lever SNBAPIError si timeout."""
        with patch("requests.get") as mock_get:
            mock_get.side_effect = requests.Timeout("Timeout")
            with pytest.raises(SNBAPIError) as exc_info:
                SNB.get_policy_rate()
            assert "failed after" in str(exc_info.value).lower()

    def test_raises_on_http_error(self):
        """get_policy_rate() doit lever SNBAPIError si erreur HTTP."""
        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = requests.HTTPError("404")
            mock_get.return_value = mock_response
            with pytest.raises(SNBAPIError) as exc_info:
                SNB.get_policy_rate()
            assert "HTTP error" in str(exc_info.value)

    def test_raises_on_invalid_provider(self):
        """get_policy_rate() doit lever ProviderNotFoundError si provider inconnu."""
        with pytest.raises(ProviderNotFoundError) as exc_info:
            SNB.get_policy_rate(provider="nonexistent")
        assert "nonexistent" in str(exc_info.value)
        assert "Available" in str(exc_info.value)


class TestSNBGetHistoricalRates:
    """Tests for SNB.get_historical_rates()"""

    def test_returns_dataframe(self, mock_snb_response):
        """get_historical_rates() doit retourner un DataFrame."""
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_snb_response),
                raise_for_status=Mock()
            )
            rates = SNB.get_historical_rates()
            assert isinstance(rates, pd.DataFrame)

    def test_has_rate_column(self, mock_snb_response):
        """get_historical_rates() doit avoir une colonne 'rate'."""
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_snb_response),
                raise_for_status=Mock()
            )
            rates = SNB.get_historical_rates()
            assert "rate" in rates.columns

    def test_index_is_date(self, mock_snb_response):
        """get_historical_rates() doit avoir un index de type datetime."""
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_snb_response),
                raise_for_status=Mock()
            )
            rates = SNB.get_historical_rates()
            assert rates.index.name == "date"
            assert pd.api.types.is_datetime64_any_dtype(rates.index)

    def test_correct_number_of_rows(self, mock_snb_response):
        """get_historical_rates() doit retourner le bon nombre de lignes."""
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_snb_response),
                raise_for_status=Mock()
            )
            rates = SNB.get_historical_rates()
            assert len(rates) == 6

    def test_sorted_by_date(self, mock_snb_response):
        """get_historical_rates() doit être trié par date."""
        with patch("requests.get") as mock_get:
            mock_get.return_value = Mock(
                json=Mock(return_value=mock_snb_response),
                raise_for_status=Mock()
            )
            rates = SNB.get_historical_rates()
            assert rates.index.is_monotonic_increasing


class TestSNBListProviders:
    """Tests for SNB.list_providers()"""

    def test_returns_list(self):
        """list_providers() doit retourner une liste."""
        providers = SNB.list_providers()
        assert isinstance(providers, list)

    def test_contains_snb_official(self):
        """list_providers() doit contenir 'snb_official'."""
        providers = SNB.list_providers()
        assert "snb_official" in providers