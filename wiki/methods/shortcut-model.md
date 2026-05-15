---
title: Shortcut Models
type: method
tags: [flow-map, generative-models, flow-matching, few-step-generation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Shortcut Models

> A [[ml_concepts/flow-map]] $F_\theta(x_t, t, s)$ trained with an **interval-additivity** self-consistency: a single jump from $t$ to $s$ must equal two smaller jumps $t \to r \to s$ (stop-gradient on the RHS).

## Motivation

Consistency models give one-step generation but lock the target time at $t = 0$. To choose the inference step count at sampling time — 1 step today, 4 steps tomorrow when quality matters more — the network has to take *both* endpoints as inputs: a [[ml_concepts/flow-map]] $F_\theta(x_t, t, s)$ that can jump from any $t$ to any $s$. The training question is how to supervise this two-argument function without a separate teacher network producing trajectory pairs at every $(t, s)$.

[[ml_concepts/flow-matching]] already gives a clean local signal: at $s = t$, the flow map should equal the instantaneous velocity $v(x_t, t)$. That fixes the diagonal of $F_\theta$ but says nothing about off-diagonal entries — the case where $s$ is far from $t$, which is exactly the regime where one-step sampling lives. Some constraint has to link short intervals (where FM trains directly) to long intervals (where one-step sampling needs the answer).

The true ODE flow has a property tailor-made for this: interval additivity. Integrating the velocity from $t$ to $s$ equals integrating it from $t$ to $r$ and then from $r$ to $s$. In flow-map form: $F(t \to s) = F\big(F(x_t, t, r),\, r, s\big)$. Use this as a stop-gradient regression target — the LHS is the network's prediction at the long interval, the RHS is the network's own composition through an intermediate point $r$, frozen. The stop-gradient prevents the trivial $F \equiv 0$ solution and turns the FM-anchored short-interval predictions into supervision for longer ones. The two losses together — FM at the diagonal, interval-additivity off-diagonal — train a single network that samples at any step count.

## Problem setting

You have access to flow-matching training (or want to add it as a side loss). You want a single network that can produce a sample in 1, 2, 4 or more steps without retraining.

## The principle

The true ODE flow satisfies **interval additivity**:

$$
\int_t^s v(x_u, u)\,\mathrm{d}u \;=\; \int_t^r v(x_u, u)\,\mathrm{d}u + \int_r^s v(x_u, u)\,\mathrm{d}u,\qquad t \le r \le s.
$$

Translated to flow maps $F$ (which represent the average velocity over the interval), this becomes a self-consistency constraint: jumping $t \to s$ directly must agree with jumping $t \to r$ and then $r \to s$.

## Algorithm

Train a network $F_\theta(x_t, t, s)$ against two losses.

1. **Flow-matching boundary** (standard FM loss at $s = t$):
   $$F_\theta(x_t, t, t) \;\approx\; v_\theta(x_t, t),$$
   i.e. the diagonal of the flow map equals the instantaneous velocity, trained as in flow matching.

2. **Shortcut self-consistency** (across two sub-intervals):
   $$\mathcal{L}_{\text{SC}}(\theta) \;=\; \big\lVert F_\theta(x_t, t, s) - \operatorname{sg}\big(F_\theta(F_\theta(x_t, t, r), r, s)\big) \big\rVert_2^2.$$

   The stop-gradient $\operatorname{sg}(\cdot)$ on the RHS prevents the trivial $F \equiv 0$ solution and stabilises training (the RHS is the supervised target, the LHS is the prediction).

At inference, pick a schedule $t_N > \ldots > t_0$ and step: $x_{n-1} = x_n + (t_{n-1} - t_n)\,F_\theta(x_n, t_n, t_{n-1})$. The same $F_\theta$ works for any step count.

## Why it works

The two losses together approximate the integral of the true velocity over arbitrary intervals: the FM loss anchors $F$ to the velocity at $s = t$, and the shortcut loss propagates that anchor along longer intervals via the interval-additivity identity.

The stop-gradient is the key implementation detail. Without it, the network can satisfy the constraint trivially by collapsing $F$ to zero or to any function of $(x, t)$ alone (independent of $s$). With it, the supervision flows from short intervals (where the FM boundary is informative) outward to longer intervals.

## Properties

- **Step count at inference:** any. The same network covers 1-step, 2-step, 4-step, etc.
- **Training:** one network, one extra forward pass per training step (for the inner $F_\theta(x_t, t, r)$ in the consistency loss).
- **Boundary:** the diagonal $F_\theta(x_t, t, t) = v_\theta(x_t, t)$.

## Variants and successors

- [[methods/mean-flow]] — closely related: same flow-map parametrisation, but uses a *differential* identity (Mean Flow Identity) instead of an *integral* identity (interval additivity).
- [[methods/consistency-distillation]] — fixed target time $s = 0$; no free time-of-arrival argument.

## Sources

- [[sources/flow-map-models-lecture]] — interval-additivity equation, stop-gradient self-consistency loss, diagram showing the $t \to r \to s$ factoring.

## Up next

- [[methods/mean-flow]] — same parametrisation, but uses a differential identity instead of interval additivity; cheaper supervision per step.
- [[topics/few-step-generative-models]] — situates shortcut models among consistency methods, mean flow, and progressive distillation.
