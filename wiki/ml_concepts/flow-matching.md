---
title: Flow Matching
type: ml_concept
tags: [generative-models, flow-matching, ode]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# Flow Matching

> A generative-modelling framework that learns a time-dependent velocity field $v(x, t)$ of an ODE that transports a simple prior to data.

Stub. The current wiki touches flow matching only as the "instantaneous velocity" baseline that [[methods/shortcut-model]] and [[methods/mean-flow]] build on:

- Flow matching: learn $v(x, t)$ such that $\mathrm{d}x = v(x, t)\,\mathrm{d}t$ maps a Gaussian prior to data.
- Flow-map methods: learn the *integrated* form $F(x, t, s)$ directly.
- The diagonal $F(x, t, t) = v(x, t)$ connects the two; the flow-map network often outputs both via the same backbone.

A proper draft awaits ingest of Lipman et al. 2023 or related.

## Sources

- [[sources/flow-map-models-lecture]] — context; not the primary source.
