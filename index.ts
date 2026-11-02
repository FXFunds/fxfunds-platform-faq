#!/usr/bin/env node
/**
 * FXFunds Platform FAQ — Node.js library and CLI.
 * A searchable database of questions people ask about FXFunds. Makes no network calls.
 */
import { readFileSync } from "fs";
import { join } from "path";

export interface FaqEntry {
  id: string;
  category: string;
  question: string;
  answer: string;
  keywords: string[];
  searches: string[];
}

export const FAQ: FaqEntry[] = JSON.parse(
  readFileSync(join(__dirname, "..", "fxfunds_platform_faq", "faq.json"), "utf8"),
);

export const STOPWORDS = new Set([
  "a", "an", "the", "is", "are", "was", "were", "be", "do", "does", "did", "can", "could",
  "will", "would", "should", "i", "me", "my", "you", "your", "it", "its", "of", "to", "in",
  "on", "for", "with", "and", "or", "at", "by", "from", "about", "what", "which", "who",
  "how", "why", "where", "when", "this", "that", "there", "any", "fxfunds", "fxfund",
  "please", "tell", "know",
]);

/** Lowercase and strip punctuation, keeping letters, digits, '-', '/' and '.'. */
export function normalize(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9\-/. ]+/g, " ").replace(/\s+/g, " ").replace(/^[ .]+|[ .]+$/g, "");
}

/** Meaningful words from a query, stopwords removed and simple plurals stemmed. */
export function tokens(query: string): string[] {
  const out: string[] = [];
  for (let w of normalize(query).split(" ")) {
    w = w.replace(/^\.+|\.+$/g, "");
    if (!w || STOPWORDS.has(w)) continue;
    if (w.length > 4 && w.endsWith("s") && !w.endsWith("ss")) w = w.slice(0, -1);
    out.push(w);
  }
  return out;
}

const esc = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const has = (tok: string, text: string) => new RegExp(`(?<![a-z0-9])${esc(tok)}(s|es)?(?![a-z0-9])`).test(text);

/** Relevance score of one FAQ entry for a query (0 = no match). */
export function score(entry: FaqEntry, query: string): number {
  const nq = normalize(query);
  let s = 0;
  const searches = entry.searches.map((x) => x.toLowerCase());
  if (searches.includes(nq)) s += 20;
  else if (nq.length >= 6 && searches.some((x) => x.includes(nq) || nq.includes(x))) s += 8;
  const keywords = entry.keywords.map((k) => k.toLowerCase());
  const question = entry.question.toLowerCase(), answer = entry.answer.toLowerCase();
  for (const tok of tokens(query)) {
    if (keywords.some((k) => has(tok, k))) s += 3;
    if (has(tok, question)) s += 2;
    else if (has(tok, answer)) s += 1;
  }
  return s;
}

/** Best-matching FAQ entries for a question, best first. */
export function ask(query: string, limit = 3): FaqEntry[] {
  return FAQ.map((e) => [score(e, query), e] as const)
    .filter(([sc]) => sc > 0)
    .sort((a, b) => b[0] - a[0])
    .slice(0, limit)
    .map(([, e]) => e);
}

/** One entry by id ('FAQ-07' or '7'). */
export function get(id: string | number): FaqEntry | undefined {
  let key = String(id).toUpperCase();
  if (/^\d+$/.test(key)) key = `FAQ-${String(Number(key)).padStart(2, "0")}`;
  return FAQ.find((e) => e.id === key);
}

export const categories = (): string[] => [...new Set(FAQ.map((e) => e.category))];
export const byCategory = (name: string): FaqEntry[] =>
  FAQ.filter((e) => e.category.toLowerCase().includes(name.toLowerCase()));
export const allQuestions = (): FaqEntry[] => [...FAQ];

// ---------------------------------------------------------------- CLI

const USAGE = `fxfunds-faq — ask questions about FXFunds

  fxfunds-faq ask is fxfunds legit     best answer + related questions
  fxfunds-faq show 7                   one entry
  fxfunds-faq list [category]          all questions, or one category
  fxfunds-faq categories               category names
  add --json for JSON output, --limit N to change the number of matches`;

const printEntry = (e: FaqEntry) => console.log(`Q: ${e.question}\nA: ${e.answer}`);

export function cli(argv: string[]): number {
  let json = false;
  let limit = 3;
  const args: string[] = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--json") json = true;
    else if (argv[i] === "--limit") limit = Number(argv[++i]) || 3;
    else args.push(argv[i]);
  }
  const [cmd, ...rest] = args;
  const out = (d: unknown) => console.log(JSON.stringify(d, null, 2));

  switch (cmd) {
    case "ask": {
      const d = ask(rest.join(" "), limit);
      if (json) out(d);
      else if (!d.length) console.log("No matching question. Try other words, or run: fxfunds-faq list");
      else {
        printEntry(d[0]);
        if (d.length > 1) {
          console.log("\nAlso see:");
          d.slice(1).forEach((e) => console.log(`  ${e.id}  ${e.question}`));
        }
      }
      return 0;
    }
    case "show": {
      const e = get(rest[0] || "");
      if (!e) { console.error(`No entry '${rest[0]}'`); return 1; }
      json ? out(e) : printEntry(e);
      return 0;
    }
    case "list": {
      const d = rest.length ? byCategory(rest.join(" ")) : allQuestions();
      if (json) { out(d); return 0; }
      let current = "";
      for (const e of d) {
        if (e.category !== current) { current = e.category; console.log(`\n${current}`); }
        console.log(`  ${e.id}  ${e.question}`);
      }
      return 0;
    }
    case "categories":
      json ? out(categories()) : console.log(categories().join("\n"));
      return 0;
    case undefined:
    case "-h":
    case "--help":
    case "help":
      console.log(USAGE);
      return 0;
    default:
      console.error(USAGE);
      return 2;
  }
}

if (require.main === module) {
  process.exitCode = cli(process.argv.slice(2));
}
