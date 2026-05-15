---
title: Mean Flow
type: method
tags: [flow-map, generative-models, flow-matching, few-step-generation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Mean Flow

> Train a [[ml_concepts/flow-map]] $F_\theta(x_t, t, s)$ to match the **average velocity** over $[t, s]$, using the [[math_concepts/mean-flow-identity]] to express that average via the instantaneous velocity and a time derivative of $F_\theta$ itself.

## Motivation

The shared goal of [[methods/shortcut-model]] and Mean Flow is the same: one [[ml_concepts/flow-map]] network $F_\theta(x_t, t, s)$ that can jump from any time $t$ to any time $s$ in a single forward pass, trained without a separate teacher. The question is what self-consistency to enforce.

ShortCut uses interval additivity: $F(t \to s) = F(t \to r \to s)$. This is correct but couples two evaluations of the network at *different intervals*. The training signal at the longer interval $[t, s]$ depends on the network's prediction at the shorter $[t, r]$, which is itself only as accurate as the network has learned to be. Errors propagate as the integrals grow longer, and the signal at short intervals — where the [[ml_concepts/flow-matching]] head anchors $F$ — has to travel through nested compositions to reach far-apart $(t, s)$ pairs.

Mean Flow swaps the integral identity for a *differential* one. Define $F_\theta$ directly as the average velocity over $[t, s]$, multiply through by $(s - t)$, differentiate, and rearrange. The result is $F_\theta(x_t, t, s) = v(x_t, t) - (s - t)\,\tfrac{\mathrm{d}}{\mathrm{d}t} F_\theta(x_t, t, s)$. The right-hand side ties $F$ to the instantaneous velocity at the *single* point $(x_t, t)$ plus a correction computed as a JVP through $F_\theta$ itself. No second composition pass through the network. The identity is pointwise in $(x_t, t)$, so the supervision signal at every $(t, s)$ pair grounds out directly in the FM-trained velocity head — closer to a local constraint, further from the error-propagation pattern of nested integrals.

## Problem setting

Same as [[methods/shortcut-model]]: one network, any number of inference steps, no separate teacher network. Mean Flow gives a different self-consistency derived from a *differential* identity rather than from interval additivity.

## The parametrisation

Mean Flow defines

$$
F_\theta(x_t, t, s) \;\approx\; \frac{1}{s - t}\int_t^s v(x_u, u)\,\mathrm{d}u,
$$

i.e. $F_\theta$ is the **average instantaneous velocity** over $[t, s]$. The corresponding sampling step is

$$
\Psi_{t \to s}(x_t) \;\approx\; x_t + (s - t)\,F_\theta(x_t, t, s).
$$

At $s = t$ the average degenerates to the instantaneous velocity: $F_\theta(x_t, t, t) = v(x_t, t)$. This is the boundary condition.

## The Mean Flow Identity

Multiply both sides by $(s - t)$ and differentiate w.r.t. $t$. The calculation, walked through in [[math_concepts/mean-flow-identity]], yields

$$
\boxed{\;F_\theta(x_t, t, s) \;=\; v(x_t, t) \;-\; (s - t)\,\frac{\mathrm{d}}{\mathrm{d}t} F_\theta(x_t, t, s)\;}
$$

This is the central training signal: the LHS is the network's output; the RHS uses the instantaneous velocity $v$ (from a flow-matching head) plus a time-derivative of $F_\theta$ itself. The $\mathrm{d}/\mathrm{d}t$ is the **total** derivative along the trajectory, so

$$
\frac{\mathrm{d}}{\mathrm{d}t} F_\theta(x_t, t, s) \;=\; \partial_t F_\theta + (\partial_x F_\theta)\,v(x_t, t),
$$

computable from one JVP through the network (with $v$ providing the direction in $x$).

## Training objective

$$
\mathcal{L}_{\text{MF}}(\theta) \;=\; \big\lVert F_\theta(x_t, t, s) - \operatorname{sg}\big(v_\theta(x_t, t) - (s - t)\,\tfrac{\mathrm{d}}{\mathrm{d}t} F_\theta(x_t, t, s)\big) \big\rVert_2^2 \;+\; \mathcal{L}_{\text{FM}}.
$$

Components:

- The squared term is the Mean Flow Identity, used as a stop-gradient target: the network's $F_\theta$ should agree with the identity's RHS.
- $\mathcal{L}_{\text{FM}}$ is the standard flow-matching loss applied to $v_\theta(x_t, t) = F_\theta(x_t, t, t)$ — the diagonal of the flow map serves as the velocity head, so the same network outputs both $v$ and $F$.

At inference: same as ShortCut. Pick a schedule, step $x_{n-1} = x_n + (t_{n-1} - t_n)\,F_\theta(x_n, t_n, t_{n-1})$. 1 step works; more steps help quality.

## Mean Flow vs ShortCut

Both train a flow map $F(x_t, t, s)$ with stop-gradient self-consistency. The difference is which identity is enforced:

| Method                | Identity used                                                                       | Extra cost during training |
|-----------------------|-------------------------------------------------------------------------------------|----------------------------|
| [[methods/shortcut-model]] | Integral: $F(t, s) \approx F(F(t, r), r, s)$ — one extra forward pass            | 1 extra forward            |
| [[methods/mean-flow]] | Differential: $F = v - (s - t)\,\mathrm{d}F/\mathrm{d}t$ — one JVP through the net | 1 JVP                      |

The differential identity gives a closer-to-pointwise signal; the integral identity gives a more "global" coupling between intervals.

## Properties

- **Step count at inference:** 1–4 typically.
- **Boundary:** $F_\theta(x_t, t, t) = v_\theta(x_t, t)$, enforced jointly with FM.
- **Compute:** training needs JVP capability (PyTorch `torch.func.jvp` or equivalent); inference is one forward pass per step.

## Variants and successors

- [[methods/shortcut-model]] — integral-identity counterpart.
- "Mean Flows for One-step Generative Modeling" (Geng et al., 2025) — the paper this lecture refers to.

## Sources

- [[sources/flow-map-models-lecture]] — definition, Mean Flow Identity, training objective, and the diagram of $v$, $F$, and the correction term $-(s - t)\,\mathrm{d}F/\mathrm{d}t$.

## Up next

- [[methods/shortcut-model]] — the integral-identity counterpart; comparing the two pinpoints what the differential identity buys.
- [[topics/few-step-generative-models]] — situates Mean Flow among consistency models, shortcut models, and progressive distillation.
