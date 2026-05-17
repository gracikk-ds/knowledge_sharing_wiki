# Wiki Source-Breakdowns Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the wiki repo from the old «concept = page» model to the new «source = page» model. Empty `wiki/` becomes a 4-folder layout (`papers/`, `lectures/`, `clips/`, `knowledge-sharings/`) ready for source breakdowns; supporting skills, rules, and docs are rewritten to match.

**Architecture:** New canonical structure: one page per source under `wiki/<source_kind>/<slug>.md`, following Template A (Motivation-first) with required sections (TL;DR / Мотивация / Идея в одной картинке / Как это работает / Вывод / Источник) and 5 optional sections. New frontmatter schema with `source_kind`, `source_path`, `authors`, `tags`, `status`; tag whitelist enforced by `wiki-lint`. Concepts navigated via tags + `wiki/index.md`, not via central concept pages.

**Tech Stack:** Markdown, Mermaid, Matplotlib, Quartz (static site generator), Vercel deploy. No code dependencies introduced.

**Spec:** `docs/superpowers/specs/2026-05-18-wiki-source-breakdowns-design.md`

**Branch:** `wiki-overhaul`

**Commit policy:** ≤ 300 changed lines per commit, conventional commits. **No `git push`** at any point.

---

## File Structure

### New files

```
wiki/.gitkeep                                  # placeholder for empty subdirs
wiki/papers/.gitkeep
wiki/lectures/.gitkeep
wiki/clips/.gitkeep
wiki/knowledge-sharings/.gitkeep
wiki/index.md                                  # skeleton index
wiki/log.md                                    # empty chronological log
```

### Rewritten files

```
.claude/rules/04-frontmatter-schema.md         # new schema + tag whitelist
.claude/skills/_shared/page-templates.md       # 2 new templates (replace 6 old)
.claude/skills/wiki-ingest/SKILL.md            # one-page flow
.claude/role.md                                # drop concept-page section
CLAUDE.md                                      # layout block
ONBOARDING.md                                  # structure map + worked example
```

### Updated files (smaller edits)

```
.claude/skills/wiki-lint/SKILL.md              # new schema enforcement
.claude/skills/wiki-query/SKILL.md             # tag-based search strategy
```

### Untouched in this plan

- `.claude/rules/01-language-policy.md`, `02-commit-policy.md`, `03-illustration-policy.md`
- `.claude/skills/write-russian/SKILL.md`
- `.claude/skills/_shared/illustration-policy.md`, `russian-style.md`, `README.md`
- `.claude/skills/autodoc/SKILL.md`, `.autodoc/`
- `.claude/agents/wiki-source-researcher.md`
- `.claude/skills/wiki-quiz/SKILL.md` (defer to next cycle)
- `raw/**`, `publish/**`

---

## Task 1: Create `wiki/` subdirectories with `.gitkeep`

**Files:**
- Create: `wiki/papers/.gitkeep`, `wiki/lectures/.gitkeep`, `wiki/clips/.gitkeep`, `wiki/knowledge-sharings/.gitkeep`
- Remove: existing `wiki/.gitkeep` (replaced by per-subdir placeholders).

- [ ] **Step 1: Create the subdirectories and placeholders**

```bash
cd /Users/syakubson/Desktop/Claude_code/SBER/knowledge_sharing_wiki
mkdir -p wiki/papers wiki/lectures wiki/clips wiki/knowledge-sharings
touch wiki/papers/.gitkeep wiki/lectures/.gitkeep wiki/clips/.gitkeep wiki/knowledge-sharings/.gitkeep
git rm wiki/.gitkeep
```

- [ ] **Step 2: Verify**

```bash
find wiki -type d -mindepth 1
ls wiki/papers/ wiki/lectures/ wiki/clips/ wiki/knowledge-sharings/
```

Expected: 4 subdirectories, each containing only `.gitkeep`.

- [ ] **Step 3: Commit**

```bash
git add wiki/
git commit -m "refactor(wiki): scaffold source_kind subdirectories"
```

---

## Task 2: Create `wiki/index.md` skeleton

**Files:**
- Create: `wiki/index.md`

- [ ] **Step 1: Write the file**

```markdown
---
title: Wiki Index
ingested: 2026-05-18
---

# Wiki Index

_Last updated: 2026-05-18_

Эта страница — карта всех разборов. Обновляется при каждом `/wiki-ingest`.

## Recent ingests (last 10)

<!-- empty: пока нет разборов -->

## Papers

<!-- empty -->

## Lectures

<!-- empty -->

## Clips

<!-- empty -->

## Knowledge Sharings (newest first)

<!-- empty -->

## By tag

<!-- empty -->
```

