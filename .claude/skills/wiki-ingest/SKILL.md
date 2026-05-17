---
name: wiki-ingest
description: Main flow for converting one raw source into one wiki breakdown page. 9 phases with explicit gates. Triggers when the user says "ingest", "process this source", "add this article to the wiki", or hands you a path under `raw/`.
---

# wiki-ingest

Convert one raw source into **one** wiki breakdown page. The page follows Template A (Motivation-first) from `_shared/page-templates.md`. Even a long lecture covering 5 concepts produces a single page — concepts become subsections of «Как это работает», not separate pages.

## Pre-flight (Phase 1)

Before doing anything else, read these in order:

- [ ] Read `.claude/role.md`
- [ ] Read `.claude/skills/_shared/page-templates.md`
- [ ] Read `.claude/skills/_shared/russian-style.md`
- [ ] Read `.claude/skills/_shared/illustration-policy.md`
- [ ] Read `.claude/rules/04-frontmatter-schema.md` (frontmatter rules)
- [ ] Read `wiki/tags.md` (the live tag registry — names + definitions)
- [ ] Read `wiki/index.md` (to see what already exists)
- [ ] Read `.autodoc/index.md` (skip if the file does not yet exist)

Then create a TodoWrite list with one item per remaining phase (2-9).

## Phase 2 — Read the source

- [ ] Confirm the source lives under `raw/{papers,clips,lectures,scratch}/` or `raw/knowledge-sharings/`. If it does not, ask where it should live; never move files in `raw/` without permission. `raw/` is **gitignored** — the file exists on the user's disk but is not in git history. That's fine for reading; just don't try to `git add` it in Phase 9.
- [ ] Read the file fully. For PDFs over 10 pages, use the Read tool's `pages` parameter to page through in ranges.
- [ ] For markdown clips with referenced images: read the markdown, identify load-bearing images (figures, plots), read those individually. Do not read all images by default.
- [ ] Take silent notes. Do not write the wiki page yet.
- [ ] Scan `wiki/index.md` — does any existing breakdown overlap with this source? If yes, the new page will link to it from «Связанные разборы».

## Phase 3 — Extract embedded images from the source

Many sources have figures embedded — papers have geometric diagrams, posts have screenshots, slides have plots. Pull them out programmatically so they can be reused as attributed cut-outs in Phase 7. This replaces the manual Cmd+Shift+4 screenshot path.

Pick the right extractor by source type:

**PDF** (`raw/papers/foo.pdf`):

```bash
mkdir -p /tmp/<slug>-source-imgs
pdfimages -png raw/papers/foo.pdf /tmp/<slug>-source-imgs/img
```

Requires `poppler-utils` (`brew install poppler` on macOS; usually pre-installed on dev machines). Outputs `img-000.png`, `img-001.png`, ... For text-heavy PDFs that embed figures as vector graphics, also try:

```bash
pdftoppm -png -r 150 raw/papers/foo.pdf /tmp/<slug>-source-imgs/page
```

(One PNG per page; useful when you need the figure with its caption in context — crop later.)

**DOCX / DOC** (`raw/clips/foo.docx`):

```bash
mkdir -p /tmp/<slug>-source-imgs
unzip -j raw/clips/foo.docx 'word/media/*' -d /tmp/<slug>-source-imgs
```

DOCX is a zip; `word/media/` is where embedded images live. Files keep their original extensions (`.png`, `.jpeg`, `.emf`).

**HTML / markdown clip** with referenced images:

```bash
mkdir -p /tmp/<slug>-source-imgs
# either: parse the markdown for ![](src) and curl each one
# or: if source is a URL, use rdrr to fetch + extract refs
rdrr <url> -j | jq -r '.images[]' | while read u; do curl -sL "$u" -O --output-dir /tmp/<slug>-source-imgs/; done
```

**PPTX** (rare, but lecture slides):

```bash
unzip -j raw/lectures/foo.pptx 'ppt/media/*' -d /tmp/<slug>-source-imgs
```

After extraction:

- [ ] List the images: `ls -lh /tmp/<slug>-source-imgs/`
- [ ] Open the directory in Finder (`open /tmp/<slug>-source-imgs/`) and visually scan.
- [ ] **Note** which extracted images correspond to which figures in the source (e.g., «img-003.png is Fig. 2 — the geometric construction»).
- [ ] **Do not commit them yet.** The final selection happens in Phase 7 when you place cut-outs into the page. Keep the temp directory until then.

