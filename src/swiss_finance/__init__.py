"""Swiss Finance Data — Official Swiss financial data for Python."""

from .rates.snb import SNB
from .fx.chf import FX
from .macro.cpi import CPI
from .equities.smi import SMI
from .core.exceptions import (
    SwissFinanceError,
    FetchError,
    SNBAPIError,
    DataValidationError,
    ProviderNotFoundError,
)

__version__ = "0.4.0"
__all__ = [
    "SNB",
    "FX",
    "CPI",
    "SMI",
    "SwissFinanceError",
    "FetchError",
    "SNBAPIError",
    "DataValidationError",
    "ProviderNotFoundError",
]
