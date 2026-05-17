# CLAUDE.md — ML Notes Wiki

This directory is a personal LLM-maintained wiki for building structured understanding of machine learning. It follows the LLM Wiki pattern (Karpathy): the LLM reads raw sources, extracts knowledge, and incrementally builds a network of interlinked markdown pages. The wiki compounds over time — every new source enriches existing pages instead of being re-derived on each query.

**Your role:** you write and maintain `wiki/` entirely. The user curates sources, asks questions, and reviews the result. Do the summarising, cross-referencing, filing, and bookkeeping.

---
## Architecture

Three layers:

| Layer       | Path                           | Who owns it   | Mutability                      |
| ----------- | ------------------------------ | ------------- | ------------------------------- |
| Raw sources | `raw/`                         | The user      | Immutable — read only           |
| Wiki        | `wiki/`                        | You (the LLM) | Read/write                      |
| Schema      | `CLAUDE.md`, `.claude/skills/` | Co-evolved    | Read/write, but discuss changes |
You read from `raw/` and write to `wiki/`. You never modify `raw/`. If you believe a raw document needs correction or annotation, file the correction as a wiki page that links to the source — do not touch the original.

---
## Directory layout

```
ml_notes/
├── CLAUDE.md                     # this file
├── .claude/skills/               # workflows: ingest, query, lint
├── raw/                          # source documents (immutable)
│   ├── papers/                   # arXiv PDFs and similar
│   ├── clips/                    # web articles (Obsidian Web Clipper)
│   ├── scratch/                  # your own notes, half-formed ideas
│   └── lectures/                 # slides, lecture notes, talk transcripts
└── wiki/                         # everything the LLM writes
    ├── index.md                  # catalog of wiki pages
    ├── log.md                    # chronological event log
    ├── ml_concepts/              # ML ideas (one per page)
    ├── math_concepts/            # math foundations — step-by-step walkthroughs
    ├── methods/                  # specific algorithms / techniques
    ├── topics/                   # umbrella areas (links + short framings)
    ├── sources/                  # one page per ingested raw source
    └── questions/                # open questions, things to investigate
```

If a source doesn't fit the existing `raw/` subdirectories, create a new one rather than forcing it into a wrong bucket.

---

## Page taxonomy

| Type       | What it captures                                           | Length          | Examples                                             |
| ---------- | ---------------------------------------------------------- | --------------- | ---------------------------------------------------- |
| `ml_concept`   | An ML idea that exists independently of any one algorithm  | Short to medium | `attention.md`, `dropout.md`, `residual-connection.md` |
| `math_concept` | A math object used by ML — walk through derivations step by step | Medium     | `kl-divergence.md`, `softmax.md`, `jacobian.md`        |
| `method`   | A specific algorithm or technique — usually with code/math | Medium          | `adamw.md`, `flash-attention.md`, `lora.md`          |
| `topic`    | A narrative primer that walks through an area, with inline links into the reference layer | Medium to long  | `optimization.md`, `regularization.md`               |
| `source`   | What you learned from one raw document                     | Short           | `sources/karpathy-makemore-lecture-3.md`             |
| `question` | An open question that hasn't been resolved yet             | Short           | `questions/why-does-lr-warmup-help.md`               |

**Concept pages are the primary unit** — both `ml_concept` and `math_concept`. Methods derive their meaning from concepts (AdamW is a method that implements momentum, decoupled weight decay, and adaptive learning rates — all `ml_concept`s).

ML ideas (mechanisms, training tricks, architectural pieces) go in `ml_concepts/`. Math objects (functions, operations, distance measures, inequalities) go in `math_concepts/`, where they get a step-by-step walkthrough, not a one-line summary. When in doubt, write an `ml_concept` and link out to `math_concept` pages for the math underneath.

---
## Frontmatter

Every wiki page starts with YAML frontmatter. Dataview queries depend on this.

```yaml
---
title: Attention Mechanism
type: ml_concept             # ml_concept | math_concept | method | topic | source | question
tags: [attention, transformers, sequence-models]
created: 2026-05-15
updated: 2026-05-15
sources: 3                   # count of distinct raw sources referenced
status: stub                 # stub | draft | mature
---
```

Field rules:

- `title`: human-readable, capitalised. The filename is the slug (kebab-case).
- `type`: matches the directory.
- `tags`: lowercase, kebab-case, plural where natural (e.g. `transformers` not `transformer`).
- `created` / `updated`: ISO date. Update `updated` whenever you change the page substantively (not for typo fixes).
- `sources`: integer count of distinct raw sources cited on the page. Bump when you add a new citation; do not double-count the same source.
- `status`:
  - `stub` — exists because someone linked to it; minimal content.
  - `draft` — has substantive content from at least one source.
  - `mature` — cross-referenced, multi-source, the synthesis feels stable.

