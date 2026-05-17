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
