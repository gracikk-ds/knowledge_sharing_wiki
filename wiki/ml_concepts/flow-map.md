---
title: Flow Map
type: ml_concept
tags: [generative-models, diffusion, flow-matching, sampling, distillation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Flow Map

> A flow map is the learnt *integrated solution* of a generative ODE: a function $\Psi_{t \to s}(x_t)$ that, given a point at time $t$, returns the point the trajectory reaches at time $s$ — no solver needed at inference.

## Motivation

Standard diffusion and [[ml_concepts/flow-matching]] learn a vector field $v(x, t)$ — the instantaneous velocity of the generative ODE. Sampling means integrating $\mathrm{d}x = v(x, t)\,\mathrm{d}t$ from noise to data. Because the trajectory is curved, an accurate solver needs many small steps; each step is a full forward pass through the network. 50–200 evaluations per sample is the standard cost.

The first attempt to cut this cost is a bigger step size, but the path's curvature limits how far you can go in one Euler step without leaving the trajectory. Better solvers (Heun, DPM-Solver) help, yet still need tens of evaluations because they fundamentally rebuild the curve from local pieces. The bottleneck is not the solver: it is the *representation*. A vector field tells you instantaneous direction, never destination.

A flow map changes what the network outputs. Instead of velocity at $(x, t)$, learn the integrated endpoint $\Psi_{t \to s}(x_t)$ — where the trajectory will be at some future time $s$. One forward pass now does the work of a full ODE rollout from $t$ to $s$. Sample in 1–4 steps where the vector-field counterpart needed 50–200.

What does this cost? Training. The vector field at $(x, t)$ is a local quantity; you can read it from infinitesimal data. The flow map at $(x, t, s)$ is the *result* of integrating that vector field, so the network must compress a whole family of integrals — one for every pair $(t, s)$ — into its weights. The interesting bit is how methods supervise this without explicitly rolling out the ODE every gradient step: teacher distillation, structural self-consistency identities like the one used by [[ml_concepts/consistency-function|consistency models]], or boundary anchoring at $s = t$. The choice of supervision is what distinguishes the methods in this family.

## Formal description

Let the generative process be the ODE

$$
\frac{\mathrm{d}x}{\mathrm{d}u} = v(x, u),\qquad u \in [0, \sigma].
$$

Its solution operator (flow) is

$$
\Psi_{t \to s}(x_t) \;=\; x_t + \int_t^s v(x_u, u)\,\mathrm{d}u .
$$

A **flow map** is a neural network $F_\theta(x_t, t, s)$ trained so that

$$
\Psi_{t \to s}(x_t) \;\approx\; x_t + (s - t)\,F_\theta(x_t, t, s),
$$

i.e. $F_\theta$ represents the *average velocity* over $[t, s]$. Equivalently the network can be parametrised to output the destination directly: $G_\theta(x_t, t, s) \approx \Psi_{t \to s}(x_t)$. The two parametrisations are interchangeable.

At inference, you pick a coarse schedule $t_N > t_{N-1} > \ldots > t_0$, set $x_N \sim \mathcal{N}(0, \sigma^2 I)$, and iterate

$$
x_{n-1} \;=\; x_n + (t_{n-1} - t_n)\,F_\theta(x_n, t_n, t_{n-1}).
$$

For $N = 1$ the model jumps from pure noise to a sample in one forward pass.

A [[ml_concepts/consistency-function]] is the special case where the target time is fixed to $t = 0$: $f_\theta(x_t, t) = \Psi_{t \to 0}(x_t)$.

## Why it can be learnt

A flow map is well-defined because the generative ODE is **deterministic**: each $(x_t, t)$ lies on exactly one trajectory, so $\Psi_{t \to s}(x_t)$ is a function. Three ways to supervise it:

1. **Distillation from a teacher** — run the teacher's ODE solver from $(x_t, t)$ to $s$, regress the student to that endpoint. Used by [[methods/progressive-distillation]] and [[methods/consistency-distillation]].
2. **Self-consistency** — exploit a structural identity the true flow satisfies. For consistency models that identity is $f(x_t, t) = f(x_{t - \Delta}, t - \Delta)$ along a trajectory; for shortcut models it is interval additivity $F(x_t, t, s) = F(F(x_t, t, r), r, s)$; for Mean Flow it is the [[math_concepts/mean-flow-identity]].
3. **Boundary anchoring** — at $s = t$ the flow map degenerates to the identity (or to the instantaneous velocity, depending on parametrisation). Pinning that boundary prevents collapse to a degenerate solution like $F \equiv 0$.

Most methods combine (1) or (2) with (3).

## Flow map vs vector field

| Property                  | Vector field $v(x, t)$         | Flow map $F(x, t, s)$ |
|---------------------------|--------------------------------|-----------------------|
| What it outputs           | Instantaneous velocity         | Integrated displacement |
| Needs ODE solver to sample? | Yes — many steps             | No — one forward pass per step |
| Domain                    | $(x, t)$                       | $(x, t, s)$ — extra time arg |
| Hard part of training     | Many-to-one regression target  | Compressing an integral family |
| Composable with solvers?  | Yes — gradient field           | No — already pre-integrated |

The last row is the practical catch: once you have a flow map, you cannot plug it into Heun, DPM-Solver, etc., because there is no derivative to integrate. Sampling uses dedicated schedules ([[methods/consistency-model-sampling]] stub) instead.

## Variations and related concepts

- [[ml_concepts/consistency-function]] — flow map with target $s = 0$.
- [[ml_concepts/step-distillation]] — supervises flow maps via a teacher.
- [[methods/shortcut-model]] — flow-map method using interval additivity.
- [[methods/mean-flow]] — flow-map method using the average-velocity identity.
- [[methods/multistep-consistency-model]] — flow maps restricted to intervals.
- [[ml_concepts/flow-matching]] — the vector-field counterpart that flow-map methods are trying to "pre-integrate".

## Open questions

- [[questions/why-cant-cms-use-ode-solvers]]
- [[questions/how-is-mean-flow-time-derivative-computed]]

## Sources

- [[sources/flow-map-models-lecture]] — introduces the term "flow map" as the unifying view of CMs, ShortCut, and Mean Flow.

## Up next

- [[ml_concepts/consistency-function]] — the most studied flow map, with the target time pinned to $s = 0$.
- [[methods/shortcut-model]] — a flow map trained via the interval-additivity identity $F(x_t, t, s) = F(F(x_t, t, r), r, s)$.
