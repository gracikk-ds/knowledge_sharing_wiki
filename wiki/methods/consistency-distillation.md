---
title: Consistency Distillation (CD)
type: method
tags: [consistency-models, distillation, diffusion, few-step-generation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Consistency Distillation (CD)

> Train a [[ml_concepts/consistency-function]] by using a pre-trained diffusion teacher to generate trajectory pairs, then enforcing the self-consistency loss on them.

## Motivation

We have a [[ml_concepts/diffusion-model]] that samples well but needs 30–80 [[ml_concepts/probability-flow-ode]] steps per image. The goal is a student that takes one step, or at most a handful. The shape of student we want is a [[ml_concepts/consistency-function]] $f_\theta(x_t, t)$ that maps any noisy point on a trajectory to its clean endpoint $x_0$. The defining property is invariance along the trajectory: $f_\theta(x_t, t) = f_\theta(x_s, s)$ for any two times $t, s$ on the same path. Train that, sample in one step.

The naive way to enforce it is to pick a noise level $t$, ask the network for $f_\theta(x_t, t)$, and supervise it with the ground-truth $x_0$. This works in principle but throws away the structure that makes consistency models cheap. The loss only ties $x_t$ to $x_0$ — it never asks the network to be invariant *between two nearby noisy points on the same trajectory*. Without that pairing the network is doing one-shot regression from arbitrary noise to clean data, which is exactly what diffusion teachers needed many steps to learn.

To get the pairing we need two points on the same trajectory. The forward noising process gives $x_t$ easily, but where does the matched $x_{t-\Delta}$ come from? A pre-trained teacher solves it. One step of the teacher's deterministic ODE solver, started at $(x_t, t)$, returns $\hat{x}_{t-\Delta}$ — the next point on the same trajectory, up to the solver's truncation error. Consistency distillation is exactly that: noise to $x_t$, run one teacher step to get $\hat{x}_{t-\Delta}$, apply the student to both points, push the two outputs together. The teacher contributes structure only — not labels — and the student inherits its trajectory geometry compressed into one network call.

## Problem setting

A pre-trained diffusion (or flow-matching) model $\Phi(\cdot \mid \phi)$ is available; you want a student $f_\theta$ that can sample in 1–4 steps.

## Algorithm

Discretise the time horizon into $t_0 < t_1 < \ldots < t_N$ (with $t_0 = \epsilon$ small but positive). One training step:

1. Sample $x_0 \sim p_{\text{data}}$ and $n \sim \mathcal{U}\{1, \ldots, N\}$.
2. Forward-noise to time $t_n$: $x_n = x_0 + t_n\,\xi$, $\xi \sim \mathcal{N}(0, I)$. So $x_n \sim \mathcal{N}(x_0, t_n^2 I)$.
3. Run **one step** of the teacher's ODE solver to get the trajectory's previous point:
   $$\hat{x}_{n-1} \;=\; \Phi(x_n,\, t_n,\, t_{n-1} \mid \phi).$$
4. Apply the student to both points and minimise the squared difference:
   $$\mathcal{L}_{\text{CD}}(\theta) \;=\; \mathbb{E}\big\lVert f_\theta(\hat{x}_{n-1}, t_{n-1}) - f_\theta(x_n, t_n) \big\rVert_2^2.$$
5. Enforce the boundary $f_\theta(x_0, t_0) = x_0$ by parametrising $f_\theta(x, t) = c_{\text{skip}}(t) \cdot x + c_{\text{out}}(t) \cdot F_\theta(x, t)$ with $c_{\text{skip}}(t_0) = 1$, $c_{\text{out}}(t_0) = 0$.

A target network (EMA of $\theta$) is typically used on the $\hat{x}_{n-1}$ branch to stabilise training, similar to BYOL/TD-learning.

## Why it works

The teacher's deterministic ODE provides the only missing ingredient: neighbouring points on the *same* trajectory. Without that, "self-consistency along a trajectory" cannot be enforced because you have no way to pair a point at $t_n$ with the corresponding point at $t_{n-1}$. The forward noising process gives $x_n$; the teacher's one solver step gives $\hat{x}_{n-1}$. Together they are a valid trajectory pair (up to the solver's truncation error).

The boundary condition rules out the trivial $f_\theta \equiv 0$ (which would minimise the self-consistency loss without learning anything useful).

## Properties

- **Step count at inference:** 1 step (greedy) or 4–5 stochastic steps.
- **Quality vs teacher:** loses some quality at 1 step, comparable at 4 steps.
- **Compute cost during training:** one teacher call per training step (the one solver step). Negligible compared to retraining the teacher.
- **Failure modes:** target collapse if the boundary is mis-parametrised; numerical issues if the teacher's solver step is too coarse.

## Variants and successors

- [[methods/consistency-training]] — drop the teacher; use a straight reference path instead.
- [[methods/multistep-consistency-model]] — relax "always project to 0" to "project to the next boundary".
- "Improved Techniques for Training Consistency Models" — variance-reduction and schedule tricks (not in this source).

## Sources

- [[sources/flow-map-models-lecture]] — derivation of the CD loss, boundary condition trick, and motivation.

## Up next

- [[methods/multistep-consistency-model]] — relax "always project to $t=0$" to "project to the next boundary"; recovers most of the teacher's quality with 4 inference steps.
- [[topics/few-step-generative-models]] — the broader area: flow maps, shortcut models, mean flow, and how CD sits among them.
