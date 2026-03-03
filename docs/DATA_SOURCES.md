# Data Sources

> ⚠️ Ce fichier documente UNIQUEMENT les sources vérifiées manuellement.
> Ne pas coder un provider sans avoir complété sa section ici.

---

## Swiss National Bank (SNB) — Policy Rates

**Status:** ✅ Vérifié le 2026-03-03

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

→ **Opportunité v0.2.0 :** exposer les taux des autres banques centrales sans changer de source.

### Filtre par dim (optionnel)

Pour ne récupérer que le taux SNB :
```
?dimSel=D0(LZ)
```

### Licence

- **Source :** Swiss National Bank — portail officiel data.snb.ch
- **Type :** Swiss Federal Open Government Data
- ✅ Usage gratuit
- ✅ Redistribution commerciale autorisée
- ✅ Attribution source requise : "Source: Swiss National Bank (data.snb.ch)"
- Ref légale : https://www.snb.ch/en/srv/disclaimer_liability

### Stabilité

| Critère           | Évaluation                              |
|-------------------|-----------------------------------------|
| Source            | Banque centrale officielle              |
| Risque downtime   | Très faible                             |
| Risque breaking change | Faible (API mature, versionnée)    |
| Maintenance       | SNB (institution permanente)            |

### Stratégie de fallback

- Si API indisponible → lever `SNBAPIError` avec message clair
- **Pas de scraping backup** (fragile, contre les principes du projet)
- Message d'erreur : `"SNB API unavailable. Check https://data.snb.ch or try later."`

### Corrections vs plan initial

| Plan initial (faux)                                    | Réalité vérifiée                                          |
|--------------------------------------------------------|-----------------------------------------------------------|
| Cube : `snbpol`                                        | Cube : `snboffzisa`                                       |
| Endpoint : `.../data/json`                             | Endpoint : `.../data/json/en`                             |
| Format réponse : `{"observations": [...]}`             | Format réponse : `{"timeseries": [{"values": [...]}]}`    |
| Clés : `obs["date"]`, `obs["value"]`                   | Identique ✅ (`val["date"]`, `val["value"]`)               |
| Parse path : `data["observations"]`                    | Parse path : `data["timeseries"][0]["values"]`            |
| Format date : `YYYY-MM-DD`                             | Format date : `YYYY-MM`                                   |

---

## Sources futures (non vérifiées — ne pas coder)

| Module          | Source envisagée         | Status         | Version cible |
|-----------------|--------------------------|----------------|---------------|
| SMI Equities    | À déterminer             | ⏳ Non vérifié  | v0.2.0        |
| Swiss Bonds     | À déterminer             | ⏳ Non vérifié  | v0.3.0        |
| Real Estate     | SWIIT / À déterminer     | ⏳ Non vérifié  | v0.4.0        |
| SARON           | `zimoma` cube (SNB)      | ⏳ À tester     | v0.2.0        |

---

*Dernière mise à jour : 2026-03-03*