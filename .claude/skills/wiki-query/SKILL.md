---
name: wiki-query
description: Answer a question against the wiki — read the index, drill into relevant pages, synthesize a precise answer with citations, and optionally file the answer back as a new wiki page. Use whenever the user asks an ML question against this vault, says "what does the wiki say about X", "synthesize X", "compare X and Y from the wiki", or asks any substantive question that the wiki could plausibly answer.
---

# wiki-query

Workflow for answering a question against the wiki. The key idea: **good answers can be filed back into the wiki as new pages** so future queries get faster and richer.

---

## Checklist (mirror as TodoWrite tasks)

1. **Restate the question.** One sentence, in your own words, so any ambiguity surfaces before you go searching.
2. **Read `wiki/index.md`.** Pick candidate pages by skimming the one-line summaries.
3. **Drill into candidate pages.** Read the relevant concept / method / topic / source pages in full.
4. **Detect gaps.** Note any concepts the question depends on that don't have pages yet — these become candidate ingests or stubs.
5. **Synthesize the answer.** Cite by `[[wiki-link]]`. Distinguish what's in the wiki from what you're inferring.
6. **Decide on filing.** If the answer is substantive and reusable, propose filing it back into the wiki. Otherwise skip and just append a log entry.
7. **Append a log entry** for the query (one-liner — even if you didn't file a page).

---

## Step 1 — Restate the question

Rewrite the user's question in one precise sentence. Examples:

- User: "what's the deal with attention scaling?" → Restate: "Why is the dot-product attention score divided by √d_k in the Transformer formulation?"
- User: "how does Adam differ from SGD?" → Restate: "What does Adam compute differently from vanilla SGD, and what failure modes does that change introduce or remove?"

If the restated question is ambiguous in a load-bearing way, ask one clarifying question — but only one. Otherwise pick the most charitable interpretation and proceed.

---

## Step 2 — Read the index

Open `wiki/index.md`. Read every line. Mentally tag candidates:

- Direct hits: pages whose one-line summary matches the question.
- Indirect hits: pages that are likely to be linked from the direct hits.
- Open questions: any `questions/` pages that overlap.

Keep the candidate list short (5–10 pages). If the candidate list explodes, the question is probably too broad — narrow it before drilling.

---

## Step 3 — Drill in

Read each candidate page in full. Follow `[[wiki-links]]` when a page references a concept central to the question. Stop expanding once you have enough material to answer; don't fan out to the whole graph.

Skim `wiki/log.md` if you want recent context — e.g., what was last ingested on this topic, or what's been flagged as contradictory.

---

## Step 4 — Detect gaps

As you drill, you'll usually find one of three states:

| State | Action |
|---|---|
| The wiki answers the question well | Synthesize from wiki content |
| The wiki has scattered pieces but no synthesis | Synthesize, **and consider filing** the result as a new page |
| The wiki doesn't cover this | Say so plainly. Suggest sources to ingest or stub pages to create. Don't bluff. |

When the wiki has gaps:

- Surface them as `[[stub-link]]` targets in your answer.
- Suggest concrete next steps: "would help to ingest X", "consider a stub page for [[concept-y]]".

---

## Step 5 — Synthesize

Write the answer for the user. Follow the same quality bar as wiki pages:

- **Definitions before claims.** State what the question is about, then the answer.
- **Cite specifically.** Every non-trivial claim ends in a `[[wiki-link]]` to the page it came from. If the claim came from multiple pages, list both.
- **Distinguish wiki content from inference.** If you're going beyond what the wiki says (e.g., synthesising a comparison the wiki doesn't make explicitly), say so with a brief "Inferring beyond the wiki:" tag. Don't invent results.
- **Match the form to the question.** A definition deserves a paragraph. A comparison deserves a table. A derivation deserves equations. Don't bullet-point everything reflexively.

Format suggestions:

- **Definition / explanation** → a few short paragraphs.
- **Comparison** → a table with rows for each item and columns for the dimensions of comparison.
- **Derivation / proof sketch** → numbered steps with equations.
- **List of things** → a bulleted list, with each bullet linking to a wiki page.

Use LaTeX for math (`$...$`, `$$...$$`).

---

## Step 6 — Decide on filing

Ask yourself: would this answer be useful to find again? Will future questions reference it? If yes, propose filing it.

Strong file-back candidates:

- Cross-concept comparisons not currently in the wiki.
- Derivations or worked examples that fill a gap on an existing page.
- Synthesised claims that span multiple sources (e.g., "across these 3 papers, the consensus on warmup is X").
- Newly-resolved questions that match an existing `questions/` page.

Weak / skip candidates:

- Pure restatements of existing pages.
- One-off clarifications that don't generalise.
- Conversational answers that don't add structure.

If filing:

- Choose the page type: usually `concept` (for new ideas), `topic` (for cross-cutting syntheses), or update an existing page (when the answer belongs as a new section there).
- Use the standard templates and frontmatter from `CLAUDE.md`.
- Update `wiki/index.md`.
- Reference the original sources via `[[sources/...]]` links.
- Note in the new page that it was created from a query (don't bury this — future you wants to know).

Ask the user once before filing:

```
This answer feels reusable. Want me to file it as [[topic/x-vs-y]] (new) /
extend [[ml_concepts/x]] / leave as chat? (default: file as new topic page)
```

If the user has asked you to work without stopping for clarifying questions, default to filing reusable answers and announce what you filed.

If a previous resolution applies the same way again (e.g., you re-derive a result already on a page), don't re-file — just cite.

---

## Step 7 — Log entry

Always append a log entry, regardless of whether you filed a page:

```markdown
## [YYYY-MM-DD] query | {short restated question}

- **Question:** {restated question}
- **Pages read:** [[a]], [[b]], [[c]]
- **Filed:** [[new-page]] (or "no — answered inline")
- **Gaps surfaced:** {concepts mentioned that don't have pages yet, or "none"}
```

---

## When the wiki is too small to help

In the early days the wiki will be sparse. If a question lands and there's nothing relevant in the index, say so plainly:

```
The wiki doesn't cover this yet. Closest pages:
- [[a]] (tangentially related: ...)

To answer this well, consider ingesting:
- {specific source suggestion}
- {another}

Want me to answer from general knowledge anyway, or hold until we've fed in
relevant sources?
```

Do not pretend the wiki said something it didn't. Citing absent pages is worse than citing none.

---

## What this skill is NOT

- Not an ingest workflow. If the user is handing you a source, use `wiki-ingest`.
- Not an opinion column. The wiki's voice is technical and specific. Personal takes that aren't supported by sources belong in `raw/scratch/` until they're substantiated.
- Not a search engine. You can read `wiki/index.md` and follow links — that's enough at this scale. If the wiki outgrows that, we'll add tooling.
