---
title: Consistency Function
type: ml_concept
tags: [consistency-models, generative-models, flow-map, distillation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Consistency Function

> A consistency function $f(x_t, t) \mapsto x_0$ maps any point on a probability-flow ODE trajectory to its origin at $t = 0$, so that all points on the same trajectory share a single image.

## Motivation

We want to generate an image $x_0$ from noise $x_\sigma$ in as few network calls as possible. A standard diffusion model gives us the [[ml_concepts/probability-flow-ode]] — a deterministic curve linking the two — but turns sampling into solving an ODE, which costs 50–200 evaluations of a vector-field network. The trajectory is determined by the model; the slowness comes entirely from numerical integration of a curved path.

The first thing to try is to use a coarser solver. This fails because the curve is genuinely non-linear: a few large Euler steps either overshoot or undershoot, and quality degrades fast. The issue is not the solver; it is that a vector field encodes *local* velocity, and one query at $(x_t, t)$ tells you nothing about where the trajectory ends up.

A consistency function sidesteps this by learning the endpoint directly. Define $f_\theta(x_t, t)$ to send any point on the trajectory to its origin $x_0$. Because the ODE is deterministic, every $(x_t, t)$ lies on exactly one trajectory, so $f_\theta$ is a function — not a relation. With it, sampling is one forward pass: feed in noise, read out an image. It is a [[ml_concepts/flow-map]] with the target time pinned to $s = 0$.

The training problem becomes: how do you supervise $f_\theta$ without integrating the slow ODE for every example? The trick is to demand that $f_\theta$ be *constant along each trajectory*. If two nearby points $(x_t, t)$ and $(x_s, s)$ sit on the same curve, their predicted origins must match. This self-consistency identity, anchored by a boundary condition at $t \approx 0$, turns "predict the integrated endpoint" into a local matching loss that does not require a full ODE rollout per gradient step.

## Formal description

Let $\{x_\tau\}_{\tau \in [0, \sigma]}$ denote a solution trajectory of the probability-flow ODE, with $x_0$ clean and $x_\sigma$ pure noise. A **consistency function** is a map

$$
f_\theta: (x_t, t) \mapsto x_0,\qquad \forall x_t \in \{x_\tau\}_{\tau \in [0, \sigma]}.
$$

It must satisfy the **self-consistency property**: for any two times $s, t \in [0, \sigma]$ on the same trajectory,

$$
f_\theta(x_t, t) \;=\; f_\theta(x_s, s).
$$

Equivalently, $f_\theta$ is constant along each trajectory.

A **boundary condition** fixes the value of $f_\theta$ at the trajectory's origin:

$$
f_\theta(x_0, t_0) \;=\; x_0,
$$

where $t_0$ is the smallest time in the schedule (usually a small $\epsilon > 0$, not exactly zero, for numerical reasons). The boundary rules out the degenerate solution $f_\theta \equiv 0$, which would otherwise satisfy the self-consistency loss trivially.

## Training objective

Discretise $[0, \sigma]$ into times $t_0 < t_1 < \ldots < t_N$. The self-consistency loss pairs adjacent times on the same trajectory:

$$
\mathcal{L}(\theta) \;=\; \mathbb{E}_{n}\big\lVert f_\theta(x_{n-1}, t_{n-1}) - f_\theta(x_n, t_n) \big\rVert_2^2,
$$

where $(x_n, x_{n-1})$ are two adjacent points on the *same* trajectory. This raises the question: where does the pair come from? Two answers split the methods:

- [[methods/consistency-distillation]] — $x_n$ is sampled from the forward noising process, and $x_{n-1}$ is produced by one step of a pre-trained diffusion teacher's ODE solver.
- [[methods/consistency-training]] — no teacher; use a straight reference path $x_\tau = x_0 + \tau\,\epsilon$ with the *same* $\epsilon$ for $x_n$ and $x_{n-1}$.

Both also enforce the boundary $f_\theta(x_0, t_0) = x_0$, typically via a skip connection: $f_\theta(x, t) = c_{\text{skip}}(t) \cdot x + c_{\text{out}}(t) \cdot F_\theta(x, t)$ with $c_{\text{skip}}(t_0) = 1$, $c_{\text{out}}(t_0) = 0$.

## Sampling

A consistency function is not a vector field, so standard ODE solvers do not apply. Two sampling strategies:

- **1-step:** $x_0 \approx f_\theta(x_N, t_N)$ with $x_N \sim \mathcal{N}(0, \sigma^2 I)$.
- **Stochastic multistep (4–5 steps):** repeat
  ```
  x_0 ← f_θ(x_n, t_n)
  ε   ∼ N(0, I)
  x_{n-1} ← x_0 + t_{n-1} ε
  ```
  Each "re-noising" step picks a fresh trajectory at a lower noise level, then projects to its origin. Quality usually beats 1-step at the cost of 4–5× the compute.

## Variations and related concepts

- [[ml_concepts/flow-map]] — consistency function is the $s = 0$ case.
- [[methods/multistep-consistency-model]] — relaxes the "always project to $t = 0$" rule to "project to the next interval boundary".
- [[methods/consistency-distillation]] — teacher-based training.
- [[methods/consistency-training]] — teacher-free training.

## Open questions

- [[questions/why-cant-cms-use-ode-solvers]]
- [[questions/why-does-consistency-training-work-without-teacher]]

## Sources

- [[sources/flow-map-models-lecture]] — definition, self-consistency property, boundary condition, and sampling protocol.

## Up next

- [[methods/consistency-distillation]] — train $f_\theta$ using a pre-trained diffusion teacher to provide adjacent-time trajectory pairs.
- [[methods/consistency-training]] — train $f_\theta$ from scratch without a teacher, by reading the ODE's local linearisation off the data.
