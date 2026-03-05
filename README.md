# swiss-finance-data

> Python package for Swiss financial data — official sources, clean API

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

**v0.2.0 — Available now:**
-  **SNB Policy Rate** — Current and historical Swiss National Bank policy rates
-  **SARON** — Swiss Average Rate Overnight, the CHF risk-free reference rate (replaces LIBOR)
-  **CHF FX Rates** — EUR, USD, GBP, JPY, CAD, AUD, SEK, NOK, DKK vs CHF
-  **Provider Architecture** — Extensible system for multiple data sources
-  **Tested & documented** — 86% unit test coverage
-  **Reliable** — Official Swiss government data sources, no scraping
-  **Robust error handling** — Clear messages for invalid date ranges and future dates

---

## Installation

```bash
pip install swiss-finance-data
```

**Requirements:** Python 3.10+

> Requires internet access — data is fetched live from the official SNB API.

---

## Quick Start

```python
from swiss_finance import SNB, FX

# SNB Policy Rate
rate = SNB.get_policy_rate()
print(f"SNB Policy Rate: {rate}%")

# SARON — CHF risk-free rate (use in Sharpe ratio calculations)
saron = SNB.get_saron()
rf = saron / 100
print(f"SARON: {saron}%")

# CHF Exchange Rates
eur_chf = FX.get_rate("EUR")
usd_chf = FX.get_rate("USD")
print(f"EUR/CHF: {eur_chf}")
print(f"USD/CHF: {usd_chf}")

# Historical data
rates = SNB.get_historical_rates(start="2022-01")
saron_hist = SNB.get_historical_saron(start="2022-01")
fx_hist = FX.get_historical_rates("EUR", start="2022-01")
print(fx_hist.tail())
#                  rate
# date
# 2025-12-01  0.93313
# 2026-01-01  0.92732
# 2026-02-01  0.91406
```

---

## API Documentation

### SNB Policy Rate

```python
# Current rate
SNB.get_policy_rate(provider='snb_official') -> float

# Historical rates
SNB.get_historical_rates(
    start='YYYY-MM',  # optional
    end='YYYY-MM',    # optional
    provider='snb_official'
) -> pd.DataFrame

# List providers
SNB.list_providers() -> list
```

### SARON

```python
# Current SARON rate
SNB.get_saron() -> float

# Historical SARON rates
SNB.get_historical_saron(
    start='YYYY-MM',  # optional
    end='YYYY-MM'     # optional
) -> pd.DataFrame
```

### FX — CHF Exchange Rates

Supported currencies: `EUR`, `USD`, `GBP`, `JPY`, `CAD`, `AUD`, `SEK`, `NOK`, `DKK`

```python
# Current rate
FX.get_rate(currency='EUR') -> float

# Historical rates
FX.get_historical_rates(
    currency='EUR',
    start='YYYY-MM',  # optional
    end='YYYY-MM'     # optional
) -> pd.DataFrame

# List supported currencies
FX.list_currencies() -> list
```

### Error handling

```python
from swiss_finance import SNB, FX, SNBAPIError, DataValidationError

try:
    rate = SNB.get_policy_rate()
except SNBAPIError as e:
    print(f"Failed to fetch data: {e}")

try:
    rates = SNB.get_historical_rates(start='2030-01')
except DataValidationError as e:
    print(f"Invalid date range: {e}")
```

---

## Data Sources

All data sources are documented in [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md).

| Source | Dataset | License |
|--------|---------|---------|
| [Swiss National Bank](https://data.snb.ch/) | SNB Policy Rate | [SNB Open Data terms](https://www.snb.ch/en/srv/disclaimer_liability) |
| [Swiss National Bank](https://data.snb.ch/) | SARON (monthly avg, 2009+) | [SNB Open Data terms](https://www.snb.ch/en/srv/disclaimer_liability) |
| [Swiss National Bank](https://data.snb.ch/) | CHF FX Rates (monthly avg, 1999+) | [SNB Open Data terms](https://www.snb.ch/en/srv/disclaimer_liability) |

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
- [x] v0.2.0 — SARON + CHF FX rates
- [ ] v0.3.0 — SMI equities + Swiss government bonds
- [ ] v0.4.0 — Real estate indices (SWIIT)
- [ ] v1.0.0 — Stable API, full documentation

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Elie Menassa**
- GitHub: [@EMen11](https://github.com/EMen11)
- Email: menassa.elie.dev@gmail.com
