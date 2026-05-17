---
title: Why does Consistency Training work without a teacher?
type: question
tags: [consistency-models, training, theory]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# Why does Consistency Training work without a teacher?

## Why it matters

[[methods/distillation/consistency-training]] утверждает, что [[ml_concepts/generative/consistency-function]] можно обучить, не запуская ни одного шага diffusion-солвера. Звучит почти слишком дёшево. Понимание, *почему* это работает, проясняет, что именно представляет полученная модель и когда CT-сэмплы расходятся с CD-сэмплами.

## What we know so far

- Трюк: пара $(x_n, x_{n-1})$ строится из **одного и того же** noise-вектора $\epsilon$: $x_n = x_0 + t_n\,\epsilon$, $x_{n-1} = x_0 + t_{n-1}\,\epsilon$.
- Эта пара лежит на **прямой** в $(x, t)$. Лекция выводит это из приближения условного score'а $\nabla_x \log p_t(x) \approx -(x - x_0)/t^2$, которое сворачивает [[ml_concepts/generative/probability-flow-ode]] к $\mathrm{d}x = (x - x_0)/t\,\mathrm{d}t$.
- То есть CT учит flow-map для **спрямлённого** ODE, а не для исходного diffusion ODE.

## Open sub-questions

- Спрямлённый ODE и исходный diffusion ODE в общем случае различаются (условный score равен score только в среднем, не поточечно). Каков зазор и когда он значим?
- Эквивалентен ли CT по сути цели rectified-flow? Статья «Consistency Flow Matching» (2024), кажется, утверждает, что да.
- На практике CT-сэмплы могут быть чёткими за 1 шаг. Это потому, что прямой ODE проще обращать, или потому, что CT регуляризует низкочастотное содержимое?

## Related

- [[methods/distillation/consistency-training]]
- [[methods/distillation/consistency-distillation]]
- [[ml_concepts/generative/consistency-function]]
- [[sources/flow-map-models-lecture]]
