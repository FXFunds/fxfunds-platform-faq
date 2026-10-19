# Changelog

All notable changes to this FAQ are recorded here.

## [1.0.0] — 2026-10-19

### Added
- 24 questions across 6 topics: Platform Information, Trading and Markets, Deposits and Withdrawals, Cryptocurrency and Stablecoins, Security and Risk, About This FAQ.
- Status labels, sources and last-checked dates for every answer.
- `fxfunds_platform_faq/faq.json` (single source) and `schema.json` (schema.org FAQPage).
- Node.js package `@fxfunds/platform-faq` and Python package `fxfunds-platform-faq` with search, filters and the `fxfunds-faq` CLI.
- Dataset `dataset/fxfunds_platform_faq.csv` for Hugging Face and Kaggle, with a Kaggle notebook.
- Consistency tests and GitHub Actions workflows for tests, npm and PyPI publishing.
- Source register (`docs/sources.md`) and ReadTheDocs documentation.
- Links to related FXFunds repositories.

### Verification notes
- Confirmed from fxfunds.com metadata: platform name, self-description and market categories.
- Not located on public pages: operator, regulator, trading terms, leverage, fees, limits, processing times and risk disclosure.
- USDT on TON, ERC20 and TRC20 is taken from FXFunds project materials and is labelled Unverified until confirmed on the official site.
