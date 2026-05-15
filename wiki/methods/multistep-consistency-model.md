---
title: Multistep Consistency Models (Multi-boundary CMs)
type: method
tags: [consistency-models, generative-models, flow-map, few-step-generation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Multistep Consistency Models (Multi-boundary CMs)

> Generalise a [[ml_concepts/consistency-function]] from "always project to $t = 0$" to "project to the next interval boundary". Split $[0, \sigma]$ into $N$ intervals and learn one consistency function per interval.

## Motivation

A single-interval [[ml_concepts/consistency-function]] asks one network to map any $x_t$ on the trajectory back to its clean endpoint $x_0$. That target spans the entire $[0, \sigma]$ interval of the [[ml_concepts/probability-flow-ode]], so the network has to represent the result of integrating a highly non-linear vector field across the whole range. With one inference step this is the maximum that one forward pass can do. The quality cost shows up in practice — single-step CMs underperform their teacher on hard distributions even after careful training.

Allowing more inference steps would help, but the standard CM has no notion of "stopping early". The function is built to land at $t = 0$, not at some intermediate time. There is no obvious way to break a long jump into shorter, easier ones using the same network — every step is a jump all the way to the endpoint.

The fix is to give the consistency function more than one boundary. Split $[0, \sigma]$ into $M$ intervals with endpoints $0 = b_0 < b_1 < \ldots < b_M = \sigma$ and define a multistep consistency function $f_\theta(x_r, r, s)$ where $(r, s)$ must lie in the *same* interval $[b_{m-1}, b_m]$. Within each interval the function obeys the standard within-trajectory invariance, but it projects to the *interval's* left endpoint rather than to zero. The regression target inside each interval is now much smaller and smoother — a piece of the integral instead of the whole thing — and the deterministic boundary-to-boundary sampling loop stitches the pieces back together at inference. With $M = 4$ the lecture reports quality matching a 50-step teacher.

## Problem setting

A standard CM has to approximate the *entire* ODE trajectory from any noise level back to $t = 0$ with one network. That is a tall order — the target is the result of integrating across the whole $[0, \sigma]$ interval. The lecture flags this as the core issue: "we need to approximate the entire solution interval".

The fix: only approximate a *piece* of it at a time.

## Algorithm

Pick boundaries $0 = b_0 < b_1 < \ldots < b_M = \sigma$. Define a **multistep consistency function**

$$
f_\theta: (x_r, r, s) \mapsto x_s,\qquad \forall x_r \in \{x_\tau\}_{\tau \in [t, s]},
$$

with the constraint that $(r, s)$ always lie within the *same* interval $[b_{m-1}, b_m]$. Inside each interval the self-consistency property holds exactly as in a single-interval CM:

$$
f_\theta(x_t, t, b_{m-1}) \;=\; x_{b_{m-1}}\quad \forall\, x_t \in [b_{m-1}, b_m].
$$

Training: discretise each interval into sub-times $t_0 < t_1 < \ldots < t_N$ and use the CD-style loss restricted to pairs within the same interval:

$$
\mathcal{L}(\theta) \;=\; \mathbb{E}\,\big\lVert f_\theta(\hat{x}_{n-1}, t_{n-1}, t'_n) - f_\theta(x_n, t_n, t'_n) \big\rVert_2^2,
$$

where $t'_n$ is the right endpoint of the interval containing $t_n$.

Sampling at inference: deterministically jump from boundary to boundary. With $M = 4$ boundaries the lecture reports quality comparable to a 50-step teacher.

## Why it works

The flow-map regression problem becomes easier as the target interval shrinks. Across the whole $[0, \sigma]$ the network is fitting an integral of a highly non-linear vector field. Across one short sub-interval the same network is fitting a much smaller, smoother chunk of that integral. The remaining "joints" between intervals are handled by the deterministic multistep sampling loop.

The boundaries serve the same anti-collapse role here as $t_0$ in a single-interval CM: each interval has its own anchored boundary condition.

## Properties

- **Step count at inference:** equal to the number of boundaries, often 4.
- **Quality:** lecture shows side-by-side that 4-step multistep CM matches 50-step teacher on text-to-image.
- **Training cost:** same per-step as CD; just with stratified time sampling restricted to within-interval pairs.
- **Hyperparameter:** the boundary schedule. Lecture does not prescribe; in practice geometric or EDM-style schedules are used.

## Variants and successors

- [[methods/consistency-distillation]] — the $M = 1$ special case.
- [[methods/shortcut-model]] — different self-consistency principle (interval additivity instead of within-interval invariance).
- "Multistep Consistency Models" (Heek et al., 2024) — the original paper.

## Sources

- [[sources/flow-map-models-lecture]] — motivation ("approximate the entire solution interval is too hard"), formal definition with $(x_r, r, s)$, and training objective.

## Up next

- [[methods/mean-flow]] — drops the boundary-projection target entirely; trains an arbitrary $F_\theta(x_t, t, s)$ on a differential identity.
- [[topics/few-step-generative-models]] — broader landscape of how multistep CMs relate to shortcut models, mean flow, and distillation.