Source pages additionally carry the raw-document path:

```yaml
---
title: "Karpathy — makemore part 3 (activations & gradients)"
type: source
source_path: raw/lectures/karpathy-makemore-3.md
source_kind: lecture          # paper | clip | scratch | lecture | other
source_date: 2022-10-11       # date of the source, not when you ingested it
ingested: 2026-05-15
tags: [initialisation, batch-norm, training-dynamics]
status: draft
---
```

---

## Page templates

Use these as defaults. Deviate when the content demands it. **Prose body is Russian; section headings, frontmatter `title:`, H1, slugs, and tags stay English. See `## Language` below.**

### ML concept page

```markdown
---
{frontmatter}
---

# {Title}

> {few-sentence definition — crisp, no hedging. This is the entry for refresh-mode reading.}

## Motivation

{2–4 paragraphs in motivated build-up voice: name what we want, name the naive
thing, name why it fails, name the workaround this concept introduces. Direct
prose, no Q&A markers, no metaphors. Math when it clarifies.}

## Formal description

{math, pseudocode, or precise prose. Use LaTeX-style $...$ and $$...$$. For
non-trivial math, link out to [[math_concepts/...]] instead of expanding it
inline.}

## Variations and related concepts

- [[ml_concepts/other-concept]] — {one-line relationship}
- [[methods/some-method]] — {how this method instantiates the concept}
- [[math_concepts/some-math]] — {the math underneath}

## Open questions

- [[questions/some-open-question]]
- {or inline if you haven't filed the question as its own page yet}

## Sources

- [[sources/source-page-a]] — {what this source contributed}
- [[sources/source-page-b]] — {what this source contributed}

## Up next

- [[wiki-link]] — {one-line "why this is the natural next step for a reader studying this area"}
```

### Math concept page

The math template differs from the ML template: more careful exposition, fewer shortcuts. The reader struggles with dense math, so unpack every step.

```markdown
---
{frontmatter}
---

# {Title}

> {few-sentence definition — what this math object computes, asserts, or measures}

## Plain-English statement

{What this is, in words. When the math object has a clean motivating story —
what we want, what naive approach fails, how this object solves it — open
with that build-up arc. For pure-math objects without such an arc, just unpack the definition. 
Math notation OK, but introduce each symbol when it first appears. Don't drop into formulas
without naming the variables.}

## Step-by-step

{Walk through the math without compression. Show every intermediate step. If a
step uses another math object, link to it: [[math_concepts/x]]. Tell the
reader what each line does and why — not just what it equals.}

## Worked example

{One concrete numerical example with small numbers. Compute end-to-end so the
reader can verify by hand. For multi-dim objects, show the shapes at each step.}

## Where it shows up in ML

- [[ml_concepts/...]] — {how this math object is used in ML}
- [[methods/...]] — {methods that rely on it}

## Common pitfalls

- {index confusions, sign errors, off-by-one mistakes, dimension mismatches,
  base of log, etc.}

## Sources

- [[sources/...]]
```

### Method page

```markdown
---
{frontmatter}
---

# {Title}

> {few-sentence summary: what problem this method solves and how}

## Motivation

{2–4 paragraphs in motivated build-up voice: what we want this method to do,
what the naive or previous approach fails at, how this method's design
addresses that. Direct prose, no Q&A markers, no metaphors.}

## Problem setting

{when this method applies; what assumptions it makes}

## Algorithm

{pseudocode or explicit equations. Be precise about indices, shapes, and
hyperparameters.}

## Why it works

{the underlying concept(s) it leverages, with [[wiki-links]] to concept pages}

## Properties

- Complexity: {time / memory}
- Hyperparameters: {what to tune, sensible defaults}
- Failure modes: {when it breaks}

## Variants and successors

- [[related-method]] — {one-line delta}

## Sources

- [[sources/...]]

## Up next

- [[methods/successor-or-related-method]] — {what it adds over this one}
- [[topics/parent-topic]] — {how to see this method in the wider area}
```

### Topic page (primer)

Topic pages are *primers*: narrative entry points that walk a reader through an area in motivated build-up voice, with inline links into the reference layer. They are not link maps — the story is in the prose, and reading order is woven into it. The numbered "Reading order (recap)" at the bottom is for scanability only.

