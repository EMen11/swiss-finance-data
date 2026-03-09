# SMI — Swiss Market Index Equities

The `SMI` class provides access to all 20 Swiss Market Index constituents: current prices, historical prices, and daily returns. Data sourced from Yahoo Finance via yfinance.

```python
from swiss_finance import SMI
```

---

## SMI Constituents

All 20 SMI constituents (as of 2025):

| Ticker | Company |
|--------|---------|
| `NESN.SW` | Nestlé |
| `ROG.SW` | Roche Holding |
| `NOVN.SW` | Novartis |
| `UBSG.SW` | UBS Group |
| `ZURN.SW` | Zurich Insurance |
| `ABBN.SW` | ABB |
| `SREN.SW` | Swiss Re |
| `GIVN.SW` | Givaudan |
| `LONN.SW` | Lonza Group |
| `SIKA.SW` | Sika |
| `GEBN.SW` | Geberit |
| `SLHN.SW` | Swiss Life |
| `SCMN.SW` | Swisscom |
| `HOLN.SW` | Holcim |
| `PGHN.SW` | Partners Group |
| `CFR.SW` | Compagnie Financière Richemont |
| `ALC.SW` | Alcon |
| `SDZ.SW` | Sandoz |
| `STMN.SW` | Straumann Holding |
| `VACN.SW` | VAT Group |

---

## `SMI.get_constituents`

```python
SMI.get_constituents() -> dict
```

Get all SMI constituents as a `{ticker: company_name}` dictionary.

**Returns:** dict mapping yfinance ticker to company name.

**Example:**

```python
constituents = SMI.get_constituents()
print(constituents["NESN.SW"])
# Nestlé

print(list(constituents.keys()))
# ['NESN.SW', 'ROG.SW', 'NOVN.SW', ...]
```

---

## `SMI.get_prices`

```python
SMI.get_prices() -> pd.DataFrame
```

Get current prices for all 20 SMI constituents.

**Returns:** DataFrame with ticker index and `name`, `price` columns.

**Example:**

```python
prices = SMI.get_prices()
print(prices)
```

```
          name             price
NESN.SW   Nestlé            94.50
ROG.SW    Roche Holding    264.30
NOVN.SW   Novartis          94.82
UBSG.SW   UBS Group         28.45
ZURN.SW   Zurich Insurance 490.10
...
```

```python
# Most expensive stocks
print(prices.sort_values("price", ascending=False).head(5))
```

---

## `SMI.get_historical_prices`

```python
SMI.get_historical_prices(
    tickers=None,
    period='1y',
    start=None,
    end=None
) -> pd.DataFrame
```

Get historical daily closing prices for SMI constituents.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `tickers` | `list` | List of tickers (default: all 20) |
| `period` | `str` | `'1y'`, `'6mo'`, `'2y'`, etc. Ignored if `start`/`end` provided |
| `start` | `str` | Start date `YYYY-MM-DD` (optional) |
| `end` | `str` | End date `YYYY-MM-DD` (optional) |

**Returns:** DataFrame with `DatetimeIndex` and one column per ticker.

**Raises:** `ValueError` if unknown tickers or `start > end`.

**Example:**

```python
# All 20 constituents, last year
prices = SMI.get_historical_prices(period="1y")
print(prices.shape)
# (252, 20)

# Specific tickers with date range
prices = SMI.get_historical_prices(
    tickers=["NESN.SW", "ROG.SW", "NOVN.SW"],
    start="2023-01-01",
    end="2024-12-31"
)
print(prices.tail(3))
```

```
            NESN.SW   ROG.SW   NOVN.SW
Date
2024-12-27    94.12   262.80    93.50
2024-12-28    94.20   263.10    93.75
2024-12-29    94.50   264.30    94.82
```

---

## `SMI.get_returns`

```python
SMI.get_returns(
    tickers=None,
    period='1y',
    start=None,
    end=None
) -> pd.DataFrame
```

Get daily returns for SMI constituents (simple percentage change, as decimals).

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `tickers` | `list` | List of tickers (default: all 20) |
| `period` | `str` | `'1y'`, `'6mo'`, `'2y'`, etc. Ignored if `start`/`end` provided |
| `start` | `str` | Start date `YYYY-MM-DD` (optional) |
| `end` | `str` | End date `YYYY-MM-DD` (optional) |

**Returns:** DataFrame with `DatetimeIndex` and daily returns as decimals (e.g. `0.012` = +1.2%).

**Raises:** `ValueError` if unknown tickers or `start > end`.

**Example:**

```python
from swiss_finance import SMI, SNB

returns = SMI.get_returns(period="1y")
print(returns.head(3))
```

```
            NESN.SW    ROG.SW   NOVN.SW  ...
Date
2024-01-03  0.00821  -0.01203  0.00345  ...
2024-01-04  0.00120   0.00400 -0.00210  ...
2024-01-05 -0.00500   0.00050  0.00180  ...
```

```python
# Annualised statistics
mean_ret = returns.mean() * 252
std_ret  = returns.std() * (252 ** 0.5)
rf_daily = SNB.get_saron_daily() / 100 / 252

sharpe = (returns.mean() - rf_daily) / returns.std() * (252 ** 0.5)
print(sharpe.sort_values(ascending=False))
```

---

## Data source

SMI equity data is fetched from [Yahoo Finance](https://finance.yahoo.com/) via the `yfinance` library. Data is adjusted for splits and dividends.

!!! note
    Yahoo Finance ToS apply. This module is intended for research and educational use.
