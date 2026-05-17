---
title: Shortcut Models
type: method
tags: [flow-map, generative-models, flow-matching, few-step-generation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Shortcut Models

> [[ml_concepts/flow-map]] $F_\theta(x_t, t, s)$, обученный со **interval-additivity** self-consistency: один прыжок из $t$ в $s$ должен совпадать с двумя меньшими $t \to r \to s$ (stop-gradient на правой части).

## Motivation

Consistency models дают one-step генерацию, но фиксируют целевой момент в $t = 0$. Чтобы выбирать число шагов inference на этапе сэмплирования — 1 шаг сегодня, 4 шага завтра, когда важнее качество — сеть должна принимать *оба* конца в качестве входов: [[ml_concepts/flow-map]] $F_\theta(x_t, t, s)$, способный прыгать с любого $t$ в любой $s$. Вопрос обучения — как супервизировать эту функцию двух аргументов без отдельного учителя, поставляющего пары на траектории для каждого $(t, s)$.

[[ml_concepts/flow-matching]] уже даёт чистый локальный сигнал: при $s = t$ flow map должен совпадать с мгновенной скоростью $v(x_t, t)$. Это фиксирует диагональ $F_\theta$, но ничего не говорит про off-diagonal — случай, когда $s$ далеко от $t$, а именно в этом режиме живёт one-step сэмплирование. Нужно ограничение, связывающее короткие интервалы (где FM обучает напрямую) с длинными (где one-step сэмплирование требует ответа).

Истинный ODE-flow обладает свойством, специально подходящим для этой задачи, — interval additivity. Интегрирование скорости от $t$ до $s$ равно интегрированию от $t$ до $r$ и потом от $r$ до $s$. В терминах flow map: $F(t \to s) = F\big(F(x_t, t, r),\, r, s\big)$. Используем это как stop-gradient регрессионный таргет: слева — предсказание сети на длинном интервале, справа — собственная композиция сети через промежуточную точку $r$, замороженная. Stop-gradient отсекает тривиальное $F \equiv 0$ и превращает FM-якорные предсказания на коротких интервалах в supervision для длинных. Два loss'а вместе — FM на диагонали, interval additivity вне её — обучают одну сеть, способную сэмплировать на любом числе шагов.

## Problem setting

Есть доступ к flow-matching обучению (или хочется добавить его как side-loss). Нужна одна сеть, способная давать сэмпл за 1, 2, 4 или больше шагов без переобучения.

## The principle

Истинный ODE-flow удовлетворяет **interval additivity**:

$$
\int_t^s v(x_u, u)\,\mathrm{d}u \;=\; \int_t^r v(x_u, u)\,\mathrm{d}u + \int_r^s v(x_u, u)\,\mathrm{d}u,\qquad t \le r \le s.
$$

В терминах flow map $F$ (представляющего среднюю скорость на интервале) это становится self-consistency ограничением: прыгнуть $t \to s$ напрямую должно согласоваться с прыжками $t \to r$ и затем $r \to s$.

## Algorithm

Обучаем сеть $F_\theta(x_t, t, s)$ под два loss'а.

1. **Flow-matching boundary** (стандартный FM-loss при $s = t$):
   $$F_\theta(x_t, t, t) \;\approx\; v_\theta(x_t, t),$$
   диагональ flow map совпадает с мгновенной скоростью, обучается как в flow matching.

2. **Shortcut self-consistency** (через два под-интервала):
   $$\mathcal{L}_{\text{SC}}(\theta) \;=\; \big\lVert F_\theta(x_t, t, s) - \operatorname{sg}\big(F_\theta(F_\theta(x_t, t, r), r, s)\big) \big\rVert_2^2.$$

   Stop-gradient $\operatorname{sg}(\cdot)$ на правой части отсекает тривиальное $F \equiv 0$ и стабилизирует обучение (правая часть — таргет, левая — предсказание).

На inference берём расписание $t_N > \ldots > t_0$ и шагаем: $x_{n-1} = x_n + (t_{n-1} - t_n)\,F_\theta(x_n, t_n, t_{n-1})$. Один и тот же $F_\theta$ работает для любого числа шагов.

## Why it works

Два loss'а вместе приближают интеграл истинной скорости на произвольных интервалах: FM-loss якорит $F$ к скорости в $s = t$, а shortcut-loss продлевает этот якорь на длинные интервалы через тождество interval additivity.

Stop-gradient — ключевая деталь реализации. Без него сеть может удовлетворить ограничение тривиально, схлопнув $F$ до нуля или до любой функции $(x, t)$ одной (не зависящей от $s$). Со stop-gradient supervision течёт от коротких интервалов (где FM-граница информативна) наружу — к длинным.

## Properties

- **Число шагов на inference:** любое. Одна и та же сеть покрывает 1-step, 2-step, 4-step и т.д.
- **Обучение:** одна сеть, один дополнительный forward pass на шаг обучения (для внутреннего $F_\theta(x_t, t, r)$ в consistency-loss).
- **Граница:** диагональ $F_\theta(x_t, t, t) = v_\theta(x_t, t)$.

## Variants and successors

- [[methods/mean-flow]] — близкий родственник: та же параметризация flow map, но использует *дифференциальное* тождество (Mean Flow Identity) вместо *интегрального* (interval additivity).
- [[methods/consistency-distillation]] — фиксированное целевое время $s = 0$; нет свободного time-of-arrival аргумента.

## Sources

- [[sources/flow-map-models-lecture]] — уравнение interval additivity, stop-gradient self-consistency loss, диаграмма с факторизацией $t \to r \to s$.

## Up next

- [[methods/mean-flow]] — та же параметризация, но дифференциальное тождество вместо interval additivity; supervision дешевле на шаг.
- [[topics/few-step-generative-models]] — место shortcut models среди consistency методов, mean flow и progressive distillation.
