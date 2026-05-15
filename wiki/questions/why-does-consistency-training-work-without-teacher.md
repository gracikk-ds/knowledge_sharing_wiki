---
title: Why does Consistency Training work without a teacher?
type: question
tags: [consistency-models, training, theory]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# Why does Consistency Training work without a teacher?

## Why it matters

[[methods/consistency-training]] claims you can fit a [[ml_concepts/consistency-function]] without running a single diffusion solver step. That sounds almost too cheap. Understanding *why* it works clarifies what the resulting model represents and when CT-trained samples diverge from CD-trained ones.

## What we know so far

- The trick: pair $(x_n, x_{n-1})$ is built from the **same** noise vector $\epsilon$: $x_n = x_0 + t_n\,\epsilon$, $x_{n-1} = x_0 + t_{n-1}\,\epsilon$.
- This pair lies on a **straight line** in $(x, t)$. The lecture derives it from the conditional-score approximation $\nabla_x \log p_t(x) \approx -(x - x_0)/t^2$, which collapses the [[ml_concepts/probability-flow-ode]] to $\mathrm{d}x = (x - x_0)/t\,\mathrm{d}t$.
- So CT trains a flow map for the **straightened** ODE, not for the original diffusion ODE.

## Open sub-questions

- The straightened ODE and the original diffusion ODE differ in general (the conditional score is the score only in expectation, not pointwise). What is the gap, and when does it matter?
- Is CT secretly equivalent to a rectified-flow target? "Consistency Flow Matching" (2024) seems to claim yes.
- Empirically, CT samples can be sharp at 1 step. Is that because the straight ODE is easier to invert, or because CT regularises away low-frequency content?

## Related

- [[methods/consistency-training]]
- [[methods/consistency-distillation]]
- [[ml_concepts/consistency-function]]
- [[sources/flow-map-models-lecture]]
