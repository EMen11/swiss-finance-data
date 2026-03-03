"""swiss-finance-data: Python package for Swiss financial data."""

__version__ = "0.1.0"

from .rates.snb import SNB
from .core.exceptions import (
    SwissFinanceError,
    FetchError,
    SNBAPIError,
    DataValidationError,
    ProviderNotFoundError,
)
from .core.providers import ProviderRegistry
from .rates.providers.snb_official import SNBOfficialProvider

ProviderRegistry.register("snb_official", SNBOfficialProvider)

__all__ = [
    "SNB",
    "SwissFinanceError",
    "FetchError",
    "SNBAPIError",
    "DataValidationError",
    "ProviderNotFoundError",
]