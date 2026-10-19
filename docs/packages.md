# Use the FAQ in Code

The FAQ ships as an offline library for Node.js and Python. Both packages contain the same `faq.json` and make no network calls.

| | Node.js | Python |
|---|---|---|
| Package | [`@fxfunds/platform-faq`](https://www.npmjs.com/package/@fxfunds/platform-faq) | [`fxfunds-platform-faq`](https://pypi.org/project/fxfunds-platform-faq/) |
| Install | `npm install @fxfunds/platform-faq` | `pip install fxfunds-platform-faq` |
| Import | `require("@fxfunds/platform-faq")` | `import fxfunds_platform_faq` |
| CLI | `npx @fxfunds/platform-faq` | `fxfunds-faq` or `python -m fxfunds_platform_faq` |
| Runtime | Node.js 18+ | Python 3.9+ |

## Command Line

| Command | Shows |
|---------|-------|
| `fxfunds-faq` | Topics and question counts |
| `fxfunds-faq search "withdrawal fees"` | Best keyword matches |
| `fxfunds-faq category payments` | All questions in a topic |
| `fxfunds-faq status not-located` | All questions with a status |
| `fxfunds-faq show faq-04` | One question |
| `fxfunds-faq all --json` | Everything as JSON |

Topic IDs: `platform`, `trading`, `payments`, `crypto`, `security`, `about`. Status values: `verified`, `self-described`, `unverified`, `not-located`, `guidance`.

## API

| Node.js | Python | Returns |
|---------|--------|---------|
| `all()` | `all_questions()` | Every question in FAQ order |
| `categories()` | `categories()` | Topics with counts |
| `byCategory(id)` | `by_category(id)` | Questions in a topic |
| `byStatus(status)` | `by_status(status)` | Questions with a status |
| `get(id)` | `get(id)` | One question or `undefined` / `None` |
| `search(query, limit = 5)` | `search(query, limit=5)` | Keyword matches |
| `format(q)` | `format_answer(q)` | Plain-text answer with label, source and date |
| `FAQ`, `STATUS_LABELS`, `LAST_CHECKED` | same | Raw data |

Search ignores common words, then scores each question: a match in the question counts 3, a match in the answer counts 1. Ties keep FAQ order. Node.js and Python return the same results; the tests check this.

## Question Fields

| Field | Example |
|-------|---------|
| `id` | `faq-10` |
| `category` | `payments` |
| `question` | Which payment methods are listed by the platform? |
| `answer` | FXFunds project materials describe USDT ... |
| `status` | `unverified` |
| `source` | FXFunds project materials (repository briefs) |
| `last_checked` | 2026-10-19 |

## Dataset

`dataset/fxfunds_platform_faq.csv` has the same questions with an extra `category_name` and `status_label` column. It is published on [Hugging Face](https://huggingface.co/datasets/FXFunds/platform-faq) and [Kaggle](https://www.kaggle.com/datasets/fxfunds/platform-faq).