```markdown
---
{frontmatter}
---

# {Title}

> {few-sentence framing of the area}

## The setting

{2–4 paragraphs in build-up voice: the problem this area addresses, what makes
it hard, what class of techniques shows up. This is the entry into the story,
not a "scope" disclaimer.}

## Core ideas

{Narrative through the concept pages of the area in reading order. Each
concept is introduced inline with `[[ml_concepts/foo]]` or
`[[math_concepts/foo]]`; the transitions between them explain why one leads to
the next. Build-up voice. Reading order is woven into prose, not stated as a
list here.}

## Methods that grow from these ideas

{Narrative through method pages in reading order, with `[[methods/...]]`
inline. Each method gets a one-paragraph sketch of what it does and what it
adds over the previous one.}

## Open threads

- {unresolved questions, what to ingest next; bullets are fine here}

## Reading order (recap)

1. [[ml_concepts/...]]
2. [[ml_concepts/...]]
3. [[methods/...]]
...

## Reading queue

- {sources to ingest next, even if not yet in raw/}
```

Target length: ~500–1200 words; expand when justified by content. No hard cap.

### Source page

```markdown
---
{frontmatter with source_path, source_kind, source_date, ingested}
---

# {Title}

> {few-sentence "what this source is and why it mattered"}

## Key takeaways

- {3–7 bullets, in your own words. Not a transcription of the source.}

## Concepts touched

- [[ml_concepts/concept-a]] — {how the source addressed it: new info, confirmation, contradiction, refinement}
- [[math_concepts/concept-b]] — {…}

## Contradictions and revisions

{Did this source disagree with anything already in the wiki? Note it. This
section can be empty.}

## Questions raised

- [[questions/...]]

## Pointer back to raw

`{source_path}`
```

### Question page

```markdown
---
{frontmatter; status starts as `stub`, flips to `mature` when resolved}
---

# {The question, phrased clearly}

## Why it matters

{1–3 sentences}

## What we know so far

- {bullets summarising current state — link to concepts/sources}

## What would resolve it

- {experiment, paper to find, derivation to attempt}

## Related

- [[ml_concepts/...]] or [[math_concepts/...]]
- [[sources/...]]
```

---

## index.md

A flat catalog of every wiki page, grouped by type. One line per page: `- [[slug]] — one-line summary` (the same summary as the first blockquote on the page). Keep entries sorted alphabetically within each section.

Skeleton:

```markdown
# Wiki Index

_Last updated: 2026-05-15_

## ML concepts
- [[ml_concepts/attention]] — short summary
- [[ml_concepts/calibration]] — short summary
...

## Math concepts
- [[math_concepts/kl-divergence]] — short summary
- [[math_concepts/softmax]] — short summary
...

## Methods
- [[methods/adamw]] — short summary
...

## Topics
- [[topics/optimization]] — short summary
...

## Sources
- [[sources/karpathy-makemore-3]] — short summary
...

## Questions
- [[questions/why-does-lr-warmup-help]] — short summary
...
```

Update `index.md` on every ingest, every new wiki page, and whenever a one-line summary changes.

---

## log.md

Append-only chronological log. Every operation that touches the wiki gets one entry. Entry headings follow a strict format so the log is grep-friendly:

```markdown
## [YYYY-MM-DD] {verb} | {short title}

- **What:** {1-line description}
- **Pages touched:** [[a]], [[b]], [[c]]
- **Notes:** {optional — open questions raised, contradictions found, things to revisit}
```

Verbs: `ingest`, `query`, `lint`, `quiz`, `refactor` (when you restructure pages without ingesting a new source).

Example:

```markdown
## [2026-05-15] ingest | Karpathy — makemore part 3

- **What:** Lecture on activations and gradients in MLPs; ingested from raw/lectures/karpathy-makemore-3.md.
- **Pages touched:** [[sources/karpathy-makemore-3]], [[ml_concepts/batch-normalization]] (new), [[ml_concepts/initialisation]] (updated), [[methods/kaiming-init]] (new), [[topics/training-dynamics]] (updated index).
- **Notes:** Raises [[questions/why-does-tanh-saturation-stall-training]].
```

The log is the timeline of how the wiki evolved. Do not edit past entries — append corrections as new entries.

---

## Linking conventions

- Use `[[wiki-link]]` syntax (Obsidian-style) for internal references. Prefer the slug only when it's unambiguous; fall back to `[[ml_concepts/foo]]` or `[[math_concepts/foo]]` when needed.
- A `[[link]]` to a page that doesn't exist is **fine and encouraged** — it marks the page as worth writing later. Surface these orphan-targets during `wiki-lint`.
- Cite raw sources by linking to the corresponding `sources/*` page (which carries the `raw/...` path in its frontmatter). Don't put raw paths directly in `ml_concept`, `math_concept`, or method pages.
- Link liberally. Obsidian's graph view depends on link density; missing links make the wiki feel like a folder of disconnected notes.
- Backlinks are free in Obsidian — you don't need to maintain "linked from" sections manually.

---

## Operations

Four operations, each codified as a project skill in `.claude/skills/`:

| Skill | Trigger | What it does |
|---|---|---|
| `wiki-ingest` | "ingest this", "process this source", "add to wiki" | Read a raw source, discuss takeaways, update relevant pages, write source page, update index, append log entry |
| `wiki-query` | "what does the wiki say about X", "synthesize X across the wiki", or any substantive ML question | Read index, drill into relevant pages, synthesize answer with citations, optionally file the answer back as a new wiki page |
| `wiki-lint` | "lint the wiki", "audit the wiki", "health check" | Scan for orphans, missing pages, contradictions, stale claims; report findings; let the user choose what to act on |
| `wiki-quiz` | "quiz me", "test me", "give me problems", "interview prep", "проверь меня", "дай задач" | Ask format/scope/difficulty/count, then generate a quiz from wiki pages (multiple choice, open questions, paper-and-pen problems); grade and explain answers; log the session |

Invoke the matching skill (via the Skill tool) when the user requests one of these. The skill walks you through the workflow.

---

## Quality bar

The reader is a working ML engineer. Calibrate accordingly:

- **No basics.** Don't define `numpy`, `dot product`, or `loss function` from scratch. Link to a concept page if needed.
- **No marketing voice.** «Attention — это революционный механизм, который изменил...» — нет. «Attention оценивает каждый key относительно query и взвешенно агрегирует values».
- **Definitions first.** Every page opens with a one- or two-sentence blockquote that defines the thing. Someone skimming the index should know what the page is about from that line alone.
- **Math when it clarifies.** Use LaTeX (`$...$`, `$$...$$`). Don't paraphrase equations into prose unless the prose is genuinely clearer. See "Math notation" below — math notation is **never** in backticks.
- **Pseudocode over English** for algorithms with non-obvious control flow.
- **One concept per page.** If a page is doing two things, split it.
- **Cite specifically.** Don't write "as discussed in the source"; link to the source page with the contribution stated inline.

### Up next footer

`## Up next` appears at the bottom of `ml_concept` and `method` pages. It tells a reader in study mode where to go next.

- 1–2 bullets, no more. Format: `- [[wiki-link]] — one-line "why this is the natural next step"`.
- On methods: a related/successor method, or the topic primer for the area.
- On `ml_concept`s: a concept that builds on this one, or a method that instantiates it.
- Omit on `math_concept`s (math is not read sequentially), on stubs, on source pages, and on question pages.

### Line length

Do **not** manually wrap prose. Obsidian soft-wraps text at display time, so source-level line breaks inside a paragraph just clutter diffs and have no rendering effect. One paragraph = one line. Same for bullet items, blockquote paragraphs, and any other block of flowing text — each stays on a single source line, no matter how long. Frontmatter, code blocks, display-math blocks, and tables are line-structured by their own syntax: leave those line breaks alone.

### Math notation

All mathematical notation goes in **LaTeX**, never in backticks. Inline math uses `$...$`, display math uses `$$...$$`. This applies to symbols, expressions, equations, set notation, function notation — anything mathematical, even a single Greek letter or a single subscripted variable. Backticks are reserved for code identifiers (function names, module paths, parameter names, type names, file paths, library names).

Bad (math notation in backticks):

- `t_0 < t_1 < ... < t_N`
- `s, t ∈ [0,σ]`
- `f_θ(x, t) = c_skip(t)·x + c_out(t)·F_θ(x, t)`
- `{x_τ}_{τ ∈ [0,σ]}`
- `x_0`, `f_θ`, `Δ = s - t`

Good (LaTeX):

- $t_0 < t_1 < \ldots < t_N$
- $s, t \in [0, \sigma]$
- $f_\theta(x, t) = c_{\text{skip}}(t) \cdot x + c_{\text{out}}(t) \cdot F_\theta(x, t)$
- $\{x_\tau\}_{\tau \in [0, \sigma]}$
- $x_0$, $f_\theta$, $\Delta = s - t$