- [ ] **Step 2: Verify**

```bash
wc -l wiki/index.md
head -5 wiki/index.md
```

Expected: ~25 lines, starts with `---` frontmatter.

- [ ] **Step 3: Commit**

```bash
git add wiki/index.md
git commit -m "feat(wiki): seed wiki/index.md skeleton"
```

---

## Task 3: Create `wiki/log.md` skeleton

**Files:**
- Create: `wiki/log.md`

- [ ] **Step 1: Write the file**

```markdown
---
title: Wiki Log
ingested: 2026-05-18
---

# Wiki Log

Append-only chronological log. Each `/wiki-ingest`, `/wiki-lint`, and substantive
refactor appends one entry. Past entries are not edited — corrections are added
as new entries.

Entry format:

```
## [YYYY-MM-DD] <verb> | <short title>

- **What:** <one-line description>
- **Page(s) touched:** [[<kind>/<slug>]]
- **Notes:** <optional — open questions, contradictions, things to revisit>
```

Verbs: `ingest`, `query`, `lint`, `refactor`.

---
```

- [ ] **Step 2: Verify**

```bash
wc -l wiki/log.md
```

Expected: ~22 lines.

- [ ] **Step 3: Commit**

```bash
git add wiki/log.md
git commit -m "feat(wiki): seed wiki/log.md skeleton"
```

---

## Task 4: Rewrite `.claude/rules/04-frontmatter-schema.md`

**Files:**
- Rewrite: `.claude/rules/04-frontmatter-schema.md`

- [ ] **Step 1: Replace contents entirely**

