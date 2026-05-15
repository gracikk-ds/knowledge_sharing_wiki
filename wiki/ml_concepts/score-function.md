---
title: Score Function
type: ml_concept
tags: [generative-models, diffusion, score-based-models]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# Score Function

> The gradient of the log-density $\nabla_x \log p_t(x)$, learnt by a score-based model to drive the reverse diffusion ODE/SDE.

Stub. In the current wiki the score function appears only in passing, specifically the **Tweedie / conditional-score** form used by [[methods/consistency-training]]:

$$
\nabla_x \log p_t(x) \;=\; -\,\frac{1}{t^2}\big(x - \mathbb{E}[x_0 \mid x]\big).
$$

Approximating $\mathbb{E}[x_0 \mid x] \approx x_0$ (a single sample) turns the [[ml_concepts/probability-flow-ode]] into a straight line in $t$, which is the trick that enables CT's "same-$\epsilon$" trajectory pairs.

A proper draft awaits ingest of a dedicated score-based source.

## Sources

- [[sources/flow-map-models-lecture]] — Tweedie identity quoted in the CT derivation.
