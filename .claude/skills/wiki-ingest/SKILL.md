---
name: wiki-ingest
description: Main flow for converting a raw source into wiki pages. 8 phases with explicit gates. Triggers when the user says "ingest", "process this source", "add this article to the wiki", or hands you a path under `raw/`.
---

# wiki-ingest

Convert one raw source into wiki pages: integration, not summarisation.

## Pre-flight (Phase 1)

Before doing anything else, read these in order:

- [ ] Read `.claude/role.md`
- [ ] Read `.claude/skills/_shared/page-templates.md`
- [ ] Read `.claude/skills/_shared/russian-style.md`
- [ ] Read `.claude/skills/_shared/illustration-policy.md`
- [ ] Read `wiki/index.md`
- [ ] Read `.autodoc/index.md` (skip if the file does not exist — it will be created on first `/autodoc` run)

Then create a TodoWrite list with one item per remaining phase (2-8).

## Phase 2 — Read the source

- [ ] Confirm the source lives under `raw/{papers,clips,lectures,scratch}/`. If it does not, ask the user where it should live; never move files in `raw/` without permission.
- [ ] Read the file fully. For PDFs over 10 pages, use the Read tool's `pages` parameter to page through in ranges.
- [ ] For markdown clips with referenced images: read the markdown, identify load-bearing images (figures, plots), read those individually. Do not read all images by default.
- [ ] Take silent notes. Do not write any wiki page yet.
- [ ] Scan `wiki/index.md` and the relevant `wiki/ml_concepts/<top>/` or `wiki/methods/<top>/` subfolders to identify pages this source touches.

## Phase 3 — Research a gap (optional)

Trigger condition: the source has a gap that blocks a clear explanation — references a prior method or result that is load-bearing for the explanation and the primary source does not define or prove it. Skip if the source is self-contained.

- [ ] If no gap, skip to Phase 4.
- [ ] If a gap exists, dispatch the `wiki-source-researcher` agent with a narrow query:
  ```
  Subagent: wiki-source-researcher
  Query: <one-sentence gap>
  Context: <what the primary source says about it>
  ```
- [ ] Wait for the structured report. Keep it in context. Do **not** write the report to `raw/` automatically — the user decides.

## Phase 4 — Takeaways and user approval

Present takeaways in this format:

```
Source: <title> (<source_kind>, <date>)

Takeaways:
- <3-7 bullets in your own words; not a transcription>

Likely wiki impact:
- Create: [[<new-page-path>]]
- Update: [[<existing-page-path>]] — <one-line what changes>
- Stub: [[<new-stub-path>]] (mentioned but not fully covered)
- Source: [[sources/<slug>]]

Open questions:
- <unresolved bits>

Anything to emphasise or skip?
```

**Stop and wait for the user.** Do not write any page yet.

If the user has explicitly asked for autonomous mode, still emit the block, then proceed without waiting unless something is genuinely ambiguous.

## Phase 5 — Write the pages

For each page in the plan:

- [ ] Pick the template from `_shared/page-templates.md` matching the `type:`.
- [ ] Write Russian prose body, English headings/slugs/tags/frontmatter (see `rules/01`).
- [ ] Frontmatter follows `rules/04`. Do **not** set `needs_rewrite` on new pages; clear it on pages you fully rewrite.
- [ ] Math in LaTeX (`$...$`, `$$...$$`), never in backticks.
- [ ] For non-trivial math, link to `[[math_concepts/...]]` instead of expanding inline.
- [ ] Stub links to not-yet-existing pages are fine and encouraged — they queue future ingests.

Edit order: concept/method pages first → source page next. `wiki/index.md` and `wiki/log.md` are updated in Phase 8.

## Phase 6 — Illustrations

For each non-trivial concept on each page just written, apply the chooser from `_shared/illustration-policy.md`:

- [ ] For each concept: mermaid / matplotlib / source cut-out / file a question page.
- [ ] Mermaid: inline in markdown, ≤ 12 nodes, no math in node labels.
- [ ] Matplotlib: write `.py` and run it to produce `.png` at `wiki/static/figures/<page-slug>/`. Commit both. PNG ≤ 200 KB. URL in markdown stays `/static/figures/<page-slug>/<file>.png`.
- [ ] Source cut-out: save under same path with `source-cut-` prefix and write attribution caption.
- [ ] Add the figure reference and caption to the page.

Run the illustration checklist in `_shared/illustration-policy.md` for each page.

## Phase 7 — Self-check (Russian style + content)

- [ ] Re-read `_shared/russian-style.md`.
- [ ] For each page, run the checklist at the end of that file (banned constructions, AI-speak, marketing epithets, calque anglicisms).
- [ ] Verify every claim is sourced or marked as an open question.
- [ ] Verify illustrations are attached to text (no floating images).
- [ ] Fix all findings inline.

## Phase 8 — Bookkeeping and commit proposal

- [ ] Update `wiki/index.md` with new entries (or revised one-line summaries).
- [ ] Append to `wiki/log.md`:
  ```
  ## [YYYY-MM-DD] ingest | <source title>

  - **What:** <one-line>
  - **Pages touched:** [[<page-a>]], [[<page-b>]], ...
  - **Notes:** <open questions, contradictions, anything to revisit>
  ```
- [ ] Report to the user: list of touched files, new stubs, contradictions with existing content.
- [ ] Suggest `/wiki-lint` if frontmatter was edited.
- [ ] Propose an atomic commit (≤ 300 lines):
  ```
  feat(wiki): ingest <source> — <short-desc>

  - new: <path-a>
  - new: <path-b>
  - update: <path-c>
  - figures: wiki/static/figures/<slug>/{<file>.py,<file>.png}
  ```
- [ ] **Stop and wait for the user to approve the commit message before running `git commit`.**
- [ ] **Never run `git push`.** Wait for the user to push manually.

## Gates where you stop and wait

| Phase | Wait for |
|---|---|
| 4 | User OK on takeaways before writing |
| 7 | (Optional `--review` mode) — diff of pages before commit |
| 8 | User OK on commit message before `git commit` |

In autonomous mode (user said "work without stopping"): phase 4 still emits takeaways but does not wait; phases 7-8 proceed without confirmation.