```markdown
# Frontmatter Schema

This rule auto-loads. `wiki-lint` enforces it. Every wiki page starts with YAML frontmatter matching the schema below.

## Base fields (paper / lecture / clip)

```yaml
---
title: <Plain title in English>
source_kind: paper | lecture | clip
source_path: raw/<kind>/<file>
source_date: YYYY-MM-DD
ingested: YYYY-MM-DD
authors: [<First Last>, <First Last>]
tags: [<tag1>, <tag2>, ...]
status: stub | draft | mature
---
```

## Knowledge-sharing fields

```yaml
---
title: <KS topic>
source_kind: knowledge-sharing
source_path: raw/knowledge-sharings/<file>
source_date: YYYY-MM-DD
ingested: YYYY-MM-DD
presenter: <First Last>
audience: <team | internal | public>
slides: <URL or relative path>
tags: [<tag1>, ...]
status: stub | draft | mature
---
```

`slides` and `audience` are optional. `presenter` replaces `authors` for KS.

## Field rules

- `title` — English, plain. No prefixes like «Paper:».
- `source_kind` — one of: `paper`, `lecture`, `clip`, `knowledge-sharing`. New kinds require an explicit spec change.
- `source_path` — relative to repo root. Must point at an existing file under `raw/`.
- `source_date` — date the source was published (arxiv submission, lecture recording, blog publication, KS meeting).
- `ingested` — when the breakdown was written. Bumped on substantive edits, not typo fixes.
- `authors` — array. For lectures and clips too (`[Andrej Karpathy]`, `[Jay Alammar]`).
- `tags` — lowercase kebab-case, plural where natural (`transformers`, not `transformer`). 3-7 tags per page. All tags must be in the whitelist below.
- `status`:
  - `stub` — TL;DR and Мотивация only, the rest is empty or missing.
  - `draft` — all required sections filled.
  - `mature` — user reviewed and approved.

## Tag whitelist

Starter set. Authors extend this list in the same commit that introduces the first page using a new tag.

```
attention
positional-encoding
normalization
optimization
regularization
generative-models
diffusion
flow-matching
variational-inference
distillation
tokenization
inference-economics
training-dynamics
```

`wiki-lint` rejects unknown tags.

## Slug rules

| `source_kind` | Pattern | Example |
|---|---|---|
| paper | `<first-author>-<year>-<short-title>.md` | `su-2021-roformer.md` |
| lecture | `<lecturer>-<short-title>.md` | `karpathy-makemore-3.md` |
| clip | `<short-title>-<author>.md` | `illustrated-transformer-jay-alammar.md` |
| knowledge-sharing | `YYYY-MM-DD-<topic>-by-<presenter>.md` | `2026-05-15-attention-deep-dive-by-grigoriy.md` |

Lowercase, kebab-case, no spaces.

## Validation rules (enforced by `wiki-lint`)

1. Every file under `wiki/{papers,lectures,clips,knowledge-sharings}/` starts with `---` on line 1.
2. All base fields present and non-empty.
3. `source_kind` matches the enclosing directory (`wiki/papers/*.md` has `source_kind: paper`).
4. `source_path` exists under `raw/`.
5. `source_date` ≤ `ingested`.
6. `tags` non-empty, all in the whitelist.
7. `status` is one of: `stub`, `draft`, `mature`.
8. `authors` is non-empty for paper/lecture/clip; `presenter` is present for knowledge-sharing.
9. Slug matches the pattern for the file's `source_kind`.
```

- [ ] **Step 2: Verify**

```bash
wc -l .claude/rules/04-frontmatter-schema.md
```

Expected: 80-110 lines.

- [ ] **Step 3: Commit**

```bash
git add .claude/rules/04-frontmatter-schema.md
git commit -m "feat(rules): rewrite 04-frontmatter-schema for source-breakdowns model"
```

---

## Task 5: Rewrite `.claude/skills/_shared/page-templates.md`

**Files:**
- Rewrite: `.claude/skills/_shared/page-templates.md`

- [ ] **Step 1: Replace contents entirely**

The new file has 3 parts: Template A (paper/lecture/clip), KS variant, and the preserved cross-cutting sections (term-introduction, formula annotation, code-formula bridge).

```markdown
# Page Templates

Read this in `wiki-ingest` phase 5. The wiki has **one canonical template** — Template A (Motivation-first) — used for every paper, lecture, and clip breakdown. Knowledge sharings use a variant with extra frontmatter fields and one optional section. All cross-cutting writing rules (term introduction, formula annotation, code-formula bridge) at the end apply to every template.

---

## Template A — Source breakdown (paper / lecture / clip)

The page belongs in `wiki/{papers,lectures,clips}/<slug>.md` per the slug rules in `rules/04-frontmatter-schema.md`.

```markdown
---
title: <Plain title in English>
source_kind: paper | lecture | clip
source_path: raw/<kind>/<file>
source_date: YYYY-MM-DD
ingested: YYYY-MM-DD
authors: [<First Last>, ...]
tags: [<tag1>, <tag2>, ...]
status: stub | draft | mature
---

# {Plain title}

> {TL;DR — 1-3 sentences in Russian. What the source shows, in plain language.
> The reader knows in 5 seconds: relevant to me or not.}

## Мотивация

{2-4 paragraphs of motivated build-up:
1. What we want (from positional encoding, attention, training, etc.).
2. The naive or previous approach.
3. Why it fails — concretely, what's the failure mode.
4. What this source proposes, in one sentence (no details yet).}

## Идея в одной картинке

{One figure — mermaid diagram or matplotlib PNG. The single most important
visualisation. Under it: caption + one paragraph of commentary explaining
what the figure shows and why it is the key.}

## Как это работает

{Details. Subsections are dictated by content. Typical subsections below.}

### Математика

{Formulas in LaTeX (`$...$`, `$$...$$`). Each non-trivial formula is followed
by a `где: ...` list explaining every symbol.}

### Pseudocode / Python

{3-6 lines per snippet. Variable names in English, comments in Russian.}

### Иллюстрация второго порядка

{Optional — if there are detail diagrams beyond the «Идея в одной картинке».}

## Вывод

{1-3 sentences. What the reader takes away after reading «Как это работает».
Not a repeat of TL;DR — by now the reader understands *why*.}

## Источник

- **`{source_path}`** ({source_kind}, {source_date})
- URL: {arxiv / DOI / blog link}
- Authors: {First Last et al.}
```

### Optional sections (insert between «Как это работает» and «Вывод»)

```markdown
## Результаты

{Papers with empirics only. 3-7 bullets with concrete numbers and benchmark
names. No vague «significant improvement» — specifics mandatory.}

## Сравнение с альтернативами

{2-4 bullets. Each: «X differs from <related method> in that …».}

## Ограничения

{Critical view: what the source omits, where it breaks, what it was not
tested on. This is the author-of-breakdown's section, not a retelling.}

## Открытые вопросы

- {Unresolved threads after reading.}
- {Experiments worth running.}

## Связанные разборы

- [[papers/<other-slug>]] — {one-line: why related}
- [[lectures/<other-slug>]] — {one-line}
```

**If an optional section has no content — it is absent**, not left as an empty header.

---

## Template B — Knowledge sharing variant

Same shape as Template A, with these deltas:

**Frontmatter:** replace `authors:` with `presenter:`, add optional `audience:` and `slides:`.

```yaml
---
title: <KS topic>
source_kind: knowledge-sharing
source_path: raw/knowledge-sharings/<file>
source_date: YYYY-MM-DD                      # date of the meeting
ingested: YYYY-MM-DD
presenter: <First Last>
audience: <team | internal | public>         # optional
slides: <URL or relative path>               # optional
tags: [<tag1>, ...]
status: stub | draft | mature
---
```

**Additional optional section** (insert before «Открытые вопросы»):

```markdown
## Q&A и обсуждение

- {Notable question + the answer / discussion that followed}
- {...}
```

Everything else (required sections, cross-cutting rules) is identical to Template A.

---

## Cross-cutting rules (apply to every template)

### Term introduction (first mention)

Every technical term gets a **one-line definition + everyday analogy** on its first mention. After that, the term is used plainly.

Format:

> **`<термин>`** (`<English original>`, if relevant) — это `<plain Russian definition>`. Можно представить как `<everyday-life analogy>`: `<one or two strokes of concrete detail>`.

Rules:

- **Bold** the term at first mention.
- One short sentence of plain-Russian definition right after the bold.
- One analogy from everyday adult life (post office, library, customs, train timetable, electric kettle). Avoid analogies that themselves need analogies (don't say «это как middleware» if the reader doesn't know middleware).
- After first mention, use plain. No re-definition further down the page.
- Applies to ML terms, math objects, dataset names (Telco Churn, MNIST), magic numbers in code (`random_state=42`, `test_size=0.2`) on first appearance.

Example:

> **Attention sink** — это феномен, когда несколько позиций (обычно первый токен или знаки препинания) собирают на себя непропорционально большой attention-вес почти во всех heads. Можно представить как **общая корзина «прочее»** в магазинной выкладке: товары, которые никуда не подошли, скапливаются в одном месте — но не потому что они особенно важны, а потому что больше некуда положить.

### Formula symbol annotation (`где: ...`)

Every non-trivial formula is followed by a `где: ...` list explaining each symbol. No exceptions.

Format:

> $\hat{y} = w_1 x_1 + w_2 x_2 + \ldots + w_n x_n + b$
>
> где:
> - $\hat{y}$ — предсказание модели
> - $x_1, x_2, \ldots, x_n$ — значения признаков объекта
> - $w_1, w_2, \ldots, w_n$ — веса модели, которые подбираются при обучении
> - $b$ — свободный член (intercept), смещение по вертикали
> - $n$ — количество признаков

Rules:

- Applies to LaTeX block formulas (`$$…$$`) and to inline formulas with non-trivial symbols (Σ, ∫, σ, α, β, ∇, indexed sums).
- Naked arithmetic (`x = 5 + 3`) — no `где` needed.
- If a Greek letter is used, name it once: «$\alpha$ — альфа, темп обучения».
- For indexed sums, state the index range.

### Code-formula bridge

Non-trivial math gets a short Python or pseudocode snippet (3-6 lines) that turns the formula into runnable code. Applies to loss functions, gradient computation, sigmoid / softmax, entropy / Gini, metric definitions.

Example:

```python
# MSE — средний квадрат ошибки
def mse(y_true, y_pred):
    return ((y_true - y_pred) ** 2).mean()

# Sigmoid
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
```

Rules:

- One concept = one snippet. No stuffing loss + gradient + update into one block.
- Pseudocode is fine when full Python distracts from the idea.
- Variable names in English, comments in Russian (`rules/01` and `write-russian` §9.3).
- Code blocks ≤ 10 lines by default.

### Other conventions

- All frontmatter follows `rules/04-frontmatter-schema.md`.
- Prose body is Russian; headings, slugs, frontmatter values are English (`rules/01-language-policy.md`).
- `[[wiki-link]]` syntax for internal references; the link path is `<kind>/<slug>` (e.g., `[[papers/su-2021-roformer]]`).
- No marketing voice, no AI-speak, no faux-warmth. Run the `write-russian` editing checklist before commit (`rules/01-language-policy.md` lists the banned phrases inline).
- Page length: dictated by content, no hard target. Long lectures may need 1500+ words; a short clip may fit in 400.
```

- [ ] **Step 2: Verify**

```bash
wc -l .claude/skills/_shared/page-templates.md
```

Expected: 180-260 lines.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/_shared/page-templates.md
git commit -m "feat(skills): rewrite page-templates for source-breakdowns model"
```

---

## Task 6: Rewrite `.claude/skills/wiki-ingest/SKILL.md`

**Files:**
- Rewrite: `.claude/skills/wiki-ingest/SKILL.md`

- [ ] **Step 1: Replace contents entirely**

````markdown
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
````

- [ ] **Step 2: Verify**

```bash
wc -l .claude/skills/wiki-ingest/SKILL.md
head -5 .claude/skills/wiki-ingest/SKILL.md
grep -nE "^## " .claude/skills/wiki-ingest/SKILL.md
```

Expected: 140-200 lines; YAML frontmatter on top; 8 phase headers + gates section.

- [ ] **Step 3: Commit**

```bash
git add .claude/skills/wiki-ingest/SKILL.md
git commit -m "feat(skill): rewrite wiki-ingest for one-source-one-page flow"
```

---

## Task 7: Update `.claude/skills/wiki-lint/SKILL.md`

**Files:**
- Modify: `.claude/skills/wiki-lint/SKILL.md`

The existing skill validated the old 6-type schema. Update it for the new schema. Most of the lint logic (orphan detection, broken-link detection, frontmatter validation pass) is preserved; only the schema definitions and globs change.

- [ ] **Step 1: Read the current file**

```bash
cat .claude/skills/wiki-lint/SKILL.md
```

- [ ] **Step 2: Update pre-flight section**

Replace the existing pre-flight with:

```markdown
## Pre-flight

- [ ] Read `.claude/role.md`
- [ ] Read `.claude/rules/04-frontmatter-schema.md`
```

- [ ] **Step 3: Update inventory step**

Find any reference to the old taxonomy (`ml_concepts`, `math_concepts`, `methods`, `topics`, `sources`, `questions`). Replace with:

```markdown
## Inventory

Scan all pages under:

- `wiki/papers/**/*.md`
- `wiki/lectures/**/*.md`
- `wiki/clips/**/*.md`
- `wiki/knowledge-sharings/**/*.md`

(`wiki/index.md` and `wiki/log.md` follow their own minimal schema and are not lint targets in this version.)
```

