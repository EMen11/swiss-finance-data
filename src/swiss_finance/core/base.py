"""Base classes for data fetchers."""
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseFetcher(ABC):
    """Abstract base class for all data fetchers."""

    @abstractmethod
    def fetch(self, **kwargs) -> Dict[str, Any]:
        """
        Fetch data from source.

        Returns:
            Dict containing fetched data

        Raises:
            FetchError: If fetch fails
        """
        pass

    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> bool:
        """
        Validate fetched data structure.

        Args:
            data: Data to validate

        Returns:
            True if valid, raises otherwise
        """
        pass