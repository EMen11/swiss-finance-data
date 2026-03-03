"""Custom exceptions for swiss-finance-data."""


class SwissFinanceError(Exception):
    """Base exception for all swiss-finance-data errors."""
    pass


class FetchError(SwissFinanceError):
    """Raised when data fetch fails."""
    pass


class SNBAPIError(FetchError):
    """Raised when SNB API call fails."""
    pass


class DataValidationError(SwissFinanceError):
    """Raised when data validation fails."""
    pass


class ProviderNotFoundError(SwissFinanceError):
    """Raised when requested provider doesn't exist."""
    pass