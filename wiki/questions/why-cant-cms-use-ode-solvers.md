---
title: Why can't consistency models be plugged into ODE solvers?
type: question
tags: [consistency-models, ode, sampling]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# Why can't consistency models be plugged into ODE solvers?

## Why it matters

ODE solvers (Heun, DPM-Solver, RK4) are a mature toolkit for diffusion sampling. If they applied to CMs, we would not need a bespoke stochastic multistep procedure to sample from CMs in 4–5 steps.

## What we know so far

- A [[ml_concepts/consistency-function]] is a [[ml_concepts/flow-map]]: it outputs the *integrated* solution $\Psi_{t \to 0}(x_t)$, not the velocity.
- ODE solvers are designed to integrate a *derivative*. Feeding them an already-integrated quantity is a category error: there is no $f'$ signal to step along.
- This is the practical reason the lecture gives for the stochastic multistep sampler.

## What would resolve it

- A formal statement of what class of objects ODE solvers act on (vector fields on $\mathbb{R}^d \times [0, T]$), and a proof that a flow-map output is not in that class without differentiation.
- Whether *numerically differentiating* $f_\theta$ w.r.t. $t$ recovers a usable vector field. (Probably not, because $f_\theta$ is approximate and the derivative would amplify error.)

## Related

- [[ml_concepts/flow-map]]
- [[ml_concepts/consistency-function]]
- [[sources/flow-map-models-lecture]]
