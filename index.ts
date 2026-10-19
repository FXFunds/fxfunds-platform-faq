#!/usr/bin/env node
/**
 * FXFunds Platform FAQ
 * Search and read the FXFunds Platform FAQ. Every answer carries a verification
 * status, a source and a last-checked date. Works offline; no network calls.
 * Built by FXFunds — https://fxfunds.com/
 */

export type Status = "verified" | "self-described" | "unverified" | "not-located" | "guidance";

export interface Question {
  id: string;
  category: string;
  question: string;
  answer: string;
  status: Status;
  source: string;
  last_checked: string;
}

export interface Category {
  id: string;
  name: string;
  count: number;
}

interface FaqData {
  title: string;
  official_website: string;
  last_checked: string;
  status_labels: Record<Status, { label: string; meaning: string }>;
  categories: { id: string; name: string }[];
  questions: Question[];
}

// eslint-disable-next-line @typescript-eslint/no-var-requires
const data: FaqData = require("./fxfunds_platform_faq/faq.json");

export const FAQ: Readonly<FaqData> = data;
export const STATUS_LABELS = data.status_labels;
export const LAST_CHECKED = data.last_checked;

const STOPWORDS = new Set([
  "a", "an", "and", "are", "as", "at", "be", "can", "do", "does", "for", "from", "how", "i", "in", "is",
  "it", "my", "of", "on", "or", "the", "to", "what", "where", "which", "who", "why", "with", "fxfunds",
]);

export function tokenize(text: string): string[] {
  return text.toLowerCase().split(/[^a-z0-9]+/).filter((w) => w.length >= 2 && !STOPWORDS.has(w));
}

/** All questions, in FAQ order. */
export function all(): Question[] {
  return [...data.questions];
}

/** Categories with their question counts. */
export function categories(): Category[] {
  return data.categories.map((c) => ({ ...c, count: data.questions.filter((q) => q.category === c.id).length }));
}

export function byCategory(categoryId: string): Question[] {
  return data.questions.filter((q) => q.category === categoryId);
}

export function byStatus(status: Status): Question[] {
  return data.questions.filter((q) => q.status === status);
}

export function get(id: string): Question | undefined {
  return data.questions.find((q) => q.id === id);
}

/** Keyword search. Matches in the question count three times as much as matches in the answer. */
export function search(query: string, limit = 5): Question[] {
  const terms = tokenize(query);
  if (!terms.length) return [];
  const scored = data.questions.map((q, index) => {
    const qWords = tokenize(q.question);
    const aWords = tokenize(q.answer);
    let score = 0;
    for (const t of terms) {
      score += 3 * qWords.filter((w) => w === t).length + aWords.filter((w) => w === t).length;
    }
    return { q, score, index };
  });
  return scored
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score || a.index - b.index)
    .slice(0, limit)
    .map((s) => s.q);
}

/** Plain-text rendering of one answer with its label, source and date. */
export function format(q: Question): string {
  return `${q.question}\n${q.answer}\n[${data.status_labels[q.status].label} · ${q.source} · last checked ${q.last_checked}]`;
}

function main(): void {
  const [cmd, ...rest] = process.argv.slice(2);
  const json = rest.includes("--json");
  const args = rest.filter((a) => a !== "--json");
  const out = (items: Question[]) => {
    if (json) { console.log(JSON.stringify(items, null, 2)); return; }
    if (!items.length) { console.log("No matching questions."); return; }
    console.log(items.map(format).join("\n\n"));
  };

  switch (cmd) {
    case "search": out(search(args.join(" "))); break;
    case "category": out(byCategory(args[0] ?? "")); break;
    case "status": out(byStatus((args[0] ?? "") as Status)); break;
    case "show": { const q = get(args[0] ?? ""); out(q ? [q] : []); break; }
    case "all": out(all()); break;
    default: {
      console.log(`\n${data.title} — ${data.questions.length} questions, last checked ${data.last_checked}`);
      console.log("=".repeat(60));
      for (const c of categories()) console.log(`  ${c.id.padEnd(10)} ${c.name} (${c.count})`);
      console.log("\nUsage:");
      console.log('  fxfunds-faq search "withdrawal fees"');
      console.log("  fxfunds-faq category payments");
      console.log("  fxfunds-faq status not-located");
      console.log("  fxfunds-faq show faq-04");
      console.log("  fxfunds-faq all [--json]");
      console.log(`\nInformational only, not financial advice. Official website: ${data.official_website}\n`);
    }
  }
}

if (require.main === module) main();
