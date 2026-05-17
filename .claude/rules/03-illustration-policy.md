# Illustration Policy

This rule auto-loads. Full manual with chooser logic lives in `.claude/skills/_shared/illustration-policy.md` and is read by `wiki-ingest` phase 6.

## Allowed tools

| Tool | When to use |
|---|---|
| Mermaid | Architectures, data flows, relationships between concepts. Inline in markdown. |
| Matplotlib (Python) | Plots, function visualisations, numerical examples. `.py` + `.png` under `publish/static/figures/<page-slug>/`. |
| Numpy/Torch + matplotlib | Numerical examples with small concrete values. Same location. |
| Source figure cut-out | Complex schemes that are better in original form than a reimplementation. `publish/static/figures/<page-slug>/source-cut-*.png`. Attribution mandatory. |

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
4. One figures folder per page: `publish/static/figures/<page-slug>/`. No shared dumping ground.
5. Mermaid: ≤ 12 nodes. Beyond that, split into two diagrams or switch to matplotlib.
6. Matplotlib `.py` scripts commit **alongside** the PNG. Reproducibility is mandatory.

## Coverage rule

Every non-trivial concept on a wiki page must have at least one illustration. If a concept is genuinely impossible to illustrate, file a question page (`wiki/questions/how-to-illustrate-<concept>.md`) instead of skipping silently.
