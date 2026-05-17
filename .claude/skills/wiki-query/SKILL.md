---
name: wiki-query
description: Answer a question against the wiki — read the index, drill into relevant pages, synthesize a precise answer with citations, and optionally file the answer back as a new wiki page. Use whenever the user asks an ML question against this vault, says "what does the wiki say about X", "synthesize X", "compare X and Y from the wiki", or asks any substantive question that the wiki could plausibly answer.
---

## Pre-flight

- [ ] Read `.claude/role.md`
- [ ] Read `wiki/index.md` — the by-tag section is the entry point for concept queries.

# wiki-query

Workflow for answering a question against the wiki. The key idea: **good answers can be filed back into the wiki as new pages** so future queries get faster and richer.

---

## Checklist (mirror as TodoWrite tasks)

1. **Restate the question.** One sentence, in your own words, so any ambiguity surfaces before you go searching.
2. **Run the search strategy** (see Search strategy section below).
3. **Detect gaps.** Note any concepts the question depends on that don't have pages yet — these become candidate ingests or stubs.
4. **Synthesize the answer.** Cite by `[[wiki-link]]`. Distinguish what's in the wiki from what you're inferring.
5. **Decide on filing.** If the answer is substantive and reusable, propose filing it back into the wiki. Otherwise skip and just append a log entry.
6. **Append a log entry** for the query (one-liner — even if you didn't file a page).

---

## Step 1 — Restate the question

Rewrite the user's question in one precise sentence. Examples:

- User: "what's the deal with attention scaling?" → Restate: "Why is the dot-product attention score divided by √d_k in the Transformer formulation?"
- User: "how does Adam differ from SGD?" → Restate: "What does Adam compute differently from vanilla SGD, and what failure modes does that change introduce or remove?"

If the restated question is ambiguous in a load-bearing way, ask one clarifying question — but only one. Otherwise pick the most charitable interpretation and proceed.

---

## Search strategy

1. **Parse the question** — identify the concept(s) the user is asking about (e.g., "How does RoPE handle long contexts?" → concept = `positional-encoding`, secondary = `attention`).
2. **Match tags** — open `wiki/index.md`, find the «By tag» section, locate the line for the relevant tag(s). It lists every breakdown that mentions the concept.
3. **Read relevant breakdowns** — open the matching `wiki/<kind>/<slug>.md` pages in priority order: papers that introduce the concept first, then lectures, then clips, then knowledge-sharings.
4. **Synthesize the answer** — combine findings across pages, cite each claim with `[[<kind>/<slug>]]`. State which page contributed which piece. If sources disagree, note both positions with attribution.
5. **Suggest next reads** — if the user might benefit from a related concept, end with «Если хочешь глубже — см. [[<related-page>]]».

Skim `wiki/log.md` if you want recent context — e.g., what was last ingested on this topic, or what's been flagged as contradictory.

---

## Step 3 — Detect gaps

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

## Step 4 — Synthesize

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

## Step 5 — Decide on filing

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

- Choose the right target: usually extend an existing breakdown (add a new subsection), or update a related page's `Связанные разборы`. Creating a whole new page from a query alone is rare — prefer adding context within existing breakdowns.
- Use the standard templates and frontmatter from `_shared/page-templates.md`.
- Update `wiki/index.md` accordingly.
- Note in the edit comment or log entry that the content was created from a query.
- Never create new source-kind pages without a raw source to back them.

Ask the user once before filing:

```
This answer feels reusable. Want me to file it as [[topic/x-vs-y]] (new) /
extend [[ml_concepts/x]] / leave as chat? (default: file as new topic page)
```

If the user has asked you to work without stopping for clarifying questions, default to filing reusable answers and announce what you filed.

If a previous resolution applies the same way again (e.g., you re-derive a result already on a page), don't re-file — just cite.

---

## Step 6 — Log entry

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
