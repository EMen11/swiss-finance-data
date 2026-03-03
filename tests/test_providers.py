"""Tests for provider registry."""
import pytest
from swiss_finance.core.providers import ProviderRegistry
from swiss_finance.core.base import BaseFetcher
from swiss_finance.core.exceptions import ProviderNotFoundError


class DummyProvider(BaseFetcher):
    """Dummy provider for testing."""
    def fetch(self, **kwargs):
        return {"test": "data"}

    def validate(self, data):
        return True


class TestProviderRegistry:
    """Tests for ProviderRegistry."""

    def test_register_and_get(self):
        """register() puis get() doit retourner le bon provider."""
        ProviderRegistry.register("test_dummy", DummyProvider)
        provider = ProviderRegistry.get("test_dummy")
        assert provider == DummyProvider

    def test_get_nonexistent_raises(self):
        """get() doit lever ProviderNotFoundError si inconnu."""
        with pytest.raises(ProviderNotFoundError) as exc_info:
            ProviderRegistry.get("does_not_exist")
        assert "does_not_exist" in str(exc_info.value)
        assert "Available" in str(exc_info.value)

    def test_register_non_fetcher_raises(self):
        """register() doit lever TypeError si la classe n'hérite pas BaseFetcher."""
        class NotAFetcher:
            pass

        with pytest.raises(TypeError):
            ProviderRegistry.register("bad", NotAFetcher)

    def test_list_providers_returns_list(self):
        """list_providers() doit retourner une liste."""
        providers = ProviderRegistry.list_providers()
        assert isinstance(providers, list)

    def test_snb_official_registered(self):
        """snb_official doit être enregistré au démarrage."""
        providers = ProviderRegistry.list_providers()
        assert "snb_official" in providers