"""Swiss Finance Data — Official Swiss financial data for Python."""

from .rates.snb import SNB
from .fx.chf import FX
from .macro.cpi import CPI
from .equities.smi import SMI
from .bonds.confederation import Bonds
from .core.exceptions import (
    SwissFinanceError,
    FetchError,
    SNBAPIError,
    DataValidationError,
    ProviderNotFoundError,
)

__version__ = "0.5.0"
__all__ = [
    "SNB",
    "FX",
    "CPI",
    "SMI",
    "Bonds",
    "SwissFinanceError",
    "FetchError",
    "SNBAPIError",
    "DataValidationError",
    "ProviderNotFoundError",
]
