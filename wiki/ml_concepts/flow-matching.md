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

> Фреймворк генеративного моделирования, в котором обучают зависящее от времени поле скоростей $v(x, t)$ ODE, переносящего простой prior в данные.

Стаб. Текущая вики касается flow matching только как «instantaneous velocity»-бэйзлайна, на котором строятся [[methods/shortcut-model]] и [[methods/mean-flow]]:

- Flow matching: выучить $v(x, t)$ так, чтобы $\mathrm{d}x = v(x, t)\,\mathrm{d}t$ переносил гауссовский prior в данные.
- Flow-map методы: выучить напрямую *проинтегрированную* форму $F(x, t, s)$.
- Диагональ $F(x, t, t) = v(x, t)$ связывает эти два взгляда; flow-map сеть часто выдаёт оба объекта через общий бэкбон.

Полноценный draft ждёт ингеста Lipman et al. 2023 или близких работ.

## Sources

- [[sources/flow-map-models-lecture]] — контекст; не основной источник.
