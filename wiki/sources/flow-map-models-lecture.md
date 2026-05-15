---
title: "Few-step Generative Models (Flow-Map models, ODE integrators) — lecture"
type: source
source_path: raw/lectures/flow-map-models.pdf
source_kind: lecture
source_date: 2025-01-01
ingested: 2026-05-15
tags: [flow-map, consistency-models, mean-flow, shortcut-models, distillation, diffusion]
sources: 1
status: draft
---

# Few-step Generative Models — lecture

> A 31-slide lecture covering why diffusion is slow, why knowledge distillation is fast, and the modern toolkit of flow-map methods (Consistency Models, Multistep CMs, ShortCut, Mean Flow).

## Key takeaways

- **Why diffusion is slow.** The probability-flow ODE has curved trajectories; a 1-step Euler approximation lands far from data. Practically you need 50–200 forward passes.
- **Why distillation is fast.** Diffusion's training objective is **one-to-many** (one $x_t$ is consistent with many $x_0$), so the network's optimum at high noise is a blurry conditional mean. Distillation replaces this with a **one-to-one** target from the teacher's deterministic solver, which a single forward pass can match.
- **Flow map unifies the modern toolkit.** Instead of learning the velocity $v(x, t)$, learn the integrated solution $F(x, t, s)$ directly. CMs, ShortCut, and Mean Flow are all flow maps under different self-consistency principles.
- **Consistency function** $f(x_t, t) \mapsto x_0$ with self-consistency $f(x_t, t) = f(x_s, s)$ along a trajectory. Two training recipes: CD (uses a teacher) and CT (uses a straight reference path with shared $\epsilon$).
- **CMs are not vector fields.** They cannot be plugged into ODE solvers — sampling uses stochastic multistep (project to $x_0$, re-noise, project again, ~4–5 rounds).
- **Multistep CMs** sidestep "approximate the whole interval" by splitting $[0, \sigma]$ into $N$ boundaries and learning a CM per interval. 4 steps $\approx$ 50-step teacher in the lecture's qualitative comparison.
- **Shortcut models** train $F(x_t, t, s)$ with stop-gradient interval-additivity: $F(t, s) \approx F(F(t, r), r, s)$.
- **Mean Flow (2025)** trains $F(x_t, t, s)$ to match the *average* velocity over $[t, s]$. The **Mean Flow Identity** $F = v(x_t, t) - (s - t)\,\mathrm{d}F/\mathrm{d}t$ is the training signal, with the total derivative implemented as a JVP.

## Concepts touched

- [[ml_concepts/flow-map]] — the unifying organising concept of the lecture; new wiki page.
- [[ml_concepts/consistency-function]] — definition, self-consistency, boundary condition; new wiki page.
- [[ml_concepts/step-distillation]] — one-to-many vs one-to-one explanation, one-step vs multi-step KD; new wiki page.
- [[ml_concepts/diffusion-model]] — referenced as the slow teacher; stub.
- [[ml_concepts/flow-matching]] — referenced as the instantaneous-velocity baseline; stub.
- [[ml_concepts/probability-flow-ode]] — the ODE the trajectory lives on; stub.
- [[ml_concepts/score-function]] — used in CT derivation; stub.
- [[methods/consistency-distillation]] — full algorithm; new wiki page.
- [[methods/consistency-training]] — straight-path derivation; new wiki page.
- [[methods/multistep-consistency-model]] — multi-boundary CM definition and objective; new wiki page.
- [[methods/shortcut-model]] — interval-additivity loss; new wiki page.
- [[methods/mean-flow]] — Mean Flow Identity and objective; new wiki page.
- [[methods/progressive-distillation]] — mentioned as multi-step KD; stub.
- [[math_concepts/mean-flow-identity]] — derivation walked through; new wiki page.
- [[topics/few-step-generative-models]] — umbrella; new wiki page.

## Contradictions and revisions

None. This is the wiki's first content ingest, so there is nothing to contradict yet.

## Questions raised

- [[questions/why-cant-cms-use-ode-solvers]]
- [[questions/how-is-mean-flow-time-derivative-computed]]
- [[questions/why-does-consistency-training-work-without-teacher]]

## Notes

- The final slide is a Russian-language meme ("Айтишники всё!") — a humorous sign-off, not technical content. Not ingested.
- The slide deck name-drops a longer reading list including "Stable Consistency Tuning", "Consistency Models Made Easy", "One-step Diffusion via Shortcut Models", "Mean Flows for One-step Generative Modeling", "Inductive Moment Matching", and "Align Your Flow". Added to the reading queue on [[topics/few-step-generative-models]].

## Pointer back to raw

`raw/lectures/flow-map-models.pdf`
