---
title: How is the Mean Flow time-derivative dF/dt computed in practice?
type: question
tags: [mean-flow, flow-map, jvp, autograd]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# How is the Mean Flow time-derivative $\mathrm{d}F/\mathrm{d}t$ computed in practice?

## Why it matters

[[math_concepts/mean-flow-identity]] использует $\tfrac{\mathrm{d}}{\mathrm{d}t} F_\theta(x_t, t, s)$ как supervision-сигнал. Это *полная* производная вдоль траектории:

$$
\frac{\mathrm{d}}{\mathrm{d}t} F_\theta(x_t, t, s) \;=\; \partial_t F_\theta \;+\; (\nabla_x F_\theta)\,v(x_t, t).
$$

Чтобы обучать Mean Flow, эту величину нужно считать для каждого сэмпла на каждом шаге. Реализация имеет значение: наивный autograd-over-autograd обходится дорого.

## What we know so far

- Правильный инструмент — **forward-mode Jacobian-vector product (JVP)** через $F_\theta$ в направлении $v(x_t, t)$, причём аргумент $t$ несёт собственный tangent $1$. Один JVP сразу даёт и $\partial_t F$, и $(\nabla_x F) \cdot v$.
- В PyTorch: `torch.func.jvp(lambda x, t: F(x, t, s), (x_t, t), (v, ones))`.
- Стоимость: примерно один forward pass через $F_\theta$ — forward-mode AD дёшев, когда направление tangent одно.

## What would resolve it

- Полная реализация цикла обучения с использованием JVP, бухгалтерией loss и расстановкой stop-gradient.
- Подтверждение из оригинальной статьи Mean Flow (Geng et al. 2025), что они используют именно JVP, а не какой-то суррогат.

## Related

- [[methods/mean-flow]]
- [[math_concepts/mean-flow-identity]]
- [[sources/flow-map-models-lecture]]
