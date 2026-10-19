"""Consistency and behaviour tests for the FXFunds Platform FAQ.
fxfunds_platform_faq/faq.json is the single source; everything else must match it."""
import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import fxfunds_platform_faq as faq

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "fxfunds_platform_faq" / "faq.json").read_text(encoding="utf-8"))
QUESTIONS = DATA["questions"]
STATUSES = set(DATA["status_labels"])
CATEGORIES = {c["id"]: c["name"] for c in DATA["categories"]}
PAGES = {
    "platform": "platform.md", "trading": "trading-and-markets.md", "payments": "deposits-and-withdrawals.md",
    "crypto": "crypto-and-stablecoins.md", "security": "security-and-risk.md", "about": "about-this-faq.md",
}
QUERIES = ["withdrawal fees", "network", "regulated", "leverage", "USDT confirmations", "password security", "xyz"]


def test_faq_structure():
    ids = [q["id"] for q in QUESTIONS]
    assert len(ids) == len(set(ids)) == 24
    for q in QUESTIONS:
        assert q["status"] in STATUSES, q["id"]
        assert q["category"] in CATEGORIES, q["id"]
        assert q["question"].endswith("?"), q["id"]
        assert q["answer"] and q["source"] and q["last_checked"], q["id"]


def test_csv_matches_json():
    with open(ROOT / "dataset" / "fxfunds_platform_faq.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(QUESTIONS)
    for row, q in zip(rows, QUESTIONS):
        for key in ("id", "category", "question", "answer", "status", "source", "last_checked"):
            assert row[key] == q[key], (q["id"], key)
        assert row["category_name"] == CATEGORIES[q["category"]]
        assert row["status_label"] == DATA["status_labels"][q["status"]]["label"]


def test_structured_data_matches_json():
    schema = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))
    assert schema["@type"] == "FAQPage"
    pairs = [(e["name"], e["acceptedAnswer"]["text"]) for e in schema["mainEntity"]]
    assert pairs == [(q["question"], q["answer"]) for q in QUESTIONS]


def test_readme_and_docs_contain_every_answer():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for q in QUESTIONS:
        assert q["question"] in readme and q["answer"] in readme, q["id"]
        page = (ROOT / "docs" / PAGES[q["category"]]).read_text(encoding="utf-8")
        assert q["question"] in page and q["answer"] in page, q["id"]


def test_python_api():
    assert len(faq.all_questions()) == 24
    assert sum(c["count"] for c in faq.categories()) == 24
    assert faq.get("faq-04")["status"] == "not-located"
    assert faq.get("nope") is None
    assert {q["id"] for q in faq.by_status("unverified")} == {"faq-10", "faq-15"}
    assert faq.search("withdrawal fees")[0]["id"] == "faq-11"
    assert faq.search("the and of") == []
    assert "last checked" in faq.format_answer(faq.get("faq-01"))


def test_python_cli():
    out = subprocess.run([sys.executable, "-m", "fxfunds_platform_faq", "show", "faq-04", "--json"],
                         capture_output=True, text=True, check=True).stdout
    assert json.loads(out)[0]["id"] == "faq-04"


@pytest.mark.skipif(shutil.which("node") is None or not (ROOT / "index.js").exists(),
                    reason="Build the Node.js package first: npm ci && npm run build")
def test_node_matches_python():
    script = ("const f=require('./index.js');const qs=JSON.parse(process.argv[1]);"
              "console.log(JSON.stringify({search:qs.map(q=>f.search(q).map(x=>x.id)),"
              "cats:f.categories().map(c=>[c.id,c.count]),unverified:f.byStatus('unverified').map(q=>q.id)}))")
    out = subprocess.run(["node", "-e", script, json.dumps(QUERIES)], cwd=ROOT,
                         capture_output=True, text=True, check=True).stdout
    node = json.loads(out)
    assert node["search"] == [[q["id"] for q in faq.search(s)] for s in QUERIES]
    assert node["cats"] == [[c["id"], c["count"]] for c in faq.categories()]
    assert node["unverified"] == [q["id"] for q in faq.by_status("unverified")]
