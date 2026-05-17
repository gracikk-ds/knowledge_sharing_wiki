---
title: Score Function
type: ml_concept
tags: [generative-models, diffusion, score-based-models]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
needs_rewrite: true
---

# Score Function

> Градиент log-плотности $\nabla_x \log p_t(x)$, который выучивает score-based модель, чтобы прогонять обратный diffusion ODE/SDE.

Стаб. В текущей вики score-функция мелькает только в одной форме — **Tweedie / conditional-score**, используемой в [[methods/distillation/consistency-training]]:

$$
\nabla_x \log p_t(x) \;=\; -\,\frac{1}{t^2}\big(x - \mathbb{E}[x_0 \mid x]\big).
$$

Приближение $\mathbb{E}[x_0 \mid x] \approx x_0$ (одним сэмплом) превращает [[ml_concepts/generative/probability-flow-ode]] в прямую по $t$ — именно этот трюк и даёт CT возможность работать на парах траекторий с одинаковым $\epsilon$.

Полноценный draft ждёт ингеста отдельного score-based источника.

## Sources

- [[sources/flow-map-models-lecture]] — Tweedie identity цитируется при выводе CT.
