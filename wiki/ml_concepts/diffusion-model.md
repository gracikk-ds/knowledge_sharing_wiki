---
title: Diffusion Model
type: ml_concept
tags: [generative-models, diffusion, score-based-models]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# Diffusion Model

> A generative model that defines a forward noising process $x_t = x_0 + t\,\epsilon$ and learns to reverse it by predicting either $x_0$, the noise $\epsilon$, or the score $\nabla_x \log p_t(x)$.

This page is a stub. The wiki's first source — a lecture on flow-map models — refers to diffusion only as the slow teacher whose ODE trajectory is being shortcut. Substantive content awaits ingest of a diffusion-specific source (Ho/Jain/Abbeel DDPM, Song et al. score-based, EDM, etc.).

## What is touched on in the current wiki

- The reverse process integrates the [[ml_concepts/probability-flow-ode]] $\mathrm{d}x = -t\,\nabla_x \log p_t(x)\,\mathrm{d}t$.
- Training loss $\mathcal{L}_{\text{diff}}(x_\phi) = \mathbb{E}_{t, x_0, \epsilon}\,\lVert x_\phi(x_t, t) - x_0 \rVert_2^2$.
- The forward noising is **one-to-many** ([[ml_concepts/step-distillation]] explains why this makes single-step inference fundamentally hard).

## Sources

- [[sources/flow-map-models-lecture]] — context only; not the primary source for this concept.
