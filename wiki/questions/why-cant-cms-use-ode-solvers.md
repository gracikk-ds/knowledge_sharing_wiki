---
title: Why can't consistency models be plugged into ODE solvers?
type: question
tags: [consistency-models, ode, sampling]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
---

# Why can't consistency models be plugged into ODE solvers?

## Why it matters

ODE-солверы (Heun, DPM-Solver, RK4) — зрелый инструментарий для сэмплирования diffusion-моделей. Если бы они применимы к CMs, не понадобилась бы отдельная стохастическая multistep-процедура, чтобы получать сэмплы из CMs за 4–5 шагов.

## What we know so far

- [[ml_concepts/generative/consistency-function]] — это [[ml_concepts/generative/flow-map]]: на выходе уже *проинтегрированное* решение $\Psi_{t \to 0}(x_t)$, а не velocity.
- ODE-солверы предназначены интегрировать *производную*. Подать им уже проинтегрированную величину — категориальная ошибка: нет $f'$-сигнала, чтобы сделать шаг.
- Это и есть практическая причина, по которой в лекции вводится стохастический multistep-сэмплер.

## What would resolve it

- Формальное описание класса объектов, на которых работают ODE-солверы (векторные поля на $\mathbb{R}^d \times [0, T]$), и доказательство, что выход flow-map без дифференцирования в этот класс не попадает.
- Восстанавливает ли *численное* дифференцирование $f_\theta$ по $t$ пригодное векторное поле. Скорее нет: $f_\theta$ приближённая, и производная усилит ошибку.

## Related

- [[ml_concepts/generative/flow-map]]
- [[ml_concepts/generative/consistency-function]]
- [[sources/flow-map-models-lecture]]
