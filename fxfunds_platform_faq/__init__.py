"""FXFunds Platform FAQ.

A searchable database of questions people ask about FXFunds. Type a question
the way you would search it ("is fxfunds legit", "withdrawal time") and get
the best-matching answers. Makes no network calls.
"""

import json
import re
from importlib import resources

__version__ = "2.0.0"

FAQ = json.loads(resources.files(__package__).joinpath("faq.json").read_text(encoding="utf-8"))

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "do", "does", "did", "can", "could",
    "will", "would", "should", "i", "me", "my", "you", "your", "it", "its", "of", "to", "in",
    "on", "for", "with", "and", "or", "at", "by", "from", "about", "what", "which", "who",
    "how", "why", "where", "when", "this", "that", "there", "any", "fxfunds", "fxfund",
    "please", "tell", "know",
}


def normalize(text):
    """Lowercase and strip punctuation, keeping letters, digits, '-', '/' and '.'."""
    text = re.sub(r"[^a-z0-9\-/. ]+", " ", text.lower())
    return re.sub(r"\s+", " ", text).strip(" .")


def tokens(query):
    """Meaningful words from a query, stopwords removed and simple plurals stemmed."""
    out = []
    for w in normalize(query).split():
        w = w.strip(".")
        if not w or w in STOPWORDS:
            continue
        if len(w) > 4 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.append(w)
    return out


def _has(tok, text):
    return re.search(rf"(?<![a-z0-9]){re.escape(tok)}(s|es)?(?![a-z0-9])", text) is not None


def score(entry, query):
    """Relevance score of one FAQ entry for a query (0 = no match)."""
    nq = normalize(query)
    s = 0
    searches = [x.lower() for x in entry["searches"]]
    if nq in searches:
        s += 20
    elif len(nq) >= 6 and any(x in nq or nq in x for x in searches):
        s += 8
    keywords = [k.lower() for k in entry["keywords"]]
    question, answer = entry["question"].lower(), entry["answer"].lower()
    for tok in tokens(query):
        if any(_has(tok, k) for k in keywords):
            s += 3
        if _has(tok, question):
            s += 2
        elif _has(tok, answer):
            s += 1
    return s


def ask(query, limit=3):
    """Return the best-matching FAQ entries for a question, best first."""
    ranked = sorted(((score(e, query), e) for e in FAQ), key=lambda p: -p[0])
    return [e for sc, e in ranked if sc > 0][:limit]


def get(faq_id):
    """Return one entry by id (e.g. 'FAQ-07' or '7'), or None."""
    faq_id = str(faq_id).upper()
    if faq_id.isdigit():
        faq_id = f"FAQ-{int(faq_id):02d}"
    return next((e for e in FAQ if e["id"] == faq_id), None)


def categories():
    """Return category names in order."""
    return list(dict.fromkeys(e["category"] for e in FAQ))


def by_category(name):
    """Return entries in a category (case-insensitive substring)."""
    n = name.lower()
    return [e for e in FAQ if n in e["category"].lower()]


def all_questions():
    """Return every entry."""
    return list(FAQ)


__all__ = ["ask", "get", "categories", "by_category", "all_questions", "score", "tokens", "normalize", "__version__"]