If extraction yields nothing useful or the tool is unavailable, skip — rely on matplotlib + mermaid as usual in Phase 7. The flow does not stall on missing extraction.

## Phase 4 — Research a gap (optional)

Trigger condition: the source has a gap that blocks a clear explanation — references a prior method or result that is load-bearing for the explanation, and the primary source does not define or prove it. Skip if the source is self-contained.

- [ ] If no gap, skip to Phase 5.
- [ ] If a gap exists, dispatch the `wiki-source-researcher` agent with a narrow query:
  ```
  Subagent: wiki-source-researcher
  Query: <one-sentence gap>
  Context: <what the primary source says about it>
  ```
- [ ] Wait for the structured report. Keep it in context. Do **not** write the report to `raw/` automatically — the user decides what to keep.

## Phase 5 — Plan + user approval

Present the plan in this format:

```
Source: <title> (<source_kind>, <source_date>)
Target page: wiki/<kind>/<slug>.md

TL;DR draft:
<4-7 sentences per page-templates.md TL;DR structure>

Tags (from wiki/tags.md): <tag1>, <tag2>, <tag3>
New tags to register (if any): <tag-x> — <one-sentence definition>

Motivation arc:
- What we want: ...
- Naive approach: ...
- Why it fails: ...
- What this source proposes: ...

Figures planned (≥ minimum from rules/03 — paper 3, lecture 2, clip 1, KS 1):
1. <type: mermaid|matplotlib|cut-out from img-NNN.png> — <one-line description>
2. <type> — <one-line description>
3. <type> — <one-line description>

Optional sections to include: <list, e.g., "Данные, Результаты, Сравнение, Ограничения"; or "none">
Comparison tables to reproduce: <list of source tables with column headers, e.g., "Table 1 (complexity vs RNN/Conv), Table 3 (PE ablation)"; or "none">
Data section needed: <yes if source documents corpus/preprocessing in detail; no for pure-theory/method papers>

Related breakdowns to link:
- [[<kind>/<slug>]] — <one-line>

Anything to emphasise, skip, or correct?
```

**Stop and wait for the user.** Do not write the page yet.

If the user has explicitly asked for autonomous mode, still emit the plan, then proceed unless something is genuinely ambiguous.

## Phase 6 — Write the page

- [ ] Pick Template A (or Template B for KS) from `_shared/page-templates.md`.
- [ ] Russian prose body, English headings/slugs/tags/frontmatter (`rules/01`).
- [ ] Frontmatter exactly per `rules/04-frontmatter-schema.md`.
- [ ] Required sections in order: TL;DR (as blockquote under H1) → Мотивация → Идея в одной картинке → Как это работает → Вывод → Источник.
- [ ] Optional sections inserted between «Как это работает» and «Вывод» when content justifies them. «Данные» belongs here when the source documents corpus composition / preprocessing / filtering in detail (skip for pure-theory papers).
- [ ] **Comparison tables.** Every comparison the source presents — benchmark grid, ablation, config matrix, dataset breakdown — gets rendered as a markdown table in the breakdown (typically inside «Сравнение с альтернативами» or «Результаты»), not flattened into bullets. Cite under the table: `*Source: ..., Table N.*`
- [ ] Math in LaTeX, every non-trivial formula followed by `где: ...`.
- [ ] Term introduction discipline on every new term (bold + definition + analogy on first mention).
- [ ] Stub links to non-existing related pages are fine — they mark future ingests.

## Phase 7 — Illustrations

For the «Идея в одной картинке» (mandatory) and any additional figures:

