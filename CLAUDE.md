# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This repository is a personal **Obsidian vault** of ML/DL/CS study notes, written in Russian prose with English technical terms, plus a vendored **Quartz** pipeline that publishes the vault as a website. The Obsidian vault root is the repository root (`.obsidian/` lives here), so `wiki/` and `images/` are both folders *inside* one vault.

## Repository layout

- `wiki/` — the notes, grouped into topic folders (`gen-ai/`, `transformer-primitives/`, `distillation/`, `applied/`, `system-design/`). Markdown notes plus a few source `.pdf` lectures. This is the published content root.
- `images/` — figure/GIF attachments in per-topic subfolders (`ddpm/`, `detr/`, `rope_images/`, `energy-based-models/`). **Target location is `wiki/images/`** — see *Publishing* for why and the pending migration.
- `publish/` — vendored Quartz v4 static-site generator. `publish/content` is a symlink → `../wiki`.
- `.claude/skills/` — `wiki-query` and `wiki-quiz` (see *Skills*).
- `.obsidian/` — Obsidian app config; gitignored.

## Authoring conventions

**Language.** Note prose is Russian. Keep established technical terms in English without transliteration (`attention`, `self-attention`, `embedding`). Everything code-related — identifiers, file paths, frontmatter keys — is English.

**Line length.** Do **not** manually wrap prose. Obsidian soft-wraps at display time, so source-level line breaks inside a paragraph only clutter diffs.

**Frontmatter.** Notes use `Created` (ISO timestamp), `Reviewed` (`Done` / `Doing` / `Todo`), and optional `Keywords` (a YAML list). Quartz reads this frontmatter (`defaultDateType: "modified"`).

**Image embeds.** Use Obsidian wikilink embeds `![[...]]`. **Always path-qualify** as `![[images/<topic>/<file>]]` — bare basenames (`![[image 1.png]]`) collide because many figures share names (`image.png`, `image 1.png`) across topic folders, so they resolve unpredictably.

**Math notation.** All mathematical notation goes in **LaTeX**, never in backticks. Inline math `$...$`, display math `$$...$$`. This covers any symbol, expression, set/function notation — even a single Greek letter or one subscripted variable. Backticks are reserved for code identifiers (function names, module paths, parameter names, type names, file paths, library names).

Bad (math in backticks) → Good (LaTeX):

- `t_0 < t_1 < ... < t_N` → $t_0 < t_1 < \ldots < t_N$
- `s, t ∈ [0,σ]` → $s, t \in [0, \sigma]$
- `f_θ(x,t) = c_skip(t)·x + c_out(t)·F_θ(x,t)` → $f_\theta(x, t) = c_{\text{skip}}(t) \cdot x + c_{\text{out}}(t) \cdot F_\theta(x, t)$
- `x_0`, `f_θ`, `Δ = s - t` → $x_0$, $f_\theta$, $\Delta = s - t$

Convert Unicode math inside backticks to LaTeX commands (`σ`→`\sigma`, `·`→`\cdot`, `∈`→`\in`, `≤`→`\leq`, `→`→`\to`). Multi-letter subscripts use `_{\text{...}}` for upright font (`c_{\text{skip}}`); single-letter subscripts go bare (`x_t`, `f_\theta`).

## Publishing (Quartz → Vercel)

`publish/` is Quartz v4 (`jackyzha0/quartz`). It builds the notes under `publish/content` (→ `../wiki`) into a static site, deployed to **Vercel** at `ml-notes-wiki.vercel.app` (`publish/vercel.json` sets `cleanUrls`, so `/foo` serves `foo.html`). Requires **Node ≥ 22** (`.node-version` pins v22.16.0).

```bash
cd publish
npx quartz build --serve   # local preview at http://localhost:8080 (live reload)
npx quartz build           # one-off build → publish/public/ (gitignored)
npm run check              # tsc + prettier check (only when editing Quartz internals)
```

Site config is `publish/quartz.config.ts` (title, `baseUrl`, `locale: ru-RU`, plugin pipeline incl. KaTeX, Obsidian-flavored markdown, OG images); layout/components are `publish/quartz.layout.ts`.

**Hard constraint — assets must live under the content root.** Quartz only emits files found under `wiki/`. Anything outside it (today's repo-root `images/`) is never copied to the build and its embeds 404 on the published site. This is why attachments must move to `wiki/images/` and embeds must point there.

**Migration pending.** The vault was restructured but the publish setup was not updated: images still sit at repo-root `images/`, several `rope.md` embeds are cross-wired to the wrong topic folder, and the `wiki/index.md` landing page was deleted. The redo is specified in `docs/plans/2026-06-20-publish-redo.md`. Until it lands, the published site is missing all figures and a home page.

## Skills

- `wiki-query` — answer a question against the wiki: read the index, drill into pages, synthesize with `[[wiki-link]]` citations.
- `wiki-quiz` — generate quizzes (MCQ, open, solve-on-paper) from wiki pages; always clarifies format/scope/difficulty/count first.

Both skills start by reading **`wiki/index.md`** as the page index. That file is currently missing (deleted in the restructure); restoring it — part of the migration above — is what makes the skills work.