- [ ] **Step 4: Replace frontmatter validation**

Replace any inlined field rules with a one-liner: «Frontmatter rules are in `.claude/rules/04-frontmatter-schema.md`. Enforce all 9 validation rules from that file.»

Then list the specific lint checks the skill performs:

```markdown
## Lint checks

1. **Frontmatter present** — file starts with `---` on line 1; ends with `---` before body.
2. **All base fields present** — `title`, `source_kind`, `source_path`, `source_date`, `ingested`, `authors` (or `presenter` for KS), `tags`, `status`.
3. **`source_kind` matches directory** — `wiki/papers/*.md` has `source_kind: paper`, etc.
4. **`source_path` exists** — referenced file under `raw/` resolves.
5. **`source_date` ≤ `ingested`** — chronological sanity.
6. **`tags` non-empty and all in whitelist** — read whitelist from `rules/04`, flag unknown tags.
7. **`status` is one of: `stub`, `draft`, `mature`**.
8. **For KS pages: `presenter` is present**, `authors` is absent.
9. **Slug pattern matches `source_kind`** — see `rules/04` slug table.
10. **No broken `[[wiki-links]]`** — link target file exists under `wiki/`.
11. **No orphan pages** — every page is reachable from `wiki/index.md`.
12. **Tag-index consistency** — every page's tags appear in the `By tag` section of `wiki/index.md`.
```

- [ ] **Step 5: Verify**

```bash
wc -l .claude/skills/wiki-lint/SKILL.md
grep -c "ml_concept\|math_concept\|method\|topic\|source\|question" .claude/skills/wiki-lint/SKILL.md
```

Expected: first command shows the new line count; second command shows 0 matches (or only matches in unrelated context, like the word "method" appearing in prose).

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/wiki-lint/SKILL.md
git commit -m "docs(skill): wiki-lint enforces new source-breakdowns schema"
```

---

## Task 8: Update `.claude/skills/wiki-query/SKILL.md`

**Files:**
- Modify: `.claude/skills/wiki-query/SKILL.md`

Update the query strategy to use tag-based search instead of concept-page lookup.

- [ ] **Step 1: Read the current file**

```bash
cat .claude/skills/wiki-query/SKILL.md
```

- [ ] **Step 2: Update pre-flight**

```markdown
## Pre-flight

- [ ] Read `.claude/role.md`
- [ ] Read `wiki/index.md` — the by-tag section is the entry point for concept queries.
```

- [ ] **Step 3: Replace the search strategy section**

Find any section describing how to locate relevant pages. Replace with:

```markdown
## Search strategy

1. **Parse the question** — identify the concept(s) the user is asking about (e.g., "How does RoPE handle long contexts?" → concept = `positional-encoding`, secondary = `attention`).
2. **Match tags** — open `wiki/index.md`, find the «By tag» section, locate the line for the relevant tag(s). It lists every breakdown that mentions the concept.
3. **Read relevant breakdowns** — open the matching `wiki/<kind>/<slug>.md` pages in priority order: papers that introduce the concept first, then lectures, then clips, then knowledge-sharings.
4. **Synthesize the answer** — combine findings across pages, cite each claim with `[[<kind>/<slug>]]`. State which page contributed which piece. If sources disagree, note both positions with attribution.
5. **Suggest next reads** — if the user might benefit from a related concept, end with «Если хочешь глубже — см. [[<related-page>]]».
```

- [ ] **Step 4: Verify**

```bash
wc -l .claude/skills/wiki-query/SKILL.md
```

Expected: similar to original length (small net change).

- [ ] **Step 5: Commit**

```bash
git add .claude/skills/wiki-query/SKILL.md
git commit -m "docs(skill): wiki-query uses tag-based navigation"
```

---

## Task 9: Update `.claude/role.md`

**Files:**
- Modify: `.claude/role.md`

Drop the «Where new pages live» section (old layout) and replace with a tight description of the new 4-folder layout.

- [ ] **Step 1: Read current file**

```bash
cat .claude/role.md
```

- [ ] **Step 2: Replace the «Where new pages live» section**

Find the section that lists 6 types (ml_concepts, math_concepts, methods, topics, sources, questions). Replace the entire section with:

```markdown
## Where new pages live

One page per source. The page lives in `wiki/<source_kind>/<slug>.md`:

- `wiki/papers/<first-author>-<year>-<short-title>.md` — for arxiv papers and similar.
- `wiki/lectures/<lecturer>-<short-title>.md` — for recorded lectures and talks.
- `wiki/clips/<short-title>-<author>.md` — for blog posts, articles, web clips.
- `wiki/knowledge-sharings/YYYY-MM-DD-<topic>-by-<presenter>.md` — for internal knowledge-sharing meetings.

You do not maintain central concept pages. Concepts live inside the breakdown of the source that introduced them. Cross-source navigation goes through tags in frontmatter and the `By tag` section of `wiki/index.md`.

If a single concept is so deeply re-examined across 5+ breakdowns that a synthesis page becomes valuable — flag it as an open question (in `wiki/questions/` if it exists, or inline on the current page). Do not create central concept pages unilaterally; that decision is a deliberate user-driven change in policy.
```

- [ ] **Step 3: Verify**

```bash
wc -l .claude/role.md
grep -n "ml_concepts\|math_concepts\|<top>" .claude/role.md
```

Expected: ≤ 100 lines; 0 matches for old taxonomy.

- [ ] **Step 4: Commit**

```bash
git add .claude/role.md
git commit -m "docs(role): describe the source-breakdowns layout"
```

---

## Task 10: Update `CLAUDE.md`

**Files:**
- Modify: `CLAUDE.md`

Update the «Layout» block to show the new 4-folder structure.

- [ ] **Step 1: Read current file**

```bash
cat CLAUDE.md
```

- [ ] **Step 2: Replace the «Layout» block**

Find the layout code block under `## Layout`. Replace the wiki/ branch with:

```
├── wiki/                 # source breakdowns: one page per paper/lecture/clip/KS
│   ├── index.md          # recent ingests, alphabetical-by-kind, by-tag
│   ├── log.md            # chronological event log
│   ├── papers/           # paper breakdowns
│   ├── lectures/         # lecture breakdowns
│   ├── clips/            # blog/article breakdowns
│   ├── knowledge-sharings/   # internal KS meeting breakdowns
│   └── static/figures/   # matplotlib .py+.png and source cut-outs per page
```

- [ ] **Step 3: Verify**

```bash
wc -l CLAUDE.md
grep -n "ml_concepts\|math_concepts\|<top>" CLAUDE.md
```

Expected: ≤ 100 lines; 0 matches for old taxonomy.

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "docs(claude): update layout block for source-breakdowns model"
```

---

## Task 11: Update `ONBOARDING.md`

**Files:**
- Modify: `ONBOARDING.md`

Replace the «Structure quick map» section and add a worked-example pointer.

- [ ] **Step 1: Read current file**

```bash
cat ONBOARDING.md
```

- [ ] **Step 2: Replace the «Structure quick map» section**

Find the structure code block. Replace with:

```markdown
## Structure quick map

```
wiki/papers/             # paper breakdowns:  su-2021-roformer.md
wiki/lectures/           # lecture breakdowns: karpathy-makemore-3.md
wiki/clips/              # blog/article breakdowns: illustrated-transformer-jay-alammar.md
wiki/knowledge-sharings/ # KS meeting breakdowns: 2026-05-15-attention-deep-dive-by-grigoriy.md
wiki/index.md            # entry point: recent / by kind / by tag
wiki/log.md              # append-only chronological event log
```

One page per source. Concepts live *inside* the breakdown; there are no separate concept pages.

To find «everything about RoPE», open `wiki/index.md`, scroll to «By tag», find the line for `positional-encoding`. It lists every breakdown that touches the concept.

## Worked example

See `docs/superpowers/specs/2026-05-18-wiki-source-breakdowns-design.md` §9 for a full example of a paper breakdown (the RoFormer/RoPE paper). It shows the template on a real source — what each section actually looks like, what kind of mermaid diagram qualifies as «идея в одной картинке», how `где: …` lists work under formulas, how «Связанные разборы» links work.
```

- [ ] **Step 3: Verify**

```bash
wc -l ONBOARDING.md
```

Expected: 90-180 lines.

- [ ] **Step 4: Commit**

```bash
git add ONBOARDING.md
git commit -m "docs(onboarding): update for source-breakdowns model, point to worked example"
```

---

## Task 12: Quartz build smoke

- [ ] **Step 1: Build**

```bash
cd publish && npx quartz build 2>&1 | tee /tmp/quartz-build.log && cd ..
```

Expected: exit code 0, message «Emitted N files to `public`».

- [ ] **Step 2: Scan for broken-link warnings**

```bash
grep -i "broken\|not found\|missing" /tmp/quartz-build.log | head -20
```

Expected: 0 warnings about wiki pages (some Quartz internal warnings about untracked-in-git source files are pre-existing and acceptable).

- [ ] **Step 3: No commit** — build artefacts are gitignored.

---

## Task 13: Skill load smoke

- [ ] **Step 1: List skills**

```bash
ls .claude/skills/
```

Expected: contains `wiki-ingest`, `wiki-lint`, `wiki-query`, `wiki-quiz`, `autodoc`, `write-russian`, `_shared`.

- [ ] **Step 2: Verify each SKILL.md has frontmatter**

```bash
for f in .claude/skills/*/SKILL.md; do
  head -1 "$f" | grep -q "^---" && echo "OK: $f" || echo "MISSING FM: $f"
