"""Provider registry for managing data sources."""
from typing import Dict, Type
from .base import BaseFetcher
from .exceptions import ProviderNotFoundError


class ProviderRegistry:
    """Registry for managing data provider instances."""

    _providers: Dict[str, Type[BaseFetcher]] = {}

    @classmethod
    def register(cls, name: str, provider_class: Type[BaseFetcher]) -> None:
        """
        Register a new provider.

        Args:
            name: Provider identifier (e.g., 'snb_official')
            provider_class: Provider class (must inherit BaseFetcher)

        Raises:
            TypeError: If provider_class doesn't inherit BaseFetcher
        """
        if not issubclass(provider_class, BaseFetcher):
            raise TypeError(f"{provider_class} must inherit from BaseFetcher")

        cls._providers[name] = provider_class

    @classmethod
    def get(cls, name: str) -> Type[BaseFetcher]:
        """
        Get a provider class by name.

        Args:
            name: Provider identifier

        Returns:
            Provider class

        Raises:
            ProviderNotFoundError: If provider not registered
        """
        if name not in cls._providers:
            available = ', '.join(cls._providers.keys())
            raise ProviderNotFoundError(
                f"Provider '{name}' not found. Available: {available}"
            )

        return cls._providers[name]

    @classmethod
    def list_providers(cls) -> list:
        """List all registered providers."""
        return list(cls._providers.keys())