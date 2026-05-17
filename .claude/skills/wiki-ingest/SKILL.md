---
name: wiki-ingest
description: Main flow for converting one raw source into one wiki breakdown page. 8 phases with explicit gates. Triggers when the user says "ingest", "process this source", "add this article to the wiki", or hands you a path under `raw/`.
---

# wiki-ingest

Convert one raw source into **one** wiki breakdown page. The page follows Template A (Motivation-first) from `_shared/page-templates.md`. Even a long lecture covering 5 concepts produces a single page — concepts become subsections of «Как это работает», not separate pages.

## Pre-flight (Phase 1)

Before doing anything else, read these in order:

- [ ] Read `.claude/role.md`
- [ ] Read `.claude/skills/_shared/page-templates.md`
- [ ] Read `.claude/skills/_shared/russian-style.md`
- [ ] Read `.claude/skills/_shared/illustration-policy.md`
- [ ] Read `.claude/rules/04-frontmatter-schema.md` (for the tag whitelist)
- [ ] Read `wiki/index.md` (to see what already exists)
- [ ] Read `.autodoc/index.md` (skip if the file does not yet exist)

Then create a TodoWrite list with one item per remaining phase (2-8).

## Phase 2 — Read the source

- [ ] Confirm the source lives under `raw/{papers,clips,lectures,scratch}/` or `raw/knowledge-sharings/`. If it does not, ask where it should live; never move files in `raw/` without permission.
- [ ] Read the file fully. For PDFs over 10 pages, use the Read tool's `pages` parameter to page through in ranges.
- [ ] For markdown clips with referenced images: read the markdown, identify load-bearing images (figures, plots), read those individually. Do not read all images by default.
- [ ] Take silent notes. Do not write the wiki page yet.
- [ ] Scan `wiki/index.md` — does any existing breakdown overlap with this source? If yes, the new page will link to it from «Связанные разборы».

## Phase 3 — Research a gap (optional)

Trigger condition: the source has a gap that blocks a clear explanation — references a prior method or result that is load-bearing for the explanation, and the primary source does not define or prove it. Skip if the source is self-contained.

- [ ] If no gap, skip to Phase 4.
- [ ] If a gap exists, dispatch the `wiki-source-researcher` agent with a narrow query:
  ```
  Subagent: wiki-source-researcher
  Query: <one-sentence gap>
  Context: <what the primary source says about it>
  ```
- [ ] Wait for the structured report. Keep it in context. Do **not** write the report to `raw/` automatically — the user decides what to keep.

## Phase 4 — Plan + user approval

Present the plan in this format:

```
Source: <title> (<source_kind>, <source_date>)
Target page: wiki/<kind>/<slug>.md

TL;DR draft:
<1-3 sentences>

Tags (from whitelist): <tag1>, <tag2>, <tag3>

Motivation arc:
- What we want: ...
- Naive approach: ...
- Why it fails: ...
- What this source proposes: ...

Key idea in one figure (planned):
- Mermaid: <short description> OR
- Matplotlib: <short description>

Optional sections to include: <list, e.g., "Результаты, Сравнение, Ограничения"; or "none">

Related breakdowns to link:
- [[<kind>/<slug>]] — <one-line>

Anything to emphasise, skip, or correct?
```

**Stop and wait for the user.** Do not write the page yet.

If the user has explicitly asked for autonomous mode, still emit the plan, then proceed unless something is genuinely ambiguous.

## Phase 5 — Write the page

- [ ] Pick Template A (or Template B for KS) from `_shared/page-templates.md`.
- [ ] Russian prose body, English headings/slugs/tags/frontmatter (`rules/01`).
- [ ] Frontmatter exactly per `rules/04-frontmatter-schema.md`.
- [ ] Required sections in order: TL;DR (as blockquote under H1) → Мотивация → Идея в одной картинке → Как это работает → Вывод → Источник.
- [ ] Optional sections inserted between «Как это работает» and «Вывод» when content justifies them.
- [ ] Math in LaTeX, every non-trivial formula followed by `где: ...`.
- [ ] Term introduction discipline on every new term (bold + definition + analogy on first mention).
- [ ] Stub links to non-existing related pages are fine — they mark future ingests.

## Phase 6 — Illustrations

For the «Идея в одной картинке» (mandatory) and any additional figures:

- [ ] Pick a tool per `_shared/illustration-policy.md`: mermaid for flow/relations, matplotlib for plots/numerical, source cut-out for paper diagrams with attribution.
- [ ] Mermaid: inline, ≤ 12 nodes, no math in node labels.
- [ ] Matplotlib: write `.py` and run it to produce `.png` at `wiki/static/figures/<page-slug>/`. Commit both files. PNG ≤ 200 KB.
- [ ] Source cut-out: save under the same path with `source-cut-` prefix; caption is mandatory with full attribution.
- [ ] Caption format follows `rules/03-illustration-policy.md`.

## Phase 7 — Self-check (Russian style + content)

- [ ] Invoke `/write-russian` on the page. The skill has the full anti-AI ruleset, term-introduction discipline, anglicism replacement table, punctuation rules, and an editing checklist + fast grep. Apply all findings inline.
- [ ] Verify every factual claim is sourced (`[[<kind>/<slug>]]` link or inline paper attribution).
- [ ] Verify illustrations are attached to text — every figure has a one-sentence lead-in and one-sentence walk-out.
- [ ] Verify `где: ...` list under every non-trivial formula.
- [ ] Verify all tags are in the `rules/04` whitelist; if a tag is missing, extend the whitelist in the same commit.
- [ ] Fix all findings inline.

## Phase 8 — Bookkeeping and commit proposal

- [ ] **Update `wiki/index.md`**:
  - Prepend a new line under «Recent ingests» with date + link + TL;DR-one-liner.
  - Insert the new page under the matching kind section, keeping alphabetical order (or chronological newest-first for KS).
  - Update the «By tag» section: under each tag this page uses, add the new link. Create a new tag entry if it didn't exist (after confirming the tag is in the whitelist).
  - Trim «Recent ingests» to the last 10 entries; drop overflow.
- [ ] **Append to `wiki/log.md`**:
  ```
  ## [YYYY-MM-DD] ingest | <source title>

  - **What:** <one-line>
  - **Page(s) touched:** [[<kind>/<slug>]]
  - **Notes:** <optional — open questions, contradictions, things to revisit>
  ```
- [ ] Report to the user: page path, status, any contradictions with existing breakdowns, any new tags added to whitelist.
- [ ] Suggest `/wiki-lint` if frontmatter was edited.
- [ ] Propose an atomic commit (≤ 300 lines):
  ```
  feat(wiki): ingest <source> — <short-desc>

  - new: wiki/<kind>/<slug>.md
  - update: wiki/index.md
  - update: wiki/log.md
  - figures: wiki/static/figures/<slug>/{<file>.py,<file>.png}  (if any)
  - update: .claude/rules/04-frontmatter-schema.md  (if new tag added)
  ```
- [ ] **Stop and wait for the user to approve the commit message before running `git commit`.**
- [ ] **Never run `git push`.** Push is a manual user action only.

## Gates where you stop and wait

| Phase | Wait for |
|---|---|
| 4 | User OK on the plan before writing the page |
| 7 | (Optional `--review` mode) — diff summary of the page before commit |
| 8 | User OK on the commit message before `git commit` |

In autonomous mode (user said "work without stopping"): Phase 4 still emits the plan but does not wait; Phases 7-8 proceed without confirmation.
