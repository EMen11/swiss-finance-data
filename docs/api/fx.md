# FX — CHF Exchange Rates

The `FX` class provides CHF exchange rates sourced from the Swiss National Bank (monthly data, 1999+).

```python
from swiss_finance import FX
```

---

## Supported currencies

| Code | Currency |
|------|----------|
| `EUR` | Euro |
| `USD` | US Dollar |
| `GBP` | British Pound |
| `JPY` | Japanese Yen |
| `CAD` | Canadian Dollar |
| `AUD` | Australian Dollar |
| `SEK` | Swedish Krona |
| `NOK` | Norwegian Krone |
| `DKK` | Danish Krone |

All rates are expressed as **units of foreign currency per 1 CHF**.

---

## `FX.get_rate`

```python
FX.get_rate(currency, provider='snb_fx') -> float
```

Get the current CHF exchange rate for a given currency.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `currency` | `str` | Currency code (e.g. `'EUR'`, `'USD'`) |
| `provider` | `str` | Data provider (default: `'snb_fx'`) |

**Returns:** Current exchange rate as float (units of currency per 1 CHF).

**Raises:** `ValueError` if currency not supported, `FetchError` if fetch fails.

**Example:**

```python
eur_chf = FX.get_rate("EUR")
print(f"EUR/CHF: {eur_chf}")
# EUR/CHF: 0.9321

usd_chf = FX.get_rate("USD")
print(f"USD/CHF: {usd_chf}")
# USD/CHF: 0.8854

# Convert 1000 CHF to EUR
chf_amount = 1000
eur_amount = chf_amount * eur_chf
print(f"1000 CHF = {eur_amount:.2f} EUR")
# 1000 CHF = 932.10 EUR
```

---

## `FX.get_historical_rates`

```python
FX.get_historical_rates(currency, start=None, end=None, provider='snb_fx') -> pd.DataFrame
```

Get historical CHF exchange rates (monthly, 1999+).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `currency` | `str` | Currency code |
| `start` | `str` | Start date `YYYY-MM` (optional) |
| `end` | `str` | End date `YYYY-MM` (optional) |
| `provider` | `str` | Data provider (default: `'snb_fx'`) |

**Returns:** DataFrame with `DatetimeIndex` and `rate` column.

**Raises:** `ValueError` if currency not supported or `start > end`.

**Example:**

```python
rates = FX.get_historical_rates("EUR", start="2020-01", end="2024-12")
print(rates.head())
```

```
              rate
date
2020-01-01    1.0804
2020-02-01    1.0627
2020-03-01    1.0591
2020-04-01    1.0545
2020-05-01    1.0568
```

```python
# Plot EUR/CHF since 2015
import matplotlib.pyplot as plt

rates = FX.get_historical_rates("EUR", start="2015-01")
rates.plot(title="EUR/CHF Monthly (SNB)")
plt.ylabel("EUR per CHF")
plt.tight_layout()
plt.show()
```

```python
# Compare multiple currencies
import pandas as pd

currencies = ["EUR", "USD", "GBP"]
df = pd.DataFrame({
    ccy: FX.get_historical_rates(ccy, start="2020-01")["rate"]
    for ccy in currencies
})
df.plot(title="CHF FX Rates (SNB, 2020+)")
```

---

## `FX.list_currencies`

```python
FX.list_currencies(provider='snb_fx') -> list
```

List all supported currency codes.

**Example:**

```python
FX.list_currencies()
# ['EUR', 'USD', 'GBP', 'JPY', 'CAD', 'AUD', 'SEK', 'NOK', 'DKK']
```

---

## Data source

Exchange rates are sourced from the SNB data portal (`data.snb.ch`), cube `devkum`. Data is monthly and available from January 1999.

!!! note
    Rates represent monthly averages, not spot rates. For intraday or daily FX data, a commercial provider is required.