- [ ] Pick a tool per `_shared/illustration-policy.md`: mermaid for flow/relations, matplotlib for plots/numerical, source cut-out (from Phase 3 extraction) for paper figures with attribution.
- [ ] Mermaid: inline, ≤ 12 nodes, no math in node labels.
- [ ] Matplotlib: write `.py` to a scratch path (e.g., `/tmp/<slug>-<name>.py`), **run it** to produce `wiki/static/figures/<slug>-<name>.png`, verify the PNG opens and is ≤ 200 KB, then **delete the .py**. Only the PNG is committed. The script is one-shot — its recipe lives in this ingest conversation, not in the repo.
- [ ] Source cut-out: copy the chosen file from `/tmp/<slug>-source-imgs/` to `wiki/static/figures/<slug>-fig<N>-cutout.png` (or `<slug>-source-<n>.png`). Crop tightly if needed. Attribution caption is mandatory: `*From <First Author> et al. (<year>), Fig. <N>.*`
- [ ] Caption format follows `rules/03-illustration-policy.md`: matplotlib has **no** caption line, cut-outs **must** have attribution, mermaid uses `*Diagram: ...*`.
- [ ] **Figure count gate.** Count the figures on the page. Required floor (rules/03): paper ≥ 3, lecture ≥ 2, clip ≥ 1, KS ≥ 1. If below floor, go back and add — typical candidates: a matplotlib plot for any quantitative claim that currently sits as bare text; a mermaid for any data flow described in prose; a source cut-out (with attribution) from Phase 3 for paper figures you would otherwise re-explain in prose.
- [ ] **Lead-in + walk-out gate.** Every figure has one sentence right before it («что покажем») and one sentence right after it («что забрать»). No floating images.
- [ ] **Cleanup.** Once all figures are in place, remove `/tmp/<slug>-source-imgs/` (the unused extracted images don't ship with the wiki).

## Phase 8 — Self-check (Russian style + content)

- [ ] Invoke `/write-russian` on the page. The skill has the full anti-AI ruleset, term-introduction discipline, anglicism replacement table, punctuation rules, and an editing checklist + fast grep. Apply all findings inline.
- [ ] Verify every factual claim is sourced (`[[<kind>/<slug>]]` link or inline paper attribution).
- [ ] Verify illustrations are attached to text — every figure has a one-sentence lead-in and one-sentence walk-out.
- [ ] Verify `где: ...` list under every non-trivial formula.
- [ ] Verify all page tags have an H2 entry in `wiki/tags.md`. If any tag is new, append an H2 to `wiki/tags.md` with name, slug, one-sentence definition, and the `[Все разборы →](/tags/<slug>)` link — **in the same commit** as the page.
- [ ] Fix all findings inline.

## Phase 9 — Bookkeeping and commit proposal

- [ ] **Update `wiki/index.md`**:
  - Prepend a new line under «Recent ingests» with date + link + TL;DR-one-liner.
  - Insert the new page under the matching kind section, keeping alphabetical order (or chronological newest-first for KS).
  - Update the «By tag» section: under each tag this page uses, add the new link. If a tag has no «By tag» entry yet, create one — but the tag must already exist as an H2 in `wiki/tags.md` (added in this same commit if new).
  - Trim «Recent ingests» to the last 10 entries; drop overflow.
- [ ] **Update `wiki/tags.md`** if this ingest introduced any new tags:
  - Append a new H2 per new tag with name, `**Slug:**`, one-sentence definition, and `[Все разборы →](/tags/<slug>)`.
  - Bump the `_Last updated:_` line at the top to today's date.
- [ ] **Append to `wiki/log.md`**:
  ```
  ## [YYYY-MM-DD] ingest | <source title>

  - **What:** <one-line>
  - **Page(s) touched:** [[<kind>/<slug>]]
  - **Notes:** <optional — open questions, contradictions, things to revisit>
  ```
- [ ] Report to the user: page path, status, any contradictions with existing breakdowns, any new tags added to the registry, any source images used as cut-outs.
- [ ] Suggest `/wiki-lint` if frontmatter was edited.
- [ ] Propose an atomic commit (≤ 300 lines):
  ```
  feat(wiki): ingest <source> — <short-desc>

  - new: wiki/<kind>/<slug>.md
  - update: wiki/index.md
  - update: wiki/log.md
  - figures: wiki/static/figures/<slug>-<name>.png  (PNGs only; .py deleted after build)
  - update: wiki/tags.md  (if new tag added)
  ```
- [ ] **Stop and wait for the user to approve the commit message before running `git commit`.**
- [ ] **Never run `git push`.** Push is a manual user action only.

## Gates where you stop and wait

| Phase | Wait for |
|---|---|
| 5 | User OK on the plan before writing the page |
| 8 | (Optional `--review` mode) — diff summary of the page before commit |
| 9 | User OK on the commit message before `git commit` |

In autonomous mode (user said "work without stopping"): Phase 5 still emits the plan but does not wait; Phases 8-9 proceed without confirmation.
