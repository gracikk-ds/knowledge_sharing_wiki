---
title: Progressive Distillation
type: method
tags: [distillation, diffusion, few-step-generation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# Progressive Distillation

> Iteratively distil a diffusion teacher into a student that takes one step where the teacher took two, halving the step count each round.

This is the canonical multi-step [[ml_concepts/step-distillation]] recipe. Each round trains a new student with the loss

$$
\mathcal{L}_{\text{KD}_m}(\theta) \;=\; \mathbb{E}_{t, x_0, x_t}\big\lVert x_\theta(x_t, t) - \hat{x}_\phi(x_t, t) \big\rVert_2^2,
$$

where $\hat{x}_\phi(x_t, t)$ is the teacher after **two** ODE steps starting from $(x_t, t)$. After convergence the student becomes the next round's teacher, halving sampling steps each time.

The lecture cites this only as the precursor that motivated CMs and flow-map methods; more detail (schedule, warm-start, parameterisation) would come from the original Salimans & Ho (2022) paper, not in this source.

## Sources

- [[sources/flow-map-models-lecture]] — referenced as "multi-step KD, progressive distillation".
