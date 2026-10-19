# Contributing to FXFunds Platform FAQ

Thank you for helping keep this FAQ accurate.

## What Makes a Good Change

- Corrects or confirms an answer using an **official FXFunds source** (a page on https://fxfunds.com/ or an official FXFunds document).
- Makes an answer clearer or shorter without changing its meaning.
- Adds a frequently asked question with a sourced answer.

## Rules

1. **Source every platform-specific claim.** Include the official URL. Without one, the answer must be labelled `unverified` or `not-located`.
2. **No guarantees.** Do not promise returns, withdrawal times, security or regulatory status.
3. **No invented details.** Never add licence numbers, regulators, company names, fees or limits that you cannot source.
4. **Keep files in sync.** `fxfunds_platform_faq/faq.json` is the single source. Update `README.md`, the topic page in `docs/`, `docs/sources.md`, `schema.json` and `dataset/fxfunds_platform_faq.csv` to match, then run `pytest`.
5. **Record the date.** Set `last_checked` to the date you checked the source, and add a `CHANGELOG.md` entry.

## Status Values

| Value | Use when |
|-------|----------|
| `verified` | Confirmed on an official FXFunds source |
| `self-described` | Quoting FXFunds' own marketing or description |
| `unverified` | Stated in project materials but not confirmed on an official public page |
| `not-located` | No official source could be found |
| `guidance` | General good practice, not a claim about FXFunds |

## Pull Requests

Describe what changed and link the source you used. Pull requests without sources for platform-specific claims will be asked to relabel the answer.
