This repository is a personal **Obsidian vault** of ML/DL/CS study notes, written in Russian prose with English technical terms. The Obsidian vault root is the repository root (`.obsidian/` lives here), so the notes in `wiki/` and their figures in `wiki/images/` are all part of one vault.

## Repository layout

- `wiki/` — the notes, grouped into topic folders (`gen-ai/`, `transformer-primitives/`, `distillation/`, `applied/`, `system-design/`). Markdown notes plus a few source `.pdf` lectures. This is the published content root.
- `wiki/images/` — figure/GIF attachments in per-topic subfolders (`ddpm/`, `detr/`, `rope_images/`, `energy-based-models/`). Lives under the content root so Quartz emits them (see `publish/CLAUDE.md`).
- `publish/` — vendored Quartz v4 static-site generator (`publish/content` is a symlink → `../wiki`); see `publish/CLAUDE.md`.
- `styleguide.md` — the single, self-contained guide for writing notes (voice, structure, derivation arc, math notation, figures, frontmatter). See *Authoring conventions*.
- `.claude/skills/` — `wiki-query` and `wiki-quiz` (see *Skills*).
- `.obsidian/` — Obsidian app config; gitignored.

## Authoring conventions

> [!important]
> **Before creating or editing ANY note under `wiki/`, you MUST read `styleguide.md` (at the repository root) first — every time, even for a one-line edit.** It is the single, self-contained reference for everything about writing notes: language, the derivation arc, structure, math notation, figures, frontmatter, line length, and what to clean up on import. This is not optional.

## Publishing

The vault is published as a website with a **Quartz → Vercel** toolchain living in `publish/`. Build mechanics, config, and the assets-under-content-root constraint are documented in **`publish/CLAUDE.md`**.

## Skills

- `wiki-query` — answer a question against the wiki: read the index, drill into pages, synthesize with `[[wiki-link]]` citations.
- `wiki-quiz` — generate quizzes (MCQ, open, solve-on-paper) from wiki pages; always clarifies format/scope/difficulty/count first.

Both skills start by reading **`wiki/index.md`** as the page index.
