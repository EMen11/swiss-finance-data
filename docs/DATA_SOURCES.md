# Data Sources

> This file documents all verified data sources used in swiss-finance-data v1.0.0.

---

## 1. SNB Policy Rate

**Status:** ✅ Verified 2026-03-03

### Endpoint

```
https://data.snb.ch/api/cube/snboffzisa/data/json/en
```

**Avec filtre de dates :**
```
https://data.snb.ch/api/cube/snboffzisa/data/json/en?fromDate=2020-01&toDate=2025-03
```

**Structure des dimensions :**
```
https://data.snb.ch/api/cube/snboffzisa/dimensions/en
```

### Structure JSON retournée

```json
{
  "timeseries": [
    {
      "header": [
        {"dim": "Overview", "dimItem": "Switzerland - SNB policy rate"}
      ],
      "metadata": {
        "key": "EPB@SNB.snboffzisa{LZ}",
        "frequency": "P1M",
        "scale": "",
        "unit": "In percent"
      },
      "values": [
        {"date": "2019-06", "value": -0.75},
        {"date": "2024-03", "value": 1.5},
        {"date": "2025-01", "value": 0.5}
      ]
    }
  ]
}
```

**Parse path :** `response["timeseries"][0]["values"]`
**Chaque entrée :** `{"date": "YYYY-MM", "value": float}`

### Caractéristiques

| Propriété          | Valeur                                |
|--------------------|---------------------------------------|
| Format             | JSON                                  |
| Auth requise       | Non                                   |
| Rate limits        | Non documentés (usage raisonnable)    |
| Fréquence données  | Mensuelle (P1M)                       |
| Historique         | Depuis 2019-06 (SNB policy rate)      |
| Unité              | Pourcentage                           |
| Cube ID            | `snboffzisa`                          |
| Dim item SNB       | `LZ` (SNB policy rate)                |

### Bonus — Autres taux dans le même cube

Le cube `snboffzisa` contient aussi (gratuit, même endpoint) :

| Banque Centrale | Dim ID | Description                          |
|-----------------|--------|--------------------------------------|
| SNB (CH)        | `LZ`   | SNB policy rate                      |
| Fed (US)        | `UG1`/`OG1` | Fed target range (lower/upper)  |
| ECB (Euro)      | `H`    | Main refinancing rate                |
| ECB (Euro)      | `EF`   | Deposit Facility                     |
| BoE (UK)        | `L0`   | Bank of England - Bank rate          |
| BoJ (Japan)     | `L1`   | Uncollateralized overnight call rate |

### License

Swiss National Bank — Swiss Federal Open Government Data.
Free use, commercial redistribution allowed, attribution required.
Ref: https://www.snb.ch/en/srv/disclaimer_liability

---

## 2. SARON Monthly Average

**Status:** ✅ Verified 2026-03-05 | Cube: `zimoma`

### Endpoint

```
https://data.snb.ch/api/cube/zimoma/data/json/en?dimSel=D0(SARON)
```

### Response structure

Same `timeseries[].values[]` format as SNB policy rate.
`{"date": "YYYY-MM", "value": float}`

### Characteristics

| Property      | Value                     |
|---------------|---------------------------|
| Frequency     | Monthly (P1M)             |
| History       | Since 2009-06             |
| Unit          | Percent                   |
| Dim filter    | `D0(SARON)`               |

### License

Same as SNB policy rate — Swiss Federal Open Government Data.

---

## 3. SARON Daily Fixing

**Status:** ✅ Verified 2026-03-05 | Cube: `snbgwdzid`

### Endpoint

```
https://data.snb.ch/api/cube/snbgwdzid/data/json/en?dimSel=D0(SARON)
https://data.snb.ch/api/cube/snbgwdzid/data/json/en?dimSel=D0(SARON)&fromDate=2024-01-01&toDate=2024-12-31
```

### Response structure

Same format — `{"date": "YYYY-MM-DD", "value": float}` — business days only.

### Characteristics

| Property      | Value                             |
|---------------|-----------------------------------|
| Frequency     | Daily (P1D), business days only   |
| History       | Since 2009-06-22                  |
| Unit          | Percent                           |
| Dim filter    | `D0(SARON)`                       |

### License

