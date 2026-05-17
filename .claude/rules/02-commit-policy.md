# Commit Policy

This rule auto-loads. It applies to all git operations in this repo.

## Size

- ≤ 300 changed lines per commit.
- If a task produces more, split into atomic commits: migration / new pages / illustrations / skill changes, each separately.
- Each commit is self-contained and passes Quartz build independently.

## Format

Conventional commits with scope. Common scopes:

| Scope | Use for |
|---|---|
| `feat(wiki)` | New page, new section in an existing page, or ingest of a new source |
| `fix(wiki)` | Broken link, frontmatter typo, factual correction |
| `refactor(wiki)` | Move pages between subfolders, rename slugs |
| `docs(skill)` | Update a SKILL.md or `.claude/role.md` |
| `feat(rules)` | New or rewritten rule |
| `chore(autodoc)` | Append session insights: `chore(autodoc): session insights — YYYY-MM-DD` |

For ingest commits, follow the subject pattern: `feat(wiki): ingest <source> — <short-desc>`.

Subject line ≤ 72 chars. Body in English, wrapped at 80 cols.

## What to commit

| Path | Commit? |
|---|---|
| `wiki/**` | Yes |
| `raw/**` | **No** — source documents are gitignored. Only the subdirectory `.gitkeep` files are tracked, so the structure exists for fresh checkouts. The wiki page records `source_path` and a URL (arxiv/DOI/blog link); that's enough to re-fetch the original. Reasons to keep local: large files (PDFs often 5-50 MB), copyright/licensing concerns, and zero incremental value from versioning binary blobs. |
| `.autodoc/**` | Yes — persistent session memory |
| `.claude/**` | Yes — config and skills |
| `wiki/static/figures/**` | Yes — only generated PNGs ≤ 200 KB |
| `publish/node_modules/`, `publish/.quartz-cache/` | No — gitignore |
| `publish/public/` (Quartz build output) | No — gitignore |

PNGs > 200 KB are rejected. Lower DPI or simplify the figure.

## Push

- **`git push` is allowed without per-action approval.** Push when the commit chain is ready.
- Before pushing to `main`, run `/wiki-lint` and fix blockers — `main` deploys to Vercel on push.
- Force-push (`--force`, `--force-with-lease`) and pushing to `main` from a feature branch still need an explicit OK from the user.

## Branches

- `main` — what gets deployed.
- Significant changes (more than ~3 commits) → feature branch like `wiki-overhaul`, `migrate-attention`.
- Single typo fixes — directly in `main` is fine.
