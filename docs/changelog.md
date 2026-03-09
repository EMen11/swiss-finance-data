# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.0.0] - 2026-03-06

### Added
- `docs/CONTRIBUTING.md` — developer guide: setup, test, add provider, code style, PR checklist
- `docs/DATA_SOURCES.md` — complete documentation for all 7 verified data sources

### Changed
- Stable public API — all modules complete, backward compatibility guaranteed from this version
- Full docstrings on all public methods (Args, Returns, Raises, Example)

---

## [0.5.0] - 2026-03-06

### Added
- Swiss Confederation bond yields (`Bonds.get_yield`, `Bonds.get_yield_curve`, `Bonds.get_historical_yields`)
- 13 standard maturities: 1y, 2y, 3y, 4y, 5y, 6y, 7y, 8y, 9y, 10y, 15y, 20y, 30y
- Data sourced from SNB official API (`rendoblid` cube)

---

## [0.3.0] - 2026-03-05

### Added
- SARON daily fixing (`SNB.get_saron_daily`, `SNB.get_historical_saron_daily`)
- Swiss CPI index (`CPI.get_current`, `CPI.get_historical`)
- Swiss YoY inflation rate (`CPI.get_inflation_yoy`)

---

## [0.2.0] - 2026-03-05

### Added
- SARON monthly average (`SNB.get_saron`, `SNB.get_historical_saron`)
- CHF FX rates for 9 currencies (`FX.get_rate`, `FX.get_historical_rates`, `FX.list_currencies`)

---

## [0.1.1] - 2026-03-05

### Fixed
- Improved error message when no data available for requested date range
- Added validation: raises `ValueError` when start date is after end date

---

## [0.1.0] - 2026-03-05

### Added
- Initial release
- SNB policy rate (`SNB.get_policy_rate`, `SNB.get_historical_rates`)
- Provider architecture (`ProviderRegistry`)
- Full test suite with CI/CD via GitHub Actions
