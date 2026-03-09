# Bonds — Swiss Confederation Bond Yields

The `Bonds` class provides Swiss Confederation government bond yields, sourced from the Swiss National Bank (monthly data, 13 maturities).

```python
from swiss_finance import Bonds
```

---

## Available maturities

13 standard maturities are supported:

`1y`, `2y`, `3y`, `4y`, `5y`, `6y`, `7y`, `8y`, `9y`, `10y`, `15y`, `20y`, `30y`

---

## `Bonds.list_maturities`

```python
Bonds.list_maturities() -> list
```

List all available bond maturities.

**Example:**

```python
Bonds.list_maturities()
# ['1y', '2y', '3y', '4y', '5y', '6y', '7y', '8y', '9y', '10y', '15y', '20y', '30y']
```

---

## `Bonds.get_yield`

```python
Bonds.get_yield(maturity='10y', provider='snb_bonds') -> float
```

Get the latest yield for a given Swiss Confederation bond maturity.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `maturity` | `str` | Bond maturity (e.g. `'10y'`, `'2y'`, `'30y'`). Default: `'10y'` |
| `provider` | `str` | Data provider (default: `'snb_bonds'`) |

**Returns:** Yield in percent (e.g. `0.85` means 0.85%).

**Raises:** `ValueError` if maturity unknown, `SNBAPIError` if API fails.

**Example:**

```python
yield_10y = Bonds.get_yield("10y")
print(f"10y Confederation bond: {yield_10y:.2f}%")
# 10y Confederation bond: 0.85%

yield_2y = Bonds.get_yield("2y")
yield_30y = Bonds.get_yield("30y")
print(f"2y: {yield_2y:.2f}%  |  30y: {yield_30y:.2f}%")
# 2y: 0.48%  |  30y: 1.12%

# Spread 10y minus 2y
spread = yield_10y - yield_2y
print(f"10y-2y spread: {spread:.2f}%")
# 10y-2y spread: 0.37%
```

---

## `Bonds.get_yield_curve`

```python
Bonds.get_yield_curve(provider='snb_bonds') -> pd.DataFrame
```

Get the latest Swiss Confederation yield curve (all maturities, single row).

**Returns:** DataFrame with one row (latest date) and one column per maturity (`1y`, `2y`, …, `30y`). Values in percent.

**Raises:** `SNBAPIError` if API fails.

**Example:**

```python
curve = Bonds.get_yield_curve()
print(curve.T)
```

```
       2025-12-01
1y         0.42
2y         0.48
3y         0.52
4y         0.58
5y         0.63
6y         0.68
7y         0.72
8y         0.76
9y         0.80
10y        0.85
15y        0.98
20y        1.05
30y        1.12
```

```python
# Plot the yield curve
import matplotlib.pyplot as plt

curve = Bonds.get_yield_curve()
maturities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30]
yields = curve.iloc[0].values

plt.figure(figsize=(10, 5))
plt.plot(maturities, yields, marker="o", color="red")
plt.xlabel("Maturity (years)")
plt.ylabel("Yield (%)")
plt.title(f"Swiss Confederation Yield Curve — {curve.index[0].date()}")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

---

## `Bonds.get_historical_yields`

```python
Bonds.get_historical_yields(
    maturity=None,
    start=None,
    end=None,
    provider='snb_bonds'
) -> pd.DataFrame
```

Get historical Swiss Confederation bond yields.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `maturity` | `str` | Bond maturity (e.g. `'10y'`). If `None`, returns all maturities |
| `start` | `str` | Start date `YYYY-MM-DD` (optional) |
| `end` | `str` | End date `YYYY-MM-DD` (optional) |
| `provider` | `str` | Data provider (default: `'snb_bonds'`) |

**Returns:** DataFrame with `DatetimeIndex` and one column per maturity (or just the requested maturity).

**Raises:** `ValueError` if maturity unknown or `start > end`, `SNBAPIError`.

**Example:**

```python
# Single maturity
hist_10y = Bonds.get_historical_yields(maturity="10y", start="2020-01-01")
print(hist_10y.head())
```

```
              10y
date
2020-01-01   -0.52
2020-02-01   -0.67
2020-03-01   -0.37
2020-04-01   -0.48
2020-05-01   -0.43
```

```python
# All maturities
hist_all = Bonds.get_historical_yields(start="2023-01-01")
print(hist_all.columns.tolist())
# ['1y', '2y', '3y', '4y', '5y', '6y', '7y', '8y', '9y', '10y', '15y', '20y', '30y']

print(hist_all.tail(3))
```

```
               1y    2y    3y   ...   10y   20y   30y
date
2025-10-01   0.38  0.44  0.49  ...  0.82  1.02  1.10
2025-11-01   0.40  0.46  0.51  ...  0.84  1.04  1.11
2025-12-01   0.42  0.48  0.52  ...  0.85  1.05  1.12
```

```python
# Plot 10y yield history
import matplotlib.pyplot as plt

hist = Bonds.get_historical_yields(maturity="10y", start="2015-01-01")
hist.plot(title="Swiss 10y Confederation Bond Yield", figsize=(12, 5))
plt.axhline(0, color="red", linewidth=0.7, linestyle="--")
plt.ylabel("Yield (%)")
plt.tight_layout()
plt.show()
```

---

## Data source

Bond yields are sourced from the SNB data portal (`data.snb.ch`), cube `rendoblid`. Data is monthly. The SNB provides spot interest rates for Swiss Confederation bond issues across 13 standard maturities.
