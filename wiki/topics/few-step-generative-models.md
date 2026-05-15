---
title: Few-step Generative Models
type: topic
tags: [generative-models, diffusion, flow-matching, distillation, sampling]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Few-step Generative Models

> Methods that turn a slow many-step ODE-based generator (diffusion, flow matching) into a model that produces samples in 1–4 forward passes, either by distilling a multi-step teacher or by directly learning the integrated solution of the generative ODE.

## The setting

A diffusion model generates by integrating a deterministic ODE backwards in time. A learned velocity field (or score) tells you how to move noise toward data; the ODE solver does the moving. The trajectory between noise and data curves through high-dimensional space, so a single Euler step from $t = \sigma$ to $t = 0$ lands far from the data manifold. In practice you need tens to hundreds of steps to keep the integration error small. Each step is a full network forward pass. Generating one image costs as much as running the model 50–100 times.

Few-step generative models reject that cost. They keep the diffusion-trained substrate — well-defined sampling distribution, mode coverage, stable training — but force inference into a handful of evaluations. Two families dominate the design space. Either bolt a student onto an existing many-step teacher and force the student to reproduce its output in fewer steps, or re-parametrise the learned object so that a single forward pass already represents a long integration. Both ideas show up in the methods below, often mixed.

## Core ideas

The substrate is a [[ml_concepts/probability-flow-ode]]. For diffusion, this is the deterministic counterpart of the noising SDE; for flow matching, the ODE that transports a prior to data along learned vector fields. Sampling means solving this ODE, and the cost of sampling is the number of solver steps.

A [[ml_concepts/flow-map]] is the change of perspective that drives the rest of the area. Instead of learning the *instantaneous* velocity $v(x_t, t)$ — the derivative of the trajectory at a single point — learn the *integrated* solution $\Psi_{t \to s}(x_t)$ directly: a function that takes a state at time $t$ and returns the state at time $s$. Once you have $\Psi_{0 \leftarrow \sigma}$ for the full interval, sampling is one network call. The whole few-step research direction is about how to fit a flow map accurate enough to skip the ODE solver.

The simplest flow-map target is the one that lands at the data. A [[ml_concepts/consistency-function]] is a flow map $\Psi_{0 \leftarrow t}$ defined for every $t$, with one constraint: points on the same probability-flow trajectory must map to the same data sample. That single property is what makes consistency models trainable without an explicit teacher, and what gives the family its name.

[[ml_concepts/step-distillation]] is the older framing the area grew out of. Train a fast student to mimic a slow multi-step teacher's *output*, treating the teacher's many-step trajectory as the supervision signal. This works whether or not the student also has flow-map structure imposed on it. The methods below mix these two ideas — flow-map parametrisation and step distillation — in different ratios.

## Methods that grow from these ideas

[[methods/progressive-distillation]] was the first method to push few-step sampling at scale. Train a student to reproduce two teacher steps in one, then repeat the distillation on the new student until you reach one step. Each round halves the number of steps. The student is a re-parametrised teacher — no flow-map structure, no consistency constraint — so it accumulates error every time you cut steps, and image quality degrades sharply at the very end of the schedule.

[[methods/consistency-distillation]] is the flow-map analogue. Train a consistency function by enforcing that adjacent points on a teacher-generated trajectory map to the same output: the student sees $x_t$ from one teacher step and $x_{t - \Delta t}$ from the next, and the loss pushes both to produce the same prediction. The teacher gives ground-truth trajectories; the consistency constraint gives the structural property. One forward pass from any $t$ to $0$ produces a sample.

[[methods/consistency-training]] removes the teacher entirely. Pick two times $t < s$, draw the *same* Gaussian noise $\varepsilon$, build the two noisy versions $x_t = x_0 + t\varepsilon$ and $x_s = x_0 + s\varepsilon$ — both lie on the same straight-line trajectory between $x_0$ and the noise endpoint — and impose the consistency constraint on those two points. No teacher, no pre-trained diffusion network. The trick is that "same $\varepsilon$" guarantees the two points sit on the same trajectory in the straight-line transport.

[[methods/multistep-consistency-model]] is the natural relaxation when one consistency function isn't accurate enough across all of $[0, \sigma]$. Split the interval into $K$ sub-intervals, learn a separate flow map per interval, and sample by chaining $K$ forward passes — usually $K = 2$ or $K = 4$. This bridges the quality gap between one-step CMs and many-step diffusion, paying for accuracy in forward passes rather than in distillation rounds.

[[methods/shortcut-model]] generalises beyond "all flow maps land at zero". Learn $F(x_t, t, s)$ for arbitrary $t, s$, and impose the interval-additivity constraint that going from $t$ to $s$ should equal going $t \to u \to s$ for any intermediate $u$. This is a self-consistency loss that, with a stop-gradient on one side of the equality, gives a single network the full $\Psi_{t \to s}$ family without a teacher.

[[methods/mean-flow]] reframes the same flow map as the *average velocity* over $[t, s]$. Average velocity is the kind of quantity natural to learn but apparently intractable — averaging needs the trajectory you're trying to skip. The [[math_concepts/mean-flow-identity]] expresses average velocity in terms of one instantaneous velocity call plus a time derivative of $F$, making the training target a local quantity. The model is trained to satisfy the identity at every $(x_t, t, s)$ triple.

## Open threads

- [[questions/why-cant-cms-use-ode-solvers]] — why consistency models cannot use standard ODE solvers.
- [[questions/how-is-mean-flow-time-derivative-computed]] — how $\mathrm{d}F/\mathrm{d}t$ along the trajectory is computed in practice (JVP via autograd).
- [[questions/why-does-consistency-training-work-without-teacher]] — why the same-$\varepsilon$ straight-path trick suffices for the consistency constraint.

## Reading order (recap)

1. [[ml_concepts/probability-flow-ode]]
2. [[ml_concepts/flow-map]]
3. [[ml_concepts/consistency-function]]
4. [[ml_concepts/step-distillation]]
5. [[methods/progressive-distillation]]
6. [[methods/consistency-distillation]]
7. [[methods/consistency-training]]
8. [[methods/multistep-consistency-model]]
9. [[methods/shortcut-model]]
10. [[math_concepts/mean-flow-identity]] → [[methods/mean-flow]]

## Reading queue

- Song et al., "Consistency Models" (2023) — original CMs paper.
- Heek et al., "Multistep Consistency Models" (2024).
- Frans et al., "One-step Diffusion via Shortcut Models" (2024).
- Geng et al., "Mean Flows for One-step Generative Modeling" (2025).
- Sabour et al., "Align Your Flow: Scaling Continuous-Time Flow-Map Distillation" (2025).

## Sources

- [[sources/flow-map-models-lecture]] — lecture covering the unifying flow-map perspective on CMs, ShortCut, and Mean Flow.