done
```

Expected: all `OK:` lines, no `MISSING FM:` lines.

- [ ] **Step 3: Verify pre-flight reads in wiki-ingest**

```bash
grep -nE "^- \[ \] Read " .claude/skills/wiki-ingest/SKILL.md
```

Expected: 7 lines listing the 7 pre-flight reads (role.md, page-templates.md, russian-style.md, illustration-policy.md, rules/04, wiki/index.md, .autodoc/index.md).

- [ ] **Step 4: No commit** — purely a sanity check.

---

## Task 14: End-to-end ingest verification (deferred to user)

The final acceptance test: run `/wiki-ingest` on one real source from `raw/` to validate the whole flow.

This task is **user-driven** — not automated. The branch is ready for the user to invoke `/wiki-ingest raw/papers/<file>` or any other source they care about and verify that:

- [ ] Phase 1 pre-flight reads all 7 files without error.
- [ ] Phase 2 reads the source.
- [ ] Phase 4 emits the plan block (Source / Target page / TL;DR draft / Tags / Motivation arc / Key idea / Optional sections / Related).
- [ ] After user approval, Phase 5 writes one page at `wiki/<kind>/<slug>.md` with valid frontmatter and all required sections.
- [ ] Phase 6 produces at least one illustration; mermaid renders in local Quartz preview, or matplotlib `.py + .png` lives at `wiki/static/figures/<slug>/`.
- [ ] Phase 7 self-check runs `/write-russian` over the page.
- [ ] Phase 8 updates `wiki/index.md` and appends to `wiki/log.md`.
- [ ] Proposed commit message follows `rules/02` and the page passes `/wiki-lint`.

No automation in this plan — the test happens when the user is ready and chooses a source.

---

## Definition of Done

```
[ ] Branch wiki-overhaul, ≥ 11 new commits since the spec commit (one per implementation task)
[ ] All commits ≤ 300 lines
[ ] wiki/{papers,lectures,clips,knowledge-sharings}/.gitkeep exist
[ ] wiki/index.md exists with skeleton
[ ] wiki/log.md exists with skeleton
[ ] .claude/rules/04-frontmatter-schema.md rewritten with new schema + tag whitelist
[ ] .claude/skills/_shared/page-templates.md has Template A, Template B (KS variant), and cross-cutting rules
[ ] .claude/skills/wiki-ingest/SKILL.md has 8 phases for one-page flow
[ ] .claude/skills/wiki-lint/SKILL.md enforces new schema
[ ] .claude/skills/wiki-query/SKILL.md uses tag-based navigation
[ ] .claude/role.md describes 4-folder layout
[ ] CLAUDE.md layout block reflects new structure
[ ] ONBOARDING.md points to the worked example in the spec
[ ] cd publish && npx quartz build exits 0 with no new broken-link warnings
[ ] Skill load smoke (Task 13) green
[ ] No occurrences of "ml_concepts", "math_concepts", "<top>/<sub>", or "needs_rewrite" remain in .claude/ or root *.md (except in this plan and the spec, which document the change)
[ ] git push was NOT executed at any point
```

---

## Self-review (executed against the spec)

**Spec coverage check:**

| Spec section | Spec item | Covered by |
|---|---|---|
| §1 | New `wiki/` 4-folder structure | Task 1 |
| §1 | Template A required + optional sections | Task 5 |
| §1 | Frontmatter schema with `source_kind`, `source_path`, `tags`, `status`, etc. | Task 4 |
| §1 | Tag whitelist enforcement | Task 4 (whitelist), Task 7 (lint) |
| §1 | `wiki/index.md` with by-tag groups | Tasks 2, 6 (ingest maintains it) |
| §1 | Skill updates for wiki-ingest, wiki-lint, wiki-query | Tasks 6, 7, 8 |
| §1 | `_shared/page-templates.md` rewrite | Task 5 |
| §1 | CLAUDE.md, ONBOARDING.md, role.md updates | Tasks 9, 10, 11 |
| §2 | Directory layout exact tree | Tasks 1, 10 |
| §2 | Slug naming patterns by source_kind | Task 4 |
| §2 | `wiki/index.md` structure with Recent / by-kind / by-tag | Tasks 2, 6 |
| §3 | Template A required + optional sections | Task 5 |
| §3 | Cross-cutting (term-introduction, formula annotation, code-formula bridge) | Task 5 |
| §4 | Base frontmatter fields | Task 4 |
| §4 | KS variant frontmatter | Tasks 4, 5 |
| §4 | Field rules | Task 4 |
| §4 | Tag whitelist | Task 4 |
| §4 | Validation rules | Tasks 4, 7 |
| §5 | Tag-based navigation in wiki-query | Task 8 |
| §6 | Skill rewrites, role/CLAUDE/ONBOARDING updates | Tasks 6, 7, 8, 9, 10, 11 |
| §7 | Verification smoke tests | Tasks 12, 13, 14 |
| §9 | Worked example referenced from ONBOARDING | Task 11 |

**Gaps:** none — every spec requirement maps to at least one task.

**Placeholder scan:** spec'd new content is provided verbatim in every task; no «TODO», «TBD», «fill in details», «implement later» appear in this plan. Task 14 is explicitly user-driven and labelled as such.

**Type consistency check:** all file paths use the same form throughout (e.g., `wiki/papers/<slug>.md`, `.claude/rules/04-frontmatter-schema.md`). Field names match across tasks (`source_kind`, `source_path`, `source_date`, `ingested`, `authors`, `tags`, `status`, `presenter`, `audience`, `slides`). Slug patterns are referenced consistently between Task 4 (definition) and Task 7 (enforcement).