Same as SNB policy rate — Swiss Federal Open Government Data.

---

## 4. CHF FX Rates

**Status:** ✅ Verified 2026-03-05 | Cube: `devkum`

### Endpoint

```
https://data.snb.ch/api/cube/devkum/data/json/en?dimSel=D0(EUR,USD,GBP,JPY,CAD,AUD,SEK,NOK,DKK)
```

### Response structure

Multiple timeseries, one per currency. Currency code is identified via `dimItem` header.
`{"date": "YYYY-MM", "value": float}` — units of currency per 1 CHF.

### Supported currencies

`EUR`, `USD`, `GBP`, `JPY`, `CAD`, `AUD`, `SEK`, `NOK`, `DKK`

### Characteristics

| Property      | Value                                    |
|---------------|------------------------------------------|
| Frequency     | Monthly (P1M)                            |
| History       | Since 1999-01 (EUR), varies by pair      |
| Unit          | Foreign currency units per 1 CHF         |

### License

Same as SNB policy rate — Swiss Federal Open Government Data.

---

## 5. Swiss CPI (Consumer Price Index)

**Status:** ✅ Verified 2026-03-05 | Cube: `plkopr`

### Endpoint

```
https://data.snb.ch/api/cube/plkopr/data/json/en
```

### Response structure

Single timeseries. `{"date": "YYYY-MM", "value": float}` — index value (Dec 2020 = 100).

### Characteristics

| Property      | Value                        |
|---------------|------------------------------|
| Frequency     | Monthly (P1M)                |
| History       | Since 1921-01                |
| Unit          | Index (December 2020 = 100)  |

### License

Same as SNB policy rate — Swiss Federal Open Government Data.

---

## 6. Swiss Confederation Bond Yields

**Status:** ✅ Verified 2026-03-06 | Cube: `rendoblid`

### Endpoint

```
https://data.snb.ch/api/cube/rendoblid/data/json/en
```

No `dimSel` needed — all 22 series are fetched and filtered client-side.

### Response structure

22 timeseries total. The 13 relevant ones (Confederation bonds) are identified by matching
`"CHF Swiss Confederation bond issues"` in the `dimItem` header field.
Maturity is extracted from the text suffix via regex `r'(\d+) years?$'`.

```json
{
  "timeseries": [{
    "header": [{"dimItem": "Spot interest rates ... - CHF Swiss Confederation bond issues - 10 years"}],
    "values": [{"date": "YYYY-MM-DD", "value": 0.378}]
  }]
}
```

### Available maturities

1y, 2y, 3y, 4y, 5y, 6y, 7y, 8y, 9y, 10y, 15y, 20y, 30y

### Characteristics

| Property      | Value                                         |
|---------------|-----------------------------------------------|
| Frequency     | Monthly (P1M)                                 |
| History       | Since mid-1990s (varies by maturity)          |
| Unit          | Percent (spot interest rate)                  |

### Parsing note

`dimSel` with short codes (`Y10` etc.) does NOT work for this cube.
Use full fetch without `dimSel` and filter by `dimItem` text.

### License

Same as SNB policy rate — Swiss Federal Open Government Data.

---

## 7. SMI Equities

**Status:** ✅ Verified 2026-03-05 | Source: Yahoo Finance (via `yfinance`)

### Tickers

20 SMI constituents with `.SW` suffix:
`NESN.SW`, `ROG.SW`, `NOVN.SW`, `UBSG.SW`, `ZURN.SW`, `ABBN.SW`,
`SREN.SW`, `GIVN.SW`, `LONN.SW`, `SIKA.SW`, `GEBN.SW`, `SLHN.SW`,
`SCMN.SW`, `HOLN.SW`, `PGHN.SW`, `CFR.SW`, `ALC.SW`, `SDZ.SW`,
`STMN.SW`, `VACN.SW`

### Characteristics

| Property      | Value                                |
|---------------|--------------------------------------|
| Frequency     | Daily (business days)                |
| History       | Varies by ticker (~10+ years)        |
| Unit          | CHF (adjusted closing price)         |
| Auth required | No                                   |

### License

Yahoo Finance Terms of Service — personal/research use.
Not for commercial redistribution of raw data.

---

*Last updated: 2026-03-06*