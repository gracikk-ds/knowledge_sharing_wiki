---
title: Consistency Training (CT)
type: method
tags: [consistency-models, generative-models, few-step-generation, training-free-teacher]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Consistency Training (CT)

> Train a [[ml_concepts/consistency-function]] from scratch — no diffusion teacher needed — by using the straight reference path $x_t = x_0 + t\,\epsilon$ and reusing the *same* $\epsilon$ for both ends of a trajectory pair.

## Motivation

[[methods/consistency-distillation]] needs a pre-trained [[ml_concepts/diffusion-model]] to produce matched trajectory pairs $(x_t, \hat{x}_{t-\Delta})$. That is a heavy prerequisite: you pay the full cost of training a multi-step teacher before you ever start training the one-step student. The question is whether you can skip the teacher and still train a [[ml_concepts/consistency-function]] that obeys trajectory invariance.

The blocker is the pairing itself. To enforce $f_\theta(x_t, t) = f_\theta(x_s, s)$ you need two points on the *same* ODE trajectory. The teacher was the only thing that knew which $x_s$ matches a given $x_t$, because the trajectory bends through the data manifold in a complicated way that depends on the learned [[ml_concepts/score-function]]. Sample a fresh $\epsilon$ at each time and the two points sit on *different* trajectories — the invariance constraint becomes noise.

CT escapes this by changing which ODE the consistency function is supposed to track. If you approximate the score by the conditional score at one data point, the [[ml_concepts/probability-flow-ode]] collapses to a straight line $x_t = x_0 + t \epsilon$, and the pairing becomes trivial: pick one $\epsilon$, evaluate the line at two times, you have a matched pair. The student now learns the consistency function of a *straightened* trajectory, which is also what one-step samplers want anyway — a straight ODE is exactly the one a single Euler step can solve without error. Two forward passes per training step, no teacher, no solver call. The trade is that the underlying ODE is no longer the real diffusion ODE; CT inherits whatever bias the straight-path approximation introduces.

## Problem setting

You do not have a pre-trained diffusion model, or you do not want to pay the cost of training one first. You still want a consistency function.

## The trick

Consistency distillation needs trajectory pairs $(x_n, x_{n-1})$ on the *same* ODE trajectory. Without a teacher, where do they come from?

CT uses a clean observation. If the underlying score-based ODE is

$$
\mathrm{d}x \;=\; -\,t\,\nabla_x \log p_t(x)\,\mathrm{d}t,
$$

and you approximate the score by the conditional score at a single sample,

$$
\nabla_x \log p_t(x) \;\approx\; -\,\frac{1}{t^2}\,(x - x_0),
$$

the ODE becomes the **straight line**

$$
\mathrm{d}x \;=\; \frac{1}{t}(x - x_0)\,\mathrm{d}t,
$$

whose closed-form solution is $x_t = x_0 + t\,\epsilon$ with a single $\epsilon \sim \mathcal{N}(0, I)$. So a pair $(x_n, x_{n-1})$ lies on the same *straightened* trajectory if and only if it is built from the **same $\epsilon$** at two times $t_n$, $t_{n-1}$.

## Algorithm

Discretise time as $t_0 < t_1 < \ldots < t_N$. One training step:

1. Sample $x_0 \sim p_{\text{data}}$, $n \sim \mathcal{U}\{1, \ldots, N\}$, $\epsilon \sim \mathcal{N}(0, I)$.
2. Build the pair from the **same $\epsilon$**:
   $$x_n \;=\; x_0 + t_n\,\epsilon,\qquad x_{n-1} \;=\; x_0 + t_{n-1}\,\epsilon.$$
3. Apply the student to both and minimise:
   $$\mathcal{L}_{\text{CT}}(\theta) \;=\; \mathbb{E}\big\lVert f_\theta(x_{n-1}, t_{n-1}) - f_\theta(x_n, t_n) \big\rVert_2^2.$$
4. Enforce the boundary $f_\theta(x_0, t_0) = x_0$ via the skip-connection parametrisation.

The whole training reduces to two forward passes per step (plus an EMA-target network branch in practice).

## Why it works

CT does not approximate the *real* diffusion trajectory — it approximates a **straightened** version of it. The lecture notes this explicitly: "Consistency Training forces the trajectories to be straight." The optimal $f_\theta$ under CT is the consistency function of a flow-matching-style straight ODE, which conveniently is also a valid generative model when $\epsilon$'s distribution matches the noise distribution used at inference.

In other words, CT trains a flow-map for the **rectified-flow** ODE instead of for the diffusion ODE. This is also why the resulting samples can come out sharp in one step: the underlying ODE is, by construction, a straight line.

## Properties

- **Step count at inference:** 1 step (greedy) or 4–5 stochastic steps, same as CD.
- **Teacher needed:** no.
- **Training cost:** two forward passes per step; no extra solver call.
- **Caveat:** the straight-path approximation is exact only in the limit of an infinite straightening procedure (rectified flow). With finite data the optimal flow map is not literally the diffusion flow map — but the lecture argues this is a feature, not a bug, since straight trajectories are exactly what one-step samplers want.

## Variants and successors

- "Consistency Models Made Easy" (2024) — variance reduction.
- "Consistency Flow Matching" (2024) — explicit straight-flow target.
- [[methods/consistency-distillation]] — the teacher-based counterpart.

## Sources

- [[sources/flow-map-models-lecture]] — derivation of the straight-path trick from the score-based ODE, and the loss.

## Up next

- [[methods/consistency-distillation]] — the teacher-based counterpart; comparing the two clarifies what the teacher was buying.
- [[topics/few-step-generative-models]] — broader landscape of one-step samplers; CT slots in next to shortcut models and mean flow.
