# Illustration Policy

This rule auto-loads. Full manual with chooser logic lives in `.claude/skills/_shared/illustration-policy.md` and is read by `wiki-ingest` phase 6.

## Allowed tools

| Tool | When to use |
|---|---|
| Mermaid | Architectures, data flows, relationships between concepts. Inline in markdown. |
| Matplotlib (Python) | Plots, function visualisations, numerical examples. `.py` + `.png` under `wiki/static/figures/<page-slug>/`. |
| Numpy/Torch + matplotlib | Numerical examples with small concrete values. Same location. |
| Source figure cut-out | Complex schemes that are better in original form than a reimplementation. `wiki/static/figures/<page-slug>/source-cut-*.png`. Attribution mandatory. |

## Forbidden

- **AI image generation** (DALL·E, Stable Diffusion, Midjourney, any model). Cost of wrong-but-pretty exceeds value.
- **Hand-drawn Excalidraw / manual SVG** inside the auto-flow. If hand-drawn is desired, it ships as a separate manual commit after `/wiki-ingest`.
- **TikZ / LaTeX figures** — overkill for Quartz, brittle render.
- **Screenshots of slides or talks without attribution.**

## Required for every figure

1. Caption directly under the image:
   - Mermaid: `*Diagram: <what it shows>*`
   - Matplotlib: `*Generated: figures/<slug>/<file>.py*`
   - Cut-out: `*From <First Author> et al. (<year>), Fig. <N>.*`
2. PNG size ≤ 200 KB. If exceeded, lower DPI or simplify.
3. Filename: kebab-case, no spaces. `rope-rotation-2d.png`, not `RoPE rotation (2D).png`.
4. One figures folder per page: `wiki/static/figures/<page-slug>/`. No shared dumping ground.
5. Mermaid: ≤ 12 nodes. Beyond that, split into two diagrams or switch to matplotlib.
6. Matplotlib `.py` scripts commit **alongside** the PNG. Reproducibility is mandatory.
7. Image path in markdown: **file-relative**, never absolute. From a page at `wiki/<kind>/<slug>.md`, the matplotlib PNG lives at `wiki/static/figures/<slug>/<file>.png`, so the markdown reference is `![alt](../static/figures/<slug>/<file>.png)`. Absolute paths starting with `/` work only in Quartz's HTTP server and break under file://, Obsidian, and GitHub preview.

## Coverage rule

Every non-trivial concept on a wiki page must have at least one illustration. If a concept is genuinely impossible to illustrate, add an "Открытые вопросы" bullet on the breakdown page ("как нарисовать <концепт>") instead of skipping silently.

## Minimum figure count per page

The «Идея в одной картинке» counts toward this total. Floor — not ceiling: a long paper with 6 worthwhile concepts gets 6 figures, not 3.

| `source_kind` | Minimum figures | Typical figures |
|---|---|---|
| paper | **3** | 4-6 |
| lecture | **2** | 3-5 |
| clip | **1** | 2-3 |
| knowledge-sharing | **1** | 1-3 |

If the page comes in under the minimum, `wiki-ingest` Phase 6 fails the check and you go back and add more — either matplotlib plots for the formal claims, mermaid for any data flow / dependency structure that the page describes in prose, or source cut-outs with attribution for paper figures you'd otherwise re-explain in 200 words.

Every figure on the page must connect to the text via a **lead-in** (one sentence right before the figure explaining what it shows) and a **walk-out** (one sentence right after explaining what to take away). Floating figures with no textual anchor are the same as missing figures.
