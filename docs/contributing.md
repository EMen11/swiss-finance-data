# Contributing to swiss-finance-data

Thank you for your interest in contributing.

---

## Development environment

```bash
git clone https://github.com/EMen11/swiss-finance-data.git
cd swiss-finance-data
pip install -e .[dev]
```

Dependencies: `pandas`, `requests`, `yfinance`. Dev extras: `pytest`, `pytest-cov`.

---

## Running tests

```bash
# All tests
pytest tests/

# With coverage report
pytest --cov=swiss_finance tests/

# Single module
pytest tests/test_bonds.py -v
```

All tests must pass before submitting a pull request.

---

## Project structure

```
src/swiss_finance/
    __init__.py             # Public exports: SNB, FX, CPI, SMI, Bonds
    core/
        base.py             # BaseFetcher ABC
        exceptions.py       # SwissFinanceError, SNBAPIError, FetchError, ...
        providers.py        # ProviderRegistry
        validators.py       # validate_dataframe, validate_rate
    rates/                  # SNB policy rate + SARON
    fx/                     # CHF exchange rates
    macro/                  # Swiss CPI
    equities/               # SMI constituents
    bonds/                  # Swiss Confederation bond yields
tests/
docs/
    DATA_SOURCES.md         # Verified API sources (read before adding a provider)
    CONTRIBUTING.md         # This file
```

---

## Adding a new data provider

### 1. Verify the source first

Before writing any code, document the source in `docs/DATA_SOURCES.md`:
- Confirm the endpoint works manually (curl or browser)
- Document the JSON structure, field names, date format, frequency
- Confirm the license allows redistribution

### 2. Create the provider class

```python
# src/swiss_finance/<module>/providers/<name>.py
from ...core.base import BaseFetcher
from ...core.exceptions import SNBAPIError, FetchError

class MyProvider(BaseFetcher):
    BASE_URL = "https://..."
    TIMEOUT = 30
    MAX_RETRIES = 3

    def fetch(self) -> dict:
        """Fetch raw data with retry logic."""
        ...

    def validate(self, data: dict) -> bool:
        """Return True if response structure is valid."""
        ...
```

Follow the existing providers as reference: `src/swiss_finance/bonds/providers/snb_bonds.py`.

### 3. Create the public API class

```python
# src/swiss_finance/<module>/<name>.py
from ..core.providers import ProviderRegistry
from .providers.<name> import MyProvider

ProviderRegistry.register("my_provider", MyProvider)

class MyClass:
    DEFAULT_PROVIDER = "my_provider"

    @staticmethod
    def get_something(provider: str = None):
        """
        One-line summary.

        Args:
            provider: Data provider (default: 'my_provider')

        Returns:
            Description of return value

        Raises:
            SNBAPIError: If API call fails
            ValueError: If input is invalid

        Example:
            >>> from swiss_finance import MyClass
            >>> MyClass.get_something()
        """
        provider = provider or MyClass.DEFAULT_PROVIDER
        fetcher = ProviderRegistry.get(provider)()
        return fetcher.get_something()
```

### 4. Export from `__init__.py`

```python
# src/swiss_finance/__init__.py
from .mymodule.myclass import MyClass
__all__ = [..., "MyClass"]
```

### 5. Write tests

Create `tests/test_<module>.py` with mocked HTTP responses.
Follow `tests/test_bonds.py` as reference:
- Mock fixtures that replicate the real API response structure exactly
- Test return types, column names, date index dtype
- Test error cases (HTTP errors, invalid inputs)

---

## Code style

- **Python 3.10+** — use `str | None` union types where appropriate
- **PEP 8** — 4-space indentation, max 100 chars per line
- **Type hints** on all public method signatures
- **Docstrings** on every public method: Args, Returns, Raises, Example sections
- **No scraping** — only official APIs with stable, documented endpoints
- **No side effects** at import time — module-level provider registration is acceptable

---

## Commit style

```
feat: add <feature> (vX.Y.Z)
fix: <description>
docs: <description>
test: <description>
refactor: <description>
```

---

## Pull request checklist

- [ ] `docs/DATA_SOURCES.md` updated with new source
- [ ] Provider class extends `BaseFetcher` and implements `fetch` + `validate`
- [ ] Public API class has complete docstrings (Args, Returns, Raises, Example)
- [ ] Tests cover happy path + error cases
- [ ] `pytest --cov=swiss_finance tests/` passes with no regressions
- [ ] `CHANGELOG.md` entry added
