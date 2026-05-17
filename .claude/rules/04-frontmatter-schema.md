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
- `tags` — lowercase kebab-case, plural where natural (`transformers`, not `transformer`). 3-7 tags per page. Every tag must have an entry in `wiki/tags.md` (see «Tag registry» below).
- `status`:
  - `stub` — TL;DR and Мотивация only, the rest is empty or missing.
  - `draft` — all required sections filled.
  - `mature` — user reviewed and approved.

## Tag registry

The live source of truth is `wiki/tags.md`. Every tag used on any wiki page must already have an entry there. When a page needs a new tag, append an H2 to `wiki/tags.md` **in the same commit** that introduces the tag on the page.

`wiki-lint` reads `wiki/tags.md` and rejects any page tag that has no matching entry.

Format of each entry in `wiki/tags.md`:

```markdown
## <human-readable name>

**Slug:** `<slug-used-in-frontmatter>`

<one-sentence definition: when to apply this tag>

[Все разборы →](/tags/<slug>)
```

Quartz auto-generates the `/tags/<slug>` index from frontmatter — `wiki/tags.md` adds the human-readable definition layer on top.

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
6. `tags` non-empty; every tag has a matching H2 entry in `wiki/tags.md`.
7. `status` is one of: `stub`, `draft`, `mature`.
8. `authors` is non-empty for paper/lecture/clip; `presenter` is present for knowledge-sharing.
9. Slug matches the pattern for the file's `source_kind`.
