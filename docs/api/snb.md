# SNB & SARON

The `SNB` class provides access to Swiss National Bank policy rates and SARON (Swiss Average Rate Overnight), the CHF risk-free reference rate.

```python
from swiss_finance import SNB
```

---

## Policy Rate

### `SNB.get_policy_rate`

```python
SNB.get_policy_rate(provider='snb_official') -> float
```

Get the current SNB policy rate.

**Returns:** Current policy rate in percent (e.g. `0.5` means 0.5%).

**Raises:** `SNBAPIError` if the API call fails.

**Example:**

```python
rate = SNB.get_policy_rate()
print(f"SNB Policy Rate: {rate}%")
# SNB Policy Rate: 0.5%
```

---

### `SNB.get_historical_rates`

```python
SNB.get_historical_rates(start=None, end=None, provider='snb_official') -> pd.DataFrame
```

Get historical SNB policy rates.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | `str` | Start date `YYYY-MM` (optional) |
| `end` | `str` | End date `YYYY-MM` (optional) |
| `provider` | `str` | Data provider (default: `'snb_official'`) |

**Returns:** DataFrame with `DatetimeIndex` and `rate` column (float, percent).

**Raises:** `ValueError` if `start > end`.

**Example:**

```python
rates = SNB.get_historical_rates(start="2015-01", end="2025-12")
print(rates.head())
```

```
            rate
date
2015-01-01  0.00
2015-02-01 -0.75
2015-03-01 -0.75
...
```

```python
# Plot
rates.plot(title="SNB Policy Rate")
```

---

## SARON — Monthly average

### `SNB.get_saron`

```python
SNB.get_saron(provider='saron') -> float
```

Get the current SARON monthly average. The SARON is the CHF risk-free reference rate, replacing LIBOR CHF since 2021.

**Returns:** Current SARON monthly average in percent.

**Raises:** `SNBAPIError`, `FetchError`.

**Example:**

```python
saron = SNB.get_saron()
print(f"SARON: {saron}%")
# SARON: 0.52%

# Use as annual risk-free rate for Sharpe ratio
rf_annual = saron / 100
```

---

### `SNB.get_historical_saron`

```python
SNB.get_historical_saron(start=None, end=None) -> pd.DataFrame
```

Get historical SARON monthly averages (data available from 2009).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | `str` | Start date `YYYY-MM` (optional) |
| `end` | `str` | End date `YYYY-MM` (optional) |

**Returns:** DataFrame with `DatetimeIndex` and `rate` column.

**Raises:** `ValueError` if `start > end`, `SNBAPIError`.

**Example:**

```python
saron = SNB.get_historical_saron(start="2021-01")
print(saron.tail(5))
```

```
              rate
date
2025-08-01    0.44
2025-09-01    0.42
2025-10-01    0.40
2025-11-01    0.52
2025-12-01    0.52
```

---

## SARON — Daily fixing

### `SNB.get_saron_daily`

```python
SNB.get_saron_daily() -> float
```

Get the latest SARON daily fixing. Published at the close of each business day. More granular than the monthly average — use for daily risk calculations.

**Returns:** Latest SARON daily fixing in percent.

**Example:**

```python
saron = SNB.get_saron_daily()
print(f"SARON daily: {saron}%")
# SARON daily: 0.515%

# Daily risk-free rate for Sharpe ratio
rf_daily = saron / 100 / 252
print(f"Daily rf: {rf_daily:.8f}")
# Daily rf: 0.00000204
```

---

### `SNB.get_historical_saron_daily`

```python
SNB.get_historical_saron_daily(start=None, end=None) -> pd.DataFrame
```

Get historical SARON daily fixings (business days only, data from 2009).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | `str` | Start date `YYYY-MM-DD` (optional) |
| `end` | `str` | End date `YYYY-MM-DD` (optional) |

**Returns:** DataFrame with `DatetimeIndex` (business days) and `rate` column.

**Raises:** `ValueError` if `start > end`, `SNBAPIError`.

**Example:**

```python
saron = SNB.get_historical_saron_daily(start="2024-01-01", end="2024-12-31")
print(saron.head(5))
```

```
              rate
date
2024-01-02    1.72
2024-01-03    1.72
2024-01-04    1.72
2024-01-05    1.72
2024-01-08    1.72
```

```python
# Cumulative compounded risk-free return
rf_cumulative = ((1 + saron["rate"] / 100 / 252)).cumprod()
```

---

## Provider utilities

### `SNB.list_providers`

```python
SNB.list_providers() -> list
```

List all registered SNB data providers.

**Example:**

```python
SNB.list_providers()
# ['snb_official', 'saron']
```

---

## Data source

All SNB data is fetched from the official [SNB data portal](https://data.snb.ch/) (`data.snb.ch`).

| Dataset | SNB Cube |
|---------|----------|
| Policy Rate | `snboffzisa` |
| SARON monthly | `zimoma` |
| SARON daily | `snbgwdzid` |
