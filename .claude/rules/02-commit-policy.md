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
| `feat(wiki)` | New page, new section in an existing page |
| `feat(wiki)` | Ingest a new source: `feat(wiki): ingest <source> — <short-desc>` |
| `fix(wiki)` | Broken link, frontmatter typo, factual correction |
| `refactor(wiki)` | Move pages between subfolders, rename slugs |
| `docs(skill)` | Update a SKILL.md or `.claude/role.md` |
| `feat(rules)` | New or rewritten rule |
| `chore(autodoc)` | Append session insights: `chore(autodoc): session insights — YYYY-MM-DD` |

Subject line ≤ 72 chars. Body in English, wrapped at 80 cols.

## What to commit

| Path | Commit? |
|---|---|
| `wiki/**` | Yes |
| `raw/**` | Yes — sources are part of history |
| `.autodoc/**` | Yes — persistent session memory |
| `.claude/**` | Yes — config and skills |
| `publish/static/figures/**` | Yes — only generated PNGs ≤ 200 KB |
| `publish/node_modules/`, `publish/.quartz-cache/` | No — gitignore |
| `publish/public/` (Quartz build output) | No — gitignore |

PNGs > 200 KB are rejected. Lower DPI or simplify the figure.

## Push

- **Claude never runs `git push`**, regardless of branch or instruction.
- Push is a manual user action only.
- `main` deploys to Vercel on push. Run `/wiki-lint` before pushing.

## Branches

- `main` — what gets deployed.
- Significant changes (more than ~3 commits) → feature branch like `wiki-overhaul`, `migrate-attention`.
- Single typo fixes — directly in `main` is fine.
