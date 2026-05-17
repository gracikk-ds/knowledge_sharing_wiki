# Frontmatter Schema

This rule auto-loads. `wiki-lint` enforces it. Every wiki page starts with YAML frontmatter matching the schema below.

## Common fields (every page)

```yaml
---
title: <Human-readable, English, capitalised>
type: <one of: ml_concept | math_concept | method | topic | source | question>
tags: [<lowercase>, <kebab-case>, <plural-where-natural>]
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources: <integer; count of distinct raw sources cited>
status: <one of: stub | draft | mature>
---
```

### Field rules

- `title`: English, capitalised. The filename is the slug (kebab-case).
- `type`: matches the directory the file lives in.
- `tags`: lowercase, kebab-case. Plural where natural (`transformers`, not `transformer`).
- `created` / `updated`: ISO date. Update `updated` on substantive changes; do not bump for typo fixes.
- `sources`: integer count of distinct raw sources cited. Bump on new citation; do not double-count.
- `status`:
  - `stub` — exists because someone linked to it; minimal content.
  - `draft` — substantive content from at least one source.
  - `mature` — cross-referenced, multi-source, synthesis stable.
## Source pages — additional fields

```yaml
---
title: "<First Author> — <short title>"
type: source
source_path: raw/<kind>/<file>
source_kind: <one of: paper | clip | scratch | lecture | other>
source_date: YYYY-MM-DD
ingested: YYYY-MM-DD
tags: [...]
status: <stub | draft | mature>
---
```

- `source_path`: relative to repo root. Validate the file exists.
- `source_date`: when the source was published (not when ingested).
- `ingested`: when this source page was created.

## Validation rules (enforced by `wiki-lint`)

1. Every file under `wiki/` starts with `---` on line 1.
2. All common fields present and non-empty.
3. `type` matches enclosing directory (e.g., `wiki/ml_concepts/*.md` has `type: ml_concept`).
4. `created` ≤ `updated`.
5. `tags` is non-empty.
6. Source pages have all source-specific fields.
7. `status` is one of the three values.
