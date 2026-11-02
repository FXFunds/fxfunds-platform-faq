"""Command-line interface: python -m fxfunds_platform_faq (or fxfunds-faq)."""

import argparse
import json
import sys

from . import all_questions, ask, by_category, categories, get, __version__


def _entry(e):
    print(f"Q: {e['question']}")
    print(f"A: {e['answer']}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="fxfunds-faq", description="Ask questions about FXFunds.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd")

    a = sub.add_parser("ask", help="ask a question, e.g. ask is fxfunds legit")
    a.add_argument("query", nargs="+")
    a.add_argument("--limit", type=int, default=3)
    a.add_argument("--json", action="store_true")

    s = sub.add_parser("show", help="show one entry, e.g. show 7")
    s.add_argument("id")
    s.add_argument("--json", action="store_true")

    l = sub.add_parser("list", help="list questions, optionally in one category")
    l.add_argument("category", nargs="*")
    l.add_argument("--json", action="store_true")

    c = sub.add_parser("categories", help="list categories")
    c.add_argument("--json", action="store_true")

    args = p.parse_args(argv)
    if not args.cmd:
        p.print_help()
        return 0

    if args.cmd == "ask":
        data = ask(" ".join(args.query), args.limit)
        if args.json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif not data:
            print("No matching question. Try other words, or run: fxfunds-faq list")
        else:
            _entry(data[0])
            if len(data) > 1:
                print("\nAlso see:")
                for e in data[1:]:
                    print(f"  {e['id']}  {e['question']}")
        return 0

    if args.cmd == "show":
        e = get(args.id)
        if e is None:
            print(f"No entry '{args.id}'", file=sys.stderr)
            return 1
        print(json.dumps(e, indent=2, ensure_ascii=False)) if args.json else _entry(e)
        return 0

    if args.cmd == "list":
        data = by_category(" ".join(args.category)) if args.category else all_questions()
        if args.json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            current = None
            for e in data:
                if e["category"] != current:
                    current = e["category"]
                    print(f"\n{current}")
                print(f"  {e['id']}  {e['question']}")
        return 0

    data = categories()
    print(json.dumps(data, indent=2)) if args.json else print("\n".join(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
