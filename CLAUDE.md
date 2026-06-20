This repository is a personal **Obsidian vault** of ML/DL/CS study notes, written in Russian prose with English technical terms. The Obsidian vault root is the repository root (`.obsidian/` lives here), so the notes in `wiki/` and their figures in `wiki/images/` are all part of one vault.

## Repository layout

- `wiki/` — the notes, grouped into topic folders (`gen-ai/`, `transformer-primitives/`, `distillation/`, `applied/`, `system-design/`). Markdown notes plus a few source `.pdf` lectures. This is the published content root.
- `wiki/images/` — figure/GIF attachments in per-topic subfolders (`ddpm/`, `detr/`, `rope_images/`, `energy-based-models/`). Lives under the content root so Quartz emits them (see `publish/CLAUDE.md`).
- `publish/` — vendored Quartz v4 static-site generator (`publish/content` is a symlink → `../wiki`); see `publish/CLAUDE.md`.
- `styleguide.md` — the canonical guide for writing notes (voice, structure, derivation arc, math notation). See *Authoring conventions*.
- `.claude/skills/` — `wiki-query` and `wiki-quiz` (see *Skills*).
- `.obsidian/` — Obsidian app config; gitignored.

## Authoring conventions

> [!important]
> **Before creating or editing ANY note under `wiki/`, you MUST read `styleguide.md` (at the repository root) first — every time, even for a one-line edit.** It is the canonical reference for note language, the derivation arc, structure, math notation, figures, and what to clean up on import. The conventions below are the low-level mechanics; `styleguide.md` is the full picture and takes precedence. This is not optional.

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

## Publishing

The vault is published as a website with a **Quartz → Vercel** toolchain living in `publish/`. Build mechanics, config, and the assets-under-content-root constraint are documented in **`publish/CLAUDE.md`**.

## Skills

- `wiki-query` — answer a question against the wiki: read the index, drill into pages, synthesize with `[[wiki-link]]` citations.
- `wiki-quiz` — generate quizzes (MCQ, open, solve-on-paper) from wiki pages; always clarifies format/scope/difficulty/count first.

Both skills start by reading **`wiki/index.md`** as the page index.
