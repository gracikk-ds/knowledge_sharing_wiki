---
name: wiki-reindex
description: Reconcile `wiki/index.md` with notes and lecture PDFs on disk after files under `wiki/` are added, removed, renamed, or substantially rewritten. Use for “update/rebuild/reindex the wiki”, «обнови индекс», «пересобери индекс», and after ingesting or removing wiki content.
---

# wiki-reindex

Reconcile the index; do not rewrite it.

Allowed content operations:

- **Add** an entry for a file missing from the index.
- **Remove** an entry whose file no longer exists.
- **Update** only a stale one-line summary.

Preserve the exact wording of every still-accurate entry. On every run, including a content no-op, set frontmatter `Updated` to the current system date.

## Process

1. Spawn one subagent for the bounded reconciliation task below so note contents do not fill the main context.
2. Review `git diff -- wiki/index.md` in the main session.
3. Report Added, Removed, Updated, the unchanged count, and the new date.

If subagents are unavailable, perform the same bounded reconciliation directly.

## Subagent brief

Give the subagent this self-contained task:

> Maintain the index of the Obsidian ML-notes vault at `wiki/index.md`. Reconcile it with disk. Apply only Add / Remove / Update; do not reword entries that remain accurate. Keep the diff minimal.
>
> 1. List `*.md` and `*.pdf` files under `wiki/`. Ignore `wiki/index.md` and everything under `wiki/images/`.
> 2. Read `wiki/index.md`. Preserve its frontmatter and introduction except for `Updated`.
> 3. List a Markdown note in its topic section as `- [[<basename-without-.md>|<Display Title>]] — <summary>`. Follow the current index style: use a basename by default, but use the shortest disambiguating path relative to `wiki/` for `index.md` files or duplicate basenames, for example `coding/index`. Match existing terse Russian summaries with natural English technical terms. Read a note before adding or refreshing its summary. Take a new display title from frontmatter `title` or H1; preserve an existing title.
> 4. List PDFs under `## Лекции (слайды)` as backtick relative paths with a short Russian description. Reading a PDF is optional when its purpose is clear.
> 5. Map `gen-ai/` to `## Генеративные модели`, `transformer-primitives/` to `## Трансформеры`, and `applied/` to `## Прикладные модели`. Group PDF-oriented folders such as `distillation/`, `system-design/`, and `metrics/` under `## Лекции (слайды)`. Add a sensible section for a new notes topic when necessary.
> 6. Run `date +%Y-%m-%d` and set `Updated` to that value, adding it directly below `title` if absent.
> 7. Write the reconciled `wiki/index.md`.
> 8. Return a concise Added / Removed / Updated report, unchanged count, and date. Do not paste the whole file.

## Review

Confirm the diff contains no equivalent rewording, dropped sections, broken wikilinks, Markdown notes represented as raw paths, or PDFs represented as wikilinks. A date-only change is expected.

The change remains in the working tree. Do not discard it unless the user explicitly asks; report that it can be reverted with `git restore -- wiki/index.md`.
