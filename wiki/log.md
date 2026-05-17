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

## [2026-05-17] ingest | Attention Is All You Need (Vaswani et al., 2017)

- **What:** Founding Transformer paper — seq2seq based entirely on attention; SOTA on WMT'14 EN-DE and EN-FR.
- **Page(s) touched:** [[papers/vaswani-2017-attention-is-all-you-need]]
- **Notes:** First page in the wiki. Wanted to use `transformers` tag (this is the founding paper of the family), but the tag whitelist in `.claude/rules/04-frontmatter-schema.md` does not include it and the auto-mode classifier blocks edits under `.claude/rules/`. Used `training-dynamics` as the 5th tag instead — user may want to extend the whitelist with `transformers` and `machine-translation`. Figure: `softmax-saturation.png` (matplotlib) — numerical demo of why `1/√d_k` scaling is needed. Mermaid for the encoder/decoder architecture as «Идея в одной картинке».

