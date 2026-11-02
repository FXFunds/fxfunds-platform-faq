"""Database consistency and search behaviour tests."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

import fxfunds_platform_faq as fx
from fxfunds_platform_faq.__main__ import main

ROOT = Path(__file__).resolve().parent.parent


def test_generated_files_up_to_date():
    r = subprocess.run([sys.executable, str(ROOT / "tools/generate.py"), "--check"], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr


def test_database_shape():
    entries = fx.all_questions()
    assert [e["id"] for e in entries] == [f"FAQ-{i:02d}" for i in range(1, 39)]
    for e in entries:
        assert set(e) == {"id", "category", "question", "answer", "keywords", "searches"}
        assert e["question"].endswith("?") and e["answer"]
        assert e["keywords"] and e["searches"]
        assert all(s == s.lower() for s in e["searches"])
    assert len(fx.categories()) == 7
    questions = [e["question"] for e in entries]
    assert len(set(questions)) == len(questions)


def test_search_phrases_find_their_entry():
    for e in fx.all_questions():
        for s in e["searches"]:
            assert fx.ask(s)[0]["id"] == e["id"], f"{s!r} did not return {e['id']}"


@pytest.mark.parametrize("query, expected", [
    ("is fxfunds legit", "FAQ-02"),
    ("Is FXFunds a scam?", "FAQ-02"),
    ("how long does withdrawal take", "FAQ-26"),
    ("SEC", "FAQ-07"),
    ("is my money safe", "FAQ-16"),
    ("trc20", "FAQ-35"),
    ("customer support", "FAQ-31"),
    ("what is fxfunds", "FAQ-01"),
    ("is it regulated", "FAQ-09"),
    ("how to deposit", "FAQ-23"),
    ("bitcoin", "FAQ-19"),
    ("fake recruitment message", "FAQ-32"),
])
def test_ask(query, expected):
    assert fx.ask(query)[0]["id"] == expected


def test_ask_no_match_and_limit():
    assert fx.ask("xyzzy") == []
    assert fx.ask("") == []
    assert len(fx.ask("withdrawal", limit=2)) == 2


def test_get_and_categories():
    assert fx.get("7")["id"] == "FAQ-07"
    assert fx.get("faq-23")["id"] == "FAQ-23"
    assert fx.get("99") is None
    assert len(fx.by_category("security")) == 6


def test_faq_text_numbered_in_readme():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for e in fx.all_questions():
        n = int(e["id"].split("-")[1])
        assert f"**{n}. {e['question']}**" in readme
        assert e["answer"] in readme


def test_cli(capsys):
    assert main(["ask", "is", "fxfunds", "legit"]) == 0
    assert "Q: Is FXFunds a legitimate company?" in capsys.readouterr().out
    assert main(["show", "7", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["id"] == "FAQ-07"
    assert main(["ask", "xyzzy"]) == 0
    assert "No matching question" in capsys.readouterr().out
    assert main(["show", "99"]) == 1
