---
title: Diffusion Model
type: ml_concept
tags: [generative-models, diffusion, score-based-models]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
needs_rewrite: true
---

# Diffusion Model

> Генеративная модель, задающая forward noising-процесс $x_t = x_0 + t\,\epsilon$ и обучающаяся обращать его, предсказывая либо $x_0$, либо шум $\epsilon$, либо score $\nabla_x \log p_t(x)$.

Это стаб. Первый источник в вики — лекция по flow-map моделям — упоминает diffusion только как медленного учителя, чью ODE-траекторию обходят. Содержательное наполнение ждёт отдельного diffusion-источника (DDPM Ho/Jain/Abbeel, score-based от Song et al., EDM и т.п.).

## What is touched on in the current wiki

- Обратный процесс интегрирует [[ml_concepts/probability-flow-ode]] $\mathrm{d}x = -t\,\nabla_x \log p_t(x)\,\mathrm{d}t$.
- Training loss: $\mathcal{L}_{\text{diff}}(x_\phi) = \mathbb{E}_{t, x_0, \epsilon}\,\lVert x_\phi(x_t, t) - x_0 \rVert_2^2$.
- Forward noising — **one-to-many** ([[ml_concepts/step-distillation]] объясняет, почему это делает single-step inference принципиально трудным).

## Sources

- [[sources/flow-map-models-lecture]] — только контекст, не основной источник для концепта.
