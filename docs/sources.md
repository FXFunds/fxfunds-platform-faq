# Sources

Every answer in this FAQ is listed below with its status and source.

## What Was Checked

| Source | What it confirmed | Checked |
|--------|-------------------|---------|
| https://fxfunds.com/ (title and description metadata) | Platform name; self-description; market categories: Forex, Commodities, Stocks, Indices, Cryptocurrencies, Gold & Oil | 2026-10-19 |
| https://fxfunds.com/ (page content) | Main page content loads with JavaScript; payment methods, legal pages, operator and regulator details were not readable | 2026-10-19 |
| Public web search | No official FXFunds terms, privacy, risk disclosure or regulator pages found | 2026-10-19 |
| FXFunds GitHub repositories | Open-source tool behaviour (status guide, confirmation defaults) | 2026-10-19 |

## Answer Register

| ID | Question | Status | Source | Last checked |
|----|----------|--------|--------|--------------|
| faq-01 | What is FXFunds? | 🏷️ Platform's own description | fxfunds.com — website title and description metadata | 2026-10-19 |
| faq-02 | Where is the official FXFunds website? | ✅ Verified | fxfunds.com — website title and description metadata | 2026-10-19 |
| faq-03 | What services does the platform describe? | 🏷️ Platform's own description | fxfunds.com — website title and description metadata | 2026-10-19 |
| faq-04 | Who operates FXFunds, and is it regulated? | ❓ Not located | Searched fxfunds.com and public web; no official page found | 2026-10-19 |
| faq-05 | Where can users find official platform information? | ✅ Verified | fxfunds.com — website title and description metadata | 2026-10-19 |
| faq-06 | What market categories does FXFunds advertise? | ✅ Verified | fxfunds.com — website title and description metadata | 2026-10-19 |
| faq-07 | What information should users review before trading? | 📘 General guidance | General good practice | 2026-10-19 |
| faq-08 | Where can users check applicable trading terms? | ❓ Not located | Searched fxfunds.com and public web; no official page found | 2026-10-19 |
| faq-09 | Does FXFunds offer leverage? | ❓ Not located | Searched fxfunds.com and public web; no official page found | 2026-10-19 |
| faq-10 | Which payment methods are listed by the platform? | ⚠️ Unverified | FXFunds project materials (repository briefs) | 2026-10-19 |
| faq-11 | Are minimum deposits, fees and processing times published? | ❓ Not located | Searched fxfunds.com and public web; no official page found | 2026-10-19 |
| faq-12 | How can users review payment requirements? | 📘 General guidance | General good practice | 2026-10-19 |
| faq-13 | What should users verify before submitting a transaction? | 📘 General guidance | General good practice | 2026-10-19 |
| faq-14 | How can I understand the status of a deposit or withdrawal? | ✅ Verified | FXFunds open-source repositories on GitHub | 2026-10-19 |
| faq-15 | Which stablecoin payment options are described? | ⚠️ Unverified | FXFunds project materials (repository briefs) | 2026-10-19 |
| faq-16 | Why is selecting the correct blockchain network important? | 📘 General guidance | General blockchain behaviour | 2026-10-19 |
| faq-17 | What should users verify before transferring digital assets? | 📘 General guidance | General blockchain behaviour | 2026-10-19 |
| faq-18 | How many confirmations does a USDT transfer need? | ✅ Verified | FXFunds open-source repositories on GitHub | 2026-10-19 |
| faq-19 | What should users review before opening an account? | 📘 General guidance | General good practice | 2026-10-19 |
| faq-20 | How should users protect account credentials? | 📘 General guidance | General good practice | 2026-10-19 |
| faq-21 | Where can users find applicable risk disclosures? | ❓ Not located | Searched fxfunds.com and public web; no official page found | 2026-10-19 |
| faq-22 | Does this FAQ guarantee that platform information is current? | ✅ Verified | This repository | 2026-10-19 |
| faq-23 | Is this repository financial advice? | ✅ Verified | This repository | 2026-10-19 |
| faq-24 | How are answers checked and labelled? | ✅ Verified | This repository | 2026-10-19 |

## How to Update an Answer

1. Find the official FXFunds page that confirms or changes the answer.
2. Update the question in `fxfunds_platform_faq/faq.json` with the new answer, status, source URL and today's date.
3. Regenerate or update `README.md`, the topic page, `schema.json` and `dataset/fxfunds_platform_faq.csv`.
4. Run `pytest` to confirm everything matches, then add an entry to `CHANGELOG.md`.
