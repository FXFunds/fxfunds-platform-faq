"""Regenerate the dataset CSV, docs FAQ page, README FAQ section and schema FAQPage from faq.json.

    python tools/generate.py           write generated files
    python tools/generate.py --check   exit 1 if any generated file is stale
"""

import csv
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAQ = json.loads((ROOT / "fxfunds_platform_faq/faq.json").read_text(encoding="utf-8"))
FIELDS = ["id", "category", "question", "answer", "keywords", "searches"]


def faq_csv():
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    for e in FAQ:
        w.writerow({**{k: e[k] for k in FIELDS[:4]}, "keywords": "; ".join(e["keywords"]), "searches": "; ".join(e["searches"])})
    return buf.getvalue()


def faq_markdown(level):
    out, current = [], None
    for e in FAQ:
        if e["category"] != current:
            current = e["category"]
            out.append(f"{level} {current}\n")
        out.append(f"**{int(e['id'].split('-')[1])}. {e['question']}**\n")
        out.append(f"{e['answer']}\n")
    return "\n".join(out).rstrip()


def categories_table():
    counts = {}
    for e in FAQ:
        counts[e["category"]] = counts.get(e["category"], 0) + 1
    lines = ["| Category | Questions |", "|----------|-----------|"]
    lines += [f"| {c} | {n} |" for c, n in counts.items()]
    return "\n".join(lines)


def replace_block(text, name, body):
    pattern = re.compile(rf"(<!-- {name}:START -->\n).*?(<!-- {name}:END -->)", re.S)
    if not pattern.search(text):
        raise SystemExit(f"marker {name} not found")
    return pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text)


def readme():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    text = replace_block(text, "CATEGORIES", categories_table())
    return replace_block(text, "FAQ", faq_markdown("###"))


def schema():
    data = json.loads((ROOT / "schema.json").read_text(encoding="utf-8"))
    for node in data["@graph"]:
        if node["@type"] == "FAQPage":
            node["mainEntity"] = [
                {"@type": "Question", "name": e["question"], "acceptedAnswer": {"@type": "Answer", "text": e["answer"]}}
                for e in FAQ
            ]
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def outputs():
    return {
        ROOT / "dataset/fxfunds_platform_faq.csv": faq_csv(),
        ROOT / "docs/faq.md": f"# FXFunds FAQ\n\n{faq_markdown('##')}\n",
        ROOT / "README.md": readme(),
        ROOT / "schema.json": schema(),
    }


def main():
    check = "--check" in sys.argv
    stale = []
    for path, content in outputs().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            stale.append(path.relative_to(ROOT))
            if not check:
                path.write_text(content, encoding="utf-8")
    if check and stale:
        print("Stale generated files:", *stale, sep="\n  ")
        return 1
    print("Up to date." if not stale else f"Wrote {len(stale)} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
