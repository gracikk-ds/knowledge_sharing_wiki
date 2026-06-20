---
name: wiki-reindex
description: Use when notes or lecture PDFs under wiki/ are added, deleted, renamed, or substantially rewritten and wiki/index.md is now stale. Triggers on "update the index", "rebuild the index", "reindex the wiki", "обнови индекс", "пересобери индекс", or after ingesting/removing wiki content.
---

# wiki-reindex

Reconcile `wiki/index.md` with what actually lives under `wiki/`. The heavy reading runs on a **sonnet** subagent; the main session only orchestrates and shows the diff — so the full note contents never load into the main context.

## Core rule — reconcile, don't rewrite

Three operations only:

- **Add** — a content file on disk has no entry → write one fresh entry in the matching section.
- **Remove** — an entry points to a file that no longer exists → delete the bullet (and its heading if it becomes empty).
- **Update** — the file exists but its one-liner is stale (no longer matches the note) → rewrite that single line.

**Preserve the existing wording of every entry whose note is unchanged.** Minimal diff is the goal — never reword an accurate description.

**Always stamp the date.** On every run — even a no-op reconciliation — set the `Updated` frontmatter field to today's date, read from the system (never guessed). This is the one line that may change with no content change.

## Checklist (mirror as TodoWrite)

1. Delegate the reconciliation to a sonnet subagent.
2. Review the diff for accidental churn.
3. Report the changes to the user.

## Step 1 — Delegate to a sonnet subagent

Dispatch ONE subagent with the Agent tool — `model: "sonnet"`, `subagent_type: "general-purpose"` — and give it this brief verbatim (it is self-contained):

> You maintain the index of an Obsidian ML-notes vault at `wiki/index.md`. Reconcile it with disk. Apply only Add / Remove / Update; do NOT reword entries that are still accurate. Minimal diff.
>
> 1. List content files: `find wiki -type f \( -name '*.md' -o -name '*.pdf' \) | sort`. Ignore `wiki/index.md` and everything under `wiki/images/`.
> 2. Read `wiki/index.md`. Keep its intro paragraph intact, and the frontmatter too — except the `Updated` field (step 6).
> 3. **Markdown note** → goes in a topic section as `- [[<basename-without-.md>|<Display Title>]] — <summary>`. The summary is terse Russian prose with English technical terms, naming the key sub-topics the note derives — match the style of the entries already present. Read the note to write/refresh its summary. For a new note, take the Display Title from its `title` frontmatter or its H1; reuse the existing title if the entry already exists.
> 4. **`.pdf`** → a lecture, listed under `## Лекции (слайды)` as a backtick relative path (e.g. `distillation/flow-map-models.pdf`) with a short Russian description. Reading the PDF is optional — a brief accurate phrase suffices.
> 5. Section ↔ folder map: `gen-ai/` → `## Генеративные модели`; `transformer-primitives/` → `## Трансформеры`; `applied/` → `## Прикладные модели`; PDF-only folders (`distillation/`, `system-design/`, `metrics/`, …) group under `## Лекции (слайды)`. If a new topic folder of notes appears with no matching heading, add a new `##` section in a sensible place.
> 6. **Stamp the date.** Run `date +%Y-%m-%d`; set the frontmatter `Updated:` key to that value (add the key right under `title:` if it does not exist yet). Do this on every run, even if nothing in steps 3–5 changed.
> 7. Write the reconciled file back to `wiki/index.md`.
> 8. Return a concise report grouped as **Added / Removed / Updated**, plus an unchanged count and the new `Updated` date. Do NOT paste the whole file.

## Step 2 — Review the diff

Run `git diff -- wiki/index.md`. Confirm it matches the subagent's report and contains no accidental churn: reworded-but-equivalent lines, dropped sections, broken `[[wikilinks]]`, or `.md` notes mistakenly listed as backtick paths (or PDFs as wikilinks). The `Updated` frontmatter line changes on every run — that is expected, not churn. If real churn appears, re-dispatch with a reminder to preserve unchanged wording.

## Step 3 — Report

Relay the Added / Removed / Updated summary and the new `Updated` date to the user. The change is already written and git-tracked — tell them they can discard it with `git checkout -- wiki/index.md`.