When the surrounding sentence forces a choice between "math symbol" and "code identifier" interpretation, ask which one the reader needs:

- A reference to a Python attribute on the model object (`model.eps`) → code, backticks.
- The noise variable $\epsilon$ in an equation → math, LaTeX.

In Unicode-clean math expressions (e.g. `σ`, `θ`, `·`, `∈`, `≤`, `→`) inside backticks, convert to LaTeX commands (`\sigma`, `\theta`, `\cdot`, `\in`, `\leq`, `\to`). Multi-letter subscripts like `skip` or `out` use `_{\text{...}}` for upright font; single-letter subscripts go bare (`x_t`, `f_\theta`).

### Math exposition

On `math_concept` pages, walk through the math step by step. Show every intermediate step rather than collapsing to a compressed equation. Name each symbol when it first appears. Include a worked numerical example with small, concrete values. Trade brevity for clarity — the reader finds dense math hard to follow on first read.

On `ml_concept` and method pages, if a derivation gets gnarly, link out to a `math_concept` page instead of expanding it inline. Keeps the ML page focused on the mechanism, math page focused on the math.

### Page length

No hard cap. Aim for "as long as needed to make the point, no longer". If a page passes ~750 lines, look for a natural split (usually a sub-concept that deserves its own page).

### What not to write

- Don't write meta-commentary about the wiki — «эта страница рассказывает о…», «в данной заметке мы рассмотрим…», «здесь мы поговорим о…», "this page covers…", "this is part of the X topic". The frontmatter, taxonomy, and links carry that information.
- Don't write things you don't know. If a source is unclear on a point, say so in the source page; don't paper over the gap on the concept page.
- Don't summarise the source instead of integrating it. The wiki is concept-first, not source-first.

---

## Language

Narrative wiki pages — everything under `wiki/ml_concepts/`, `wiki/math_concepts/`, `wiki/methods/`, `wiki/topics/`, `wiki/sources/`, `wiki/questions/` — are written in **Russian**. Service files — this `CLAUDE.md`, `wiki/index.md`, `wiki/log.md`, `.claude/skills/**` — stay in English.

What stays English even inside Russian pages:
- **Frontmatter `title:` field and H1 of the page.** `title: Variational Autoencoder (VAE)`, `# Variational Autoencoder (VAE)`.
- **Filenames / slugs, tags, internal `[[wiki-links]]`.**
- **ML and math terms inside Russian prose.** Keep them English: flow matching, attention, score matching, KL divergence, posterior, prior, embedding, latent, ELBO, autoencoder, gradient, softmax, dropout, EMA, etc. Do not transliterate (`флоу-матчинг`, `постериор`) and do not over-translate (`нижняя граница доказательства` for ELBO). Common words with stable Russian equivalents — «градиент», «вероятность», «распределение», «выборка» — pick whichever reads cleaner in context.

Style rules for Russian prose:
- **No bureaucracy.** Avoid clerical fillers: «является», «осуществляется», «представляет собой», «в данной работе», «следует отметить, что», «производится», «имеет место».
- **No filler openings.** Banned: «в заключение», «подводя итог», «стоит отметить», «важно понимать, что», «давайте разберёмся», «погрузимся в», «как мы знаем», «как известно», «не случайно».
- **No marketing epithets.** Banned: «мощный», «впечатляющий», «революционный», «передовой», «прорывной», «инновационный».

Service text (this `CLAUDE.md`, skills, log entries) stays plain English: common words, no idioms, no archaic phrasing, straightforward grammar.

---

## What this directory is NOT

- **Not a code repo.** Python rules from `~/.claude/CLAUDE.md` (banned tools, type hints, file length limits) do not apply to markdown content. They do apply if you write helper Python scripts under `.claude/` or similar.
- **Not a chat log.** Conversation transcripts belong in `raw/scratch/` if useful, never in `wiki/`.
- **Not a static document.** Pages get revised when new sources arrive. The log captures the timeline.
- **Not a generic ML textbook.** This is a personal wiki — write what the user finds useful, in the order the user encounters it. Don't try to cover everything; let coverage emerge from sources.

---

## When you're unsure

- Default to writing an `ml_concept` page over a method page if the idea exists outside any single algorithm. Use `math_concept` only for pure math objects (operations, distance measures, inequalities, functions).
- Default to a stub `[[link]]` over silently dropping a reference.
- Default to asking before deleting or substantially rewriting an existing page (especially `mature` ones).
- Default to one ingest at a time over batch processing — the user wants to stay in the loop.
