---
title: Probability-Flow ODE
type: ml_concept
tags: [generative-models, diffusion, ode, score-based-models]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# Probability-Flow ODE

> The deterministic ODE whose marginal distributions match those of a diffusion SDE, used at inference because it is solvable with standard ODE integrators and is reproducible from a fixed noise sample.

Stub. The current wiki uses the probability-flow ODE only as the curve along which a [[ml_concepts/consistency-function]] is defined. In the common parametrisation (EDM-style),

$$
\mathrm{d}x \;=\; -\,t\,\nabla_x \log p_t(x)\,\mathrm{d}t.
$$

Together with the conditional-score approximation $\nabla_x \log p_t(x) \approx -(x - \mathbb{E}[x_0 \mid x])/t^2$, this is the ODE that [[methods/consistency-training]] linearises into a straight reference path.

A proper draft awaits ingest of Song et al. 2020 ("Score-based generative modeling through SDEs") or EDM (Karras et al. 2022).

## Sources

- [[sources/flow-map-models-lecture]] — equation reproduced; concept used as background.
