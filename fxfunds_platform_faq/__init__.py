"""
FXFunds Platform FAQ
Search and read the FXFunds Platform FAQ. Every answer carries a verification
status, a source and a last-checked date. Works offline; no network calls.
Built by FXFunds — https://fxfunds.com/
"""

__version__ = "1.0.0"

import json
import re
from importlib import resources
from typing import Dict, List, Optional

__all__ = ["FAQ", "STATUS_LABELS", "LAST_CHECKED", "all_questions", "categories", "by_category",
           "by_status", "get", "search", "format_answer", "tokenize"]

FAQ: Dict = json.loads(resources.files(__package__).joinpath("faq.json").read_text(encoding="utf-8"))
STATUS_LABELS: Dict = FAQ["status_labels"]
LAST_CHECKED: str = FAQ["last_checked"]

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "can", "do", "does", "for", "from", "how", "i", "in", "is",
    "it", "my", "of", "on", "or", "the", "to", "what", "where", "which", "who", "why", "with", "fxfunds",
}


def tokenize(text: str) -> List[str]:
    return [w for w in re.split(r"[^a-z0-9]+", text.lower()) if len(w) >= 2 and w not in STOPWORDS]


def all_questions() -> List[Dict]:
    """All questions, in FAQ order."""
    return list(FAQ["questions"])


def categories() -> List[Dict]:
    """Categories with their question counts."""
    return [{**c, "count": sum(1 for q in FAQ["questions"] if q["category"] == c["id"])} for c in FAQ["categories"]]


def by_category(category_id: str) -> List[Dict]:
    return [q for q in FAQ["questions"] if q["category"] == category_id]


def by_status(status: str) -> List[Dict]:
    return [q for q in FAQ["questions"] if q["status"] == status]


def get(question_id: str) -> Optional[Dict]:
    return next((q for q in FAQ["questions"] if q["id"] == question_id), None)


def search(query: str, limit: int = 5) -> List[Dict]:
    """Keyword search. Matches in the question count three times as much as matches in the answer."""
    terms = tokenize(query)
    if not terms:
        return []
    scored = []
    for index, q in enumerate(FAQ["questions"]):
        q_words, a_words = tokenize(q["question"]), tokenize(q["answer"])
        score = sum(3 * q_words.count(t) + a_words.count(t) for t in terms)
        if score > 0:
            scored.append((-score, index, q))
    scored.sort(key=lambda s: (s[0], s[1]))
    return [q for _, _, q in scored[:limit]]


def format_answer(q: Dict) -> str:
    """Plain-text rendering of one answer with its label, source and date."""
    label = STATUS_LABELS[q["status"]]["label"]
    return f"{q['question']}\n{q['answer']}\n[{label} · {q['source']} · last checked {q['last_checked']}]"
