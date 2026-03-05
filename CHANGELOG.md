# Changelog

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](https://semver.org/).

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
