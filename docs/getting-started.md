# Getting Started

## Requirements

- Python 3.10 or higher
- Internet access — data is fetched live from official sources

## Installation

```bash
pip install swiss-finance-data
```

For development (includes pytest):

```bash
git clone https://github.com/EMen11/swiss-finance-data.git
cd swiss-finance-data
pip install -e .[dev]
```

---

## Imports

All public classes are available directly from `swiss_finance`:

```python
from swiss_finance import SNB, FX, CPI, SMI, Bonds
```

Error classes:

```python
from swiss_finance import SNBAPIError, DataValidationError, FetchError
```

---

## First complete example

The following script fetches a snapshot of the main Swiss financial indicators:

```python
from swiss_finance import SNB, FX, CPI, SMI, Bonds

# --- Rates ---
print("=== SNB Policy Rate ===")
rate = SNB.get_policy_rate()
print(f"Current rate: {rate}%")

print("\n=== SARON ===")
saron_monthly = SNB.get_saron()
saron_daily = SNB.get_saron_daily()
rf_annual = saron_daily / 100
rf_daily  = rf_annual / 252
print(f"Monthly avg : {saron_monthly:.4f}%")
print(f"Daily fixing: {saron_daily:.4f}%")
print(f"Daily rf    : {rf_daily:.8f}")

# --- FX ---
print("\n=== CHF Exchange Rates ===")
for ccy in ["EUR", "USD", "GBP"]:
    rate = FX.get_rate(ccy)
    print(f"  {ccy}/CHF: {rate:.4f}")

# --- CPI ---
print("\n=== Swiss Inflation ===")
cpi = CPI.get_current()
inflation = CPI.get_inflation_yoy()
print(f"CPI index  : {cpi:.2f}")
print(f"YoY infl.  : {inflation.iloc[-1, 0]:.2f}%")

# --- SMI Equities ---
print("\n=== SMI (top 3 by weight) ===")
prices = SMI.get_prices()
print(prices.loc[["NESN.SW", "ROG.SW", "NOVN.SW"]])

# --- Confederation Bonds ---
print("\n=== Yield Curve ===")
curve = Bonds.get_yield_curve()
print(curve.T.rename(columns={curve.index[0]: "yield %"}))
```

Expected output (values vary with market):

```
=== SNB Policy Rate ===
Current rate: 0.5%

=== SARON ===
Monthly avg : 0.5200%
Daily fixing: 0.5150%
Daily rf    : 0.00000204

=== CHF Exchange Rates ===
  EUR/CHF: 0.9321
  USD/CHF: 0.8854
  GBP/CHF: 1.1203

=== Swiss Inflation ===
CPI index  : 107.40
YoY infl.  : 1.10%

=== SMI (top 3 by weight) ===
          name   price
NESN.SW  Nestlé   94.50
ROG.SW   Roche   264.30
NOVN.SW  Novartis 94.82

=== Yield Curve ===
      yield %
1y      0.42
2y      0.48
3y      0.52
...
10y     0.85
30y     1.12
```

---

## Error handling

```python
from swiss_finance import SNB, SNBAPIError, DataValidationError

# Invalid date range
try:
    rates = SNB.get_historical_rates(start="2030-01")
except DataValidationError as e:
    print(f"Invalid date: {e}")

# Future date / API failure
try:
    rate = SNB.get_policy_rate()
except SNBAPIError as e:
    print(f"API error: {e}")
```

---

## Next steps

- [SNB & SARON API reference](api/snb.md)
- [FX Rates API reference](api/fx.md)
- [CPI & Inflation API reference](api/cpi.md)
- [SMI Equities API reference](api/smi.md)
- [Bonds API reference](api/bonds.md)
- [Examples — Markowitz portfolio optimisation](examples.md)
