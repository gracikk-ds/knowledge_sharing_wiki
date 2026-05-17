---
title: Probability-Flow ODE
type: ml_concept
tags: [generative-models, diffusion, ode, score-based-models]
created: 2026-05-15
updated: 2026-05-17
sources: 1
status: stub
---

# Probability-Flow ODE

> Детерминированный ODE, чьи маргинальные распределения совпадают с маргиналами diffusion SDE; используется на inference, потому что решается стандартными ODE-солверами и воспроизводим из фиксированного шумового сэмпла.

Стаб. Текущая вики использует probability-flow ODE только как кривую, вдоль которой определена [[ml_concepts/consistency-function]]. В типичной параметризации (EDM-стиль):

$$
\mathrm{d}x \;=\; -\,t\,\nabla_x \log p_t(x)\,\mathrm{d}t.
$$

Вместе с приближением условного score $\nabla_x \log p_t(x) \approx -(x - \mathbb{E}[x_0 \mid x])/t^2$ это и есть ODE, который [[methods/consistency-training]] линеаризует в прямой reference-путь.

Полноценный draft ждёт ингеста Song et al. 2020 («Score-based generative modeling through SDEs») или EDM (Karras et al. 2022).

## Sources

- [[sources/flow-map-models-lecture]] — уравнение приведено, концепт используется как фон.
