# CPI — Swiss Consumer Price Index

The `CPI` class provides access to Swiss Consumer Price Index data and year-over-year inflation rates, sourced from the Swiss National Bank (monthly data, 1921+).

```python
from swiss_finance import CPI
```

---

## `CPI.get_current`

```python
CPI.get_current(provider='snb_cpi') -> float
```

Get the latest Swiss CPI index value.

**Returns:** Latest CPI index value (December 2020 = 100).

**Raises:** `SNBAPIError` if the API call fails.

**Example:**

```python
cpi = CPI.get_current()
print(f"Swiss CPI: {cpi:.2f}")
# Swiss CPI: 107.40
```

---

## `CPI.get_historical`

```python
CPI.get_historical(start=None, end=None, provider='snb_cpi') -> pd.DataFrame
```

Get historical Swiss CPI index values (monthly, 1921+).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | `str` | Start date `YYYY-MM` (optional) |
| `end` | `str` | End date `YYYY-MM` (optional) |
| `provider` | `str` | Data provider (default: `'snb_cpi'`) |

**Returns:** DataFrame with `DatetimeIndex` and `cpi` column.

**Raises:** `ValueError` if `start > end`, `SNBAPIError`.

**Example:**

```python
cpi = CPI.get_historical(start="2020-01")
print(cpi.head())
```

```
              cpi
date
2020-01-01    101.2
2020-02-01    101.5
2020-03-01    101.4
2020-04-01    100.9
2020-05-01    100.7
```

```python
# Full history since 1921
cpi_all = CPI.get_historical()
print(f"Data from {cpi_all.index[0].year} to {cpi_all.index[-1].year}")
# Data from 1921 to 2025

cpi_all.plot(title="Swiss CPI (SNB, 1921+)")
```

---

## `CPI.get_inflation_yoy`

```python
CPI.get_inflation_yoy(start=None, end=None, provider='snb_cpi') -> pd.DataFrame
```

Get Swiss year-over-year inflation rate. Computed as `(CPI_t / CPI_{t-12} - 1) * 100`.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | `str` | Start date `YYYY-MM` (optional) |
| `end` | `str` | End date `YYYY-MM` (optional) |
| `provider` | `str` | Data provider (default: `'snb_cpi'`) |

**Returns:** DataFrame with `DatetimeIndex` and `inflation_yoy` column (percentage).

**Raises:** `ValueError` if `start > end`, `SNBAPIError`.

**Example:**

```python
inflation = CPI.get_inflation_yoy(start="2020-01")
print(inflation.tail(5))
```

```
              inflation_yoy
date
2025-08-01           1.30
2025-09-01           1.15
2025-10-01           1.08
2025-11-01           1.12
2025-12-01           1.10
```

```python
# Latest value
latest = inflation.iloc[-1, 0]
print(f"Latest YoY inflation: {latest:.2f}%")
# Latest YoY inflation: 1.10%

# Peak inflation during 2022 energy crisis
peak = inflation.loc["2022-01":"2023-12"]["inflation_yoy"].max()
print(f"Peak inflation (2022–2023): {peak:.2f}%")
# Peak inflation (2022–2023): 3.50%
```

```python
# Plot inflation alongside policy rate
import matplotlib.pyplot as plt
from swiss_finance import SNB

fig, ax = plt.subplots(figsize=(12, 5))
inflation = CPI.get_inflation_yoy(start="2015-01")
rates = SNB.get_historical_rates(start="2015-01")

inflation["inflation_yoy"].plot(ax=ax, label="CPI YoY %")
rates["rate"].plot(ax=ax, label="SNB Policy Rate %")
ax.axhline(0, color="black", linewidth=0.5)
ax.legend()
ax.set_title("Swiss Inflation vs SNB Policy Rate")
plt.tight_layout()
plt.show()
```

---

## Data source

CPI data is sourced from the SNB data portal (`data.snb.ch`), cube `plkopr`. Index base: December 2020 = 100. Monthly frequency, available from 1921.
