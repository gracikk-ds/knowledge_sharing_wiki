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

## [2026-05-18] ingest | Qwen-Image Technical Report (Qwen Team, 2025)

- **What:** 20B MMDiT foundation model for T2I + image editing with a focus on complex text rendering (especially Chinese). Three modules: frozen Qwen2.5-VL as text encoder, Wan2.1-VAE backbone with a text-rich fine-tuned decoder, 20B MMDiT with MSRoPE (text on diagonal of image grid). Flow-matching pre-training plus DPO + GRPO post-training.
- **Page(s) touched:** [[papers/qwen-team-2025-qwen-image]]
- **Notes:** Source PDF downloaded from arxiv (2508.02324). Added new tag `text-to-image` to `wiki/tags.md`. Figures: mermaid pipeline overview, two source cut-outs (Fig 6 architecture, Fig 8 MSRoPE comparison), one matplotlib (flow-matching linear path + constant target velocity). Fig 8 had to be downsampled to 780px wide to stay under the 200 KB PNG ceiling — the cat photo inside makes PNG compression inefficient. Open question for the user: whether `multimodal` or `image-editing` should also become tags (skipped for now — `text-to-image` already covers the main contribution).

