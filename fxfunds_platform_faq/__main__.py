"""Command-line interface: fxfunds-faq / python -m fxfunds_platform_faq"""
import json
import sys

from . import FAQ, all_questions, by_category, by_status, categories, format_answer, get, search


def main(argv=None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    as_json = "--json" in argv
    args = [a for a in argv if a != "--json"]
    cmd, rest = (args[0], args[1:]) if args else (None, [])

    def out(items):
        if as_json:
            print(json.dumps(items, indent=2, ensure_ascii=False))
        elif not items:
            print("No matching questions.")
        else:
            print("\n\n".join(format_answer(q) for q in items))

    if cmd == "search":
        out(search(" ".join(rest)))
    elif cmd == "category":
        out(by_category(rest[0] if rest else ""))
    elif cmd == "status":
        out(by_status(rest[0] if rest else ""))
    elif cmd == "show":
        q = get(rest[0] if rest else "")
        out([q] if q else [])
    elif cmd == "all":
        out(all_questions())
    else:
        print(f"\n{FAQ['title']} — {len(FAQ['questions'])} questions, last checked {FAQ['last_checked']}")
        print("=" * 60)
        for c in categories():
            print(f"  {c['id']:<10} {c['name']} ({c['count']})")
        print("\nUsage:")
        print('  fxfunds-faq search "withdrawal fees"')
        print("  fxfunds-faq category payments")
        print("  fxfunds-faq status not-located")
        print("  fxfunds-faq show faq-04")
        print("  fxfunds-faq all [--json]")
        print(f"\nInformational only, not financial advice. Official website: {FAQ['official_website']}\n")


if __name__ == "__main__":
    main()
