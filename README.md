# swiss-finance-data

> Python package for Swiss financial data — official sources, clean API

[![PyPI version](https://img.shields.io/pypi/v/swiss-finance-data.svg)](https://pypi.org/project/swiss-finance-data/)
[![Tests](https://github.com/EMen11/swiss-finance-data/actions/workflows/test.yml/badge.svg)](https://github.com/EMen11/swiss-finance-data/actions)
[![Coverage](https://img.shields.io/codecov/c/github/EMen11/swiss-finance-data)](https://codecov.io/gh/EMen11/swiss-finance-data)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/swiss-finance-data.svg)](https://pypi.org/project/swiss-finance-data/)
[![Downloads](https://static.pepy.tech/badge/swiss-finance-data)](https://pepy.tech/project/swiss-finance-data)
[![Documentation](https://img.shields.io/badge/docs-online-blue.svg)](https://emen11.github.io/swiss-finance-data)

---

## Why swiss-finance-data?

Accessing Swiss financial data in Python is fragmented. Existing tools focus on US/global markets and provide limited support for Swiss-specific datasets.

swiss-finance-data aims to provide:
- A unified, clean API for Swiss financial data
- Official government data sources — no scraping
- Extensible provider architecture
- Long-term maintainability

**[Full documentation →](https://emen11.github.io/swiss-finance-data)**

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

**v1.0.0 — Stable public API:**
-  **SNB Policy Rate** — Current and historical Swiss National Bank policy rates
-  **SARON** — Monthly average and daily fixing, the CHF risk-free reference rate (replaces LIBOR)
-  **CHF FX Rates** — EUR, USD, GBP, JPY, CAD, AUD, SEK, NOK, DKK vs CHF
- **Swiss CPI** — Consumer Price Index and YoY inflation rate (data since 1921)
- **SMI Equities** — All 20 Swiss Market Index constituents, prices and returns
- **Swiss Confederation Bonds** — Yield curve and historical yields, 13 maturities (1y–30y)
-  **Provider Architecture** — Extensible system for multiple data sources
-  **Reliable** — Official Swiss government data sources, no scraping
-  **Robust error handling** — Clear messages for invalid date ranges and future dates

---

## Installation

```bash


```

**Requirements:** Python 3.10+

> Requires internet access — data is fetched live from official sources.

---

## Quick Start

```python
from swiss_finance import SNB, FX, CPI, SMI, Bonds

# SNB Policy Rate
rate = SNB.get_policy_rate()
print(f"SNB Policy Rate: {rate}%")

# SARON — CHF risk-free rate (monthly and daily)
saron = SNB.get_saron()
rf_daily = SNB.get_saron_daily() / 100 / 252  # daily risk-free rate
print(f"SARON: {saron}%")

# CHF Exchange Rates
eur_chf = FX.get_rate("EUR")
print(f"EUR/CHF: {eur_chf}")

# Swiss CPI and inflation
inflation = CPI.get_inflation_yoy()
print(f"Inflation YoY: {inflation.iloc[-1, 0]:.2f}%")

# SMI equities
prices = SMI.get_prices()           # current prices for all 20 constituents
returns = SMI.get_returns(period="1y")  # daily returns
hist = SMI.get_historical_prices(
    tickers=["NESN.SW", "ROG.SW", "NOVN.SW"],
    start="2023-01-01"
)

# Swiss Confederation bond yields
yield_10y = Bonds.get_yield("10y")
print(f"10y Confederation bond: {yield_10y:.2f}%")
curve = Bonds.get_yield_curve()                           # full yield curve (latest)
hist_bonds = Bonds.get_historical_yields(maturity="10y", start="2020-01-01")
```

---

## API Documentation

### SNB Policy Rate

```python
SNB.get_policy_rate(provider='snb_official') -> float
SNB.get_historical_rates(start='YYYY-MM', end='YYYY-MM') -> pd.DataFrame
SNB.list_providers() -> list
```

### SARON

```python
SNB.get_saron() -> float                                        # monthly average
SNB.get_historical_saron(start='YYYY-MM', end='YYYY-MM') -> pd.DataFrame
SNB.get_saron_daily() -> float                                  # latest daily fixing
SNB.get_historical_saron_daily(start='YYYY-MM-DD', end='YYYY-MM-DD') -> pd.DataFrame
```

### FX — CHF Exchange Rates

Supported currencies: `EUR`, `USD`, `GBP`, `JPY`, `CAD`, `AUD`, `SEK`, `NOK`, `DKK`

```python
FX.get_rate(currency='EUR') -> float
FX.get_historical_rates(currency='EUR', start='YYYY-MM', end='YYYY-MM') -> pd.DataFrame
FX.list_currencies() -> list
```

### CPI — Swiss Consumer Price Index

```python
CPI.get_current() -> float                                      # latest index value
CPI.get_historical(start='YYYY-MM', end='YYYY-MM') -> pd.DataFrame
CPI.get_inflation_yoy(start='YYYY-MM', end='YYYY-MM') -> pd.DataFrame
```

### SMI — Swiss Market Index Equities

```python
SMI.get_constituents() -> dict                                  # {ticker: company_name}
SMI.get_prices() -> pd.DataFrame                                # current prices, all 20
SMI.get_historical_prices(
    tickers=['NESN.SW', 'ROG.SW'],  # optional, default: all 20
    period='1y',                     # ignored if start/end provided
    start='YYYY-MM-DD',
    end='YYYY-MM-DD'
) -> pd.DataFrame
SMI.get_returns(tickers=None, period='1y', start=None, end=None) -> pd.DataFrame
```

**SMI constituents:** NESN, ROG, NOVN, UBSG, ZURN, ABBN, SREN, GIVN, LONN, SIKA, GEBN, SLHN, SCMN, HOLN, PGHN, CFR, ALC, SDZ, STMN, VACN

### Bonds — Swiss Confederation Bond Yields

```python
Bonds.list_maturities() -> list                             # ['1y', '2y', ..., '30y']
Bonds.get_yield(maturity='10y') -> float                    # latest yield in %
Bonds.get_yield_curve() -> pd.DataFrame                     # one row, all maturities
Bonds.get_historical_yields(
    maturity='10y',          # optional, returns all maturities if omitted
    start='YYYY-MM-DD',
    end='YYYY-MM-DD'
) -> pd.DataFrame
```

**Available maturities:** 1y, 2y, 3y, 4y, 5y, 6y, 7y, 8y, 9y, 10y, 15y, 20y, 30y

### Error handling

```python
from swiss_finance import SNB, FX, CPI, SMI, SNBAPIError, DataValidationError

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

| Source | Dataset | License |
|--------|---------|---------|
| [Swiss National Bank](https://data.snb.ch/) | SNB Policy Rate | [SNB Open Data terms](https://www.snb.ch/en/srv/disclaimer_liability) |
| [Swiss National Bank](https://data.snb.ch/) | SARON monthly avg (2009+) | [SNB Open Data terms](https://www.snb.ch/en/srv/disclaimer_liability) |
| [Swiss National Bank](https://data.snb.ch/) | SARON daily fixing (2009+) | [SNB Open Data terms](https://www.snb.ch/en/srv/disclaimer_liability) |
| [Swiss National Bank](https://data.snb.ch/) | CHF FX Rates (monthly, 1999+) | [SNB Open Data terms](https://www.snb.ch/en/srv/disclaimer_liability) |
| [Swiss National Bank](https://data.snb.ch/) | Swiss CPI (monthly, 1921+) | [SNB Open Data terms](https://www.snb.ch/en/srv/disclaimer_liability) |
| [Swiss National Bank](https://data.snb.ch/) | Confederation bond yields (monthly, 13 maturities) | [SNB Open Data terms](https://www.snb.ch/en/srv/disclaimer_liability) |
| [Yahoo Finance](https://finance.yahoo.com/) | SMI equities (via yfinance) | Yahoo Finance ToS |

---

## Examples

| Notebook | Description |
|----------|-------------|
| [Markowitz SMI Optimisation](examples/markowitz_smi_optimization.ipynb) | Mean-variance portfolio optimisation on SMI constituents using SARON as risk-free rate |

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
- [x] v0.2.0 — SARON monthly + CHF FX rates
- [x] v0.3.0 — SARON daily + Swiss CPI + inflation
- [x] v0.4.0 — SMI equities (20 constituents, prices, returns)
- [x] v0.5.0 — Swiss Confederation bond yields (13 maturities, yield curve)
- [x] v1.0.0 — Stable public API, full documentation (CONTRIBUTING, DATA_SOURCES)

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for full version history.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Elie Menassa**
- GitHub: [@EMen11](https://github.com/EMen11)
- Email: menassa.elie.dev@gmail.com