# Examples

Concrete usage examples with expected outputs.

---

## SNB Policy Rate — current and historical

```python
from swiss_finance import SNB

# Current rate
rate = SNB.get_policy_rate()
print(f"SNB Policy Rate: {rate}%")
# SNB Policy Rate: 0.5%

# Historical rates since 2000
hist = SNB.get_historical_rates(start="2000-01")
print(hist.tail(5))
```

```
              rate
date
2025-08-01    0.50
2025-09-01    0.50
2025-10-01    0.50
2025-11-01    0.50
2025-12-01    0.50
```

```python
# Negative rate period
neg = hist.loc[hist["rate"] < 0]
print(f"Negative rates: {neg.index[0].date()} → {neg.index[-1].date()}")
# Negative rates: 2015-01-22 → 2022-06-16
```

---

## SARON — daily risk-free rate for quantitative finance

```python
from swiss_finance import SNB

# Current daily fixing
saron = SNB.get_saron_daily()
rf_daily = saron / 100 / 252

print(f"SARON daily fixing : {saron:.4f}%")
print(f"Daily risk-free rate: {rf_daily:.8f}")
# SARON daily fixing : 0.5150%
# Daily risk-free rate: 0.00000204
```

```python
# Historical daily series for backtesting
import pandas as pd

saron_hist = SNB.get_historical_saron_daily(start="2024-01-01")

# Cumulative compounded risk-free return (money market account)
rf_cumret = (1 + saron_hist["rate"] / 100 / 252).cumprod()
rf_cumret.plot(title="Cumulative risk-free return (SARON compounded)")
```

---

## FX — Swiss franc conversion

```python
from swiss_finance import FX

# Convert 10,000 USD to CHF
usd_per_chf = FX.get_rate("USD")
chf_per_usd = 1 / usd_per_chf
print(f"USD/CHF spot: {chf_per_usd:.4f}")
print(f"10,000 USD = {10_000 * chf_per_usd:.0f} CHF")
# USD/CHF spot: 1.1294
# 10,000 USD = 11,294 CHF
```

```python
# EUR/CHF weakening since 2015 SNB floor removal
import matplotlib.pyplot as plt

eur = FX.get_historical_rates("EUR", start="2014-01")
eur.plot(figsize=(12, 4), title="EUR/CHF — Monthly (SNB, 2014+)", color="red")
plt.axhline(1.20, color="black", linestyle="--", label="Former SNB floor (1.20)")
plt.legend()
plt.tight_layout()
plt.show()
```

---

## Swiss Inflation vs SNB Policy Rate

```python
from swiss_finance import CPI, SNB
import matplotlib.pyplot as plt

inflation = CPI.get_inflation_yoy(start="2015-01")
rates     = SNB.get_historical_rates(start="2015-01")

fig, ax = plt.subplots(figsize=(12, 5))
inflation["inflation_yoy"].plot(ax=ax, label="CPI YoY %", color="orange")
rates["rate"].plot(ax=ax, label="SNB Policy Rate %", color="red")
ax.axhline(0, color="black", linewidth=0.5)
ax.axhline(2, color="gray", linewidth=0.5, linestyle="--", label="2% target")
ax.legend()
ax.set_title("Swiss Inflation vs SNB Policy Rate (2015+)")
plt.tight_layout()
plt.show()
```

Expected output: the chart shows the inflation spike of 2022–2023 followed by SNB tightening, then reversal.

---

## Swiss Confederation yield curve

```python
from swiss_finance import Bonds
import matplotlib.pyplot as plt

curve = Bonds.get_yield_curve()
maturities = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 30]
yields = curve.iloc[0].values

plt.figure(figsize=(10, 5))
plt.plot(maturities, yields, marker="o", color="red", linewidth=2)
plt.fill_between(maturities, yields, alpha=0.1, color="red")
plt.xlabel("Maturity (years)")
plt.ylabel("Yield (%)")
plt.title(f"Swiss Confederation Yield Curve — {curve.index[0].strftime('%Y-%m-%d')}")
plt.grid(True, alpha=0.3)
plt.axhline(0, color="black", linewidth=0.5)
plt.tight_layout()
plt.show()
```

---

## Markowitz Portfolio Optimisation — SMI + SARON

This example runs a mean-variance optimisation on all 20 SMI constituents, using the SARON daily fixing as risk-free rate. A full version with frontier plot is available in [examples/markowitz_smi_optimization.ipynb](https://github.com/EMen11/swiss-finance-data/blob/main/examples/markowitz_smi_optimization.ipynb).

```python
import numpy as np
import pandas as pd
from swiss_finance import SMI, SNB

# --- Data ---
returns = SMI.get_returns(period="3y")          # 3-year daily returns, 20 stocks
rf      = SNB.get_saron_daily() / 100 / 252     # daily risk-free rate

mu    = returns.mean() * 252                    # annualised expected returns
sigma = returns.cov()  * 252                    # annualised covariance matrix

print(f"Assets : {returns.shape[1]}")
print(f"Obs    : {returns.shape[0]} trading days")
print(f"Rf/day : {rf:.8f}")
# Assets : 20
# Obs    : 756 trading days
# Rf/day : 0.00000204
```

```python
# --- Monte Carlo simulation ---
n_portfolios = 10_000
n_assets = len(mu)
results = np.zeros((3, n_portfolios))

for i in range(n_portfolios):
    w = np.random.dirichlet(np.ones(n_assets))
    ret  = w @ mu.values
    risk = np.sqrt(w @ sigma.values @ w)
    sharpe = (ret - rf * 252) / risk
    results[:, i] = [ret, risk, sharpe]

# Max Sharpe portfolio
idx_max = results[2].argmax()
print(f"\nMax Sharpe Portfolio:")
print(f"  Expected return : {results[0, idx_max]:.2%}")
print(f"  Volatility      : {results[1, idx_max]:.2%}")
print(f"  Sharpe ratio    : {results[2, idx_max]:.3f}")
```

```
Max Sharpe Portfolio:
  Expected return : 12.84%
  Volatility      : 11.20%
  Sharpe ratio    : 1.143
```

```python
# --- Plot efficient frontier ---
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
sc = plt.scatter(
    results[1], results[0],
    c=results[2], cmap="RdYlGn",
    alpha=0.5, s=5
)
plt.colorbar(sc, label="Sharpe Ratio")
plt.scatter(results[1, idx_max], results[0, idx_max],
            color="red", marker="*", s=200, zorder=5, label="Max Sharpe")
plt.xlabel("Annualised Volatility")
plt.ylabel("Annualised Return")
plt.title("SMI — Efficient Frontier (Monte Carlo, 10k portfolios)")
plt.legend()
plt.tight_layout()
plt.show()
```
