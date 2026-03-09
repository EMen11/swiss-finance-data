# swiss-finance-data

> Python package for Swiss financial data — official sources, clean API

[![PyPI version](https://img.shields.io/pypi/v/swiss-finance-data.svg)](https://pypi.org/project/swiss-finance-data/)
[![Tests](https://github.com/EMen11/swiss-finance-data/actions/workflows/test.yml/badge.svg)](https://github.com/EMen11/swiss-finance-data/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/swiss-finance-data.svg)](https://pypi.org/project/swiss-finance-data/)

---

## Why swiss-finance-data?

Accessing Swiss financial data in Python is fragmented. Existing tools focus on US/global markets and provide limited support for Swiss-specific datasets.

**swiss-finance-data** provides:

- A unified, clean API for Swiss financial data
- Official government data sources — no scraping
- Extensible provider architecture
- Long-term maintainability with a stable public API

It does not aim to replace global data providers such as yfinance, but to complement them for Swiss markets.

---

## What's included

| Module | Data | Source |
|--------|------|--------|
| `SNB` | Policy rate, SARON monthly & daily | Swiss National Bank |
| `FX` | CHF exchange rates (9 currencies) | Swiss National Bank |
| `CPI` | Consumer Price Index, YoY inflation | Swiss National Bank |
| `SMI` | 20 SMI constituents, prices, returns | Yahoo Finance |
| `Bonds` | Confederation bond yields, 13 maturities | Swiss National Bank |

---

## Quick Start

```python
from swiss_finance import SNB, FX, CPI, SMI, Bonds

# SNB Policy Rate
rate = SNB.get_policy_rate()
print(f"SNB Policy Rate: {rate}%")
# SNB Policy Rate: 0.5%

# SARON — CHF risk-free rate
saron = SNB.get_saron()
rf_daily = SNB.get_saron_daily() / 100 / 252  # daily risk-free rate
print(f"SARON: {saron}%")
# SARON: 0.52%

# CHF Exchange Rates
eur_chf = FX.get_rate("EUR")
print(f"EUR/CHF: {eur_chf}")
# EUR/CHF: 0.9321

# Swiss CPI and YoY inflation
inflation = CPI.get_inflation_yoy()
print(f"Inflation YoY: {inflation.iloc[-1, 0]:.2f}%")
# Inflation YoY: 1.10%

# SMI equities
prices = SMI.get_prices()
returns = SMI.get_returns(period="1y")

# Swiss Confederation bond yields
yield_10y = Bonds.get_yield("10y")
print(f"10y Confederation bond: {yield_10y:.2f}%")
# 10y Confederation bond: 0.85%

curve = Bonds.get_yield_curve()
```

---

## API Stability

- **v1.0+** — Stable public API, backward compatibility guaranteed
- Versioning follows [Semantic Versioning](https://semver.org/)

See the [Changelog](changelog.md) for full version history.
