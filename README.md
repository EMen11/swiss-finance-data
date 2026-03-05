# swiss-finance-data

> Python package for Swiss financial data — starting with SNB (Swiss National Bank)

[![PyPI version](https://img.shields.io/pypi/v/swiss-finance-data.svg)](https://pypi.org/project/swiss-finance-data/)
[![Tests](https://github.com/EMen11/swiss-finance-data/actions/workflows/test.yml/badge.svg)](https://github.com/EMen11/swiss-finance-data/actions)
[![Coverage](https://img.shields.io/codecov/c/github/EMen11/swiss-finance-data)](https://codecov.io/gh/EMen11/swiss-finance-data)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/swiss-finance-data.svg)](https://pypi.org/project/swiss-finance-data/)
[![Downloads](https://static.pepy.tech/badge/swiss-finance-data)](https://pepy.tech/project/swiss-finance-data) 

---

## Why swiss-finance-data?

Accessing Swiss financial data in Python is fragmented. Existing tools focus on US/global markets and provide limited support for Swiss-specific datasets.

swiss-finance-data aims to provide:
- A unified, clean API for Swiss financial data
- Official government data sources — no scraping
- Extensible provider architecture
- Long-term maintainability

---
## Scope

swiss-finance-data focuses on:

- Official and legally reusable data sources
- Clean abstraction over data providers
- Stability and long-term maintainability
- Swiss-specific financial datasets

It does not aim to replace global data providers such as yfinance, but to complement them for Swiss markets.

---

## Features

## Features

**v0.1.1 — Available now:**
-  **SNB Policy Rate** — Current and historical Swiss National Bank policy rates
-  **Provider Architecture** — Extensible system for multiple data sources
-  **Tested & documented** — 89% unit test coverage
-  **Reliable** — Official Swiss government data sources, no scraping
-  **Improved error handling** — Clear messages for invalid date ranges and future dates

**Coming in future versions:**
- SMI equities (v0.2.0)
- Caching layer (v0.2.0)
- Swiss government bonds (v0.3.0)
- Real estate indices SWIIT (v0.4.0)

---

## Installation

```bash
pip install swiss-finance-data
```

**Requirements:** Python 3.10+
> Requires internet access — data is fetched live from the official SNB API.

---

## Quick Start

### Get current SNB policy rate

```python
from swiss_finance import SNB

rate = SNB.get_policy_rate()
print(f"SNB Policy Rate: {rate}%")
# Output: SNB Policy Rate: 0.0%
```

### Get historical rates

```python
from swiss_finance import SNB

rates = SNB.get_historical_rates(start='2020-01')
print(rates.tail())
#                 rate
# date
# 2025-09-01      0.0
# 2025-10-01      0.0
# 2025-11-01      0.0
# 2025-12-01      0.0
# 2026-01-01      0.0
```

### Error handling

```python
from swiss_finance import SNB, SNBAPIError

try:
    rate = SNB.get_policy_rate()
except SNBAPIError as e:
    print(f"Failed to fetch data: {e}")
```

---

## API Documentation

### `SNB.get_policy_rate(provider='snb_official')`

Get the current SNB policy rate.

**Parameters:**
- `provider` *(str, optional)*: Data provider to use. Default: `'snb_official'`

**Returns:** `float` — Current policy rate (percentage)

**Raises:**
- `SNBAPIError` — If API call fails
- `ProviderNotFoundError` — If provider doesn't exist

**Example:**
```python
rate = SNB.get_policy_rate()
```

---

### `SNB.get_historical_rates(start=None, end=None, provider='snb_official')`

Get historical SNB policy rates.

**Parameters:**
- `start` *(str, optional)*: Start date `YYYY-MM`
- `end` *(str, optional)*: End date `YYYY-MM`
- `provider` *(str, optional)*: Data provider to use. Default: `'snb_official'`

**Returns:** `pandas.DataFrame` — Date index + `rate` column

**Raises:**
- `SNBAPIError` — If API call fails

**Example:**
```python
# Full history
rates = SNB.get_historical_rates()

# Specific range
rates = SNB.get_historical_rates(start='2020-01', end='2024-12')
```

---

### `SNB.list_providers()`

List available data providers.

**Returns:** `list`

**Example:**
```python
SNB.list_providers()
# ['snb_official']
```

---

## Data Sources

All data sources are documented in [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md).

| Source | Data | License |
|--------|------|---------|
| [Swiss National Bank](https://data.snb.ch/) | Policy rates (current + historical) | [SNB Open Data terms](https://www.snb.ch/en/srv/disclaimer_liability) |

---

## Development

### Setup

```bash
git clone https://github.com/EMen11/swiss-finance-data.git
cd swiss-finance-data
pip install -e .[dev]
```

### Run tests

```bash
pytest --cov=swiss_finance tests/
```

---

## API Stability

- **v0.x** — API may evolve based on feedback
- **v1.0+** — Stable public API with backward compatibility guaranteed
- Versioning follows [Semantic Versioning (SemVer)](https://semver.org/).

---

## Roadmap

- [x] v0.1.0 — SNB policy rates
- [x] v0.1.1 — Improved error handling and date validation
- [ ] v0.2.0 — SARON + FX rates CHF + SMI equities
- [ ] v0.3.0 — Swiss government bonds
- [ ] v0.4.0 — Real estate indices (SWIIT)
- [ ] v1.0.0 — Stable API, full documentation

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Elie Menassa**
- GitHub: [@EMen11](https://github.com/EMen11)
- LinkedIn: [Elie Menassa](https://linkedin.com/in/elie-menassa)
- Email: menassa.elie.dev@gmail.com