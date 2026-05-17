---
title: "Few-step Generative Models (Flow-Map models, ODE integrators) — lecture"
type: source
source_path: raw/lectures/flow-map-models.pdf
source_kind: lecture
source_date: 2025-01-01
ingested: 2026-05-15
updated: 2026-05-17
tags: [flow-map, consistency-models, mean-flow, shortcut-models, distillation, diffusion]
sources: 1
status: mature
---

# Few-step Generative Models — lecture

> Лекция из 31 слайда: почему diffusion работает медленно, почему knowledge distillation работает быстро, и обзор современного инструментария flow-map методов (Consistency Models, Multistep CMs, ShortCut, Mean Flow).

## Key takeaways

- **Why diffusion is slow.** У probability-flow ODE искривлённые траектории; 1-шаговая аппроксимация Эйлера приземляется далеко от данных. На практике нужно 50–200 forward pass'ов.
- **Why distillation is fast.** Цель обучения diffusion — **one-to-many** (один $x_t$ согласован со многими $x_0$), поэтому оптимум сети на высокой шумности — размытое условное среднее. Distillation заменяет это на **one-to-one** target от детерминированного солвера учителя, и один forward pass способен его повторить.
- **Flow map unifies the modern toolkit.** Вместо velocity $v(x, t)$ обучаем напрямую проинтегрированное решение $F(x, t, s)$. CMs, ShortCut и Mean Flow — все это flow-map'ы под разными принципами self-consistency.
- **Consistency function** $f(x_t, t) \mapsto x_0$ с self-consistency $f(x_t, t) = f(x_s, s)$ вдоль траектории. Два рецепта обучения: CD (с учителем) и CT (с прямым reference path и общим $\epsilon$).
- **CMs are not vector fields.** Их нельзя подсунуть в ODE-солверы — сэмплирование идёт стохастическим multistep'ом (проекция в $x_0$, повторное зашумление, новая проекция, ~4–5 раундов).
- **Multistep CMs** обходят задачу «аппроксимировать весь интервал», разбивая $[0, \sigma]$ на $N$ границ и обучая по CM на каждый интервал. 4 шага $\approx$ 50-шаговый учитель в качественном сравнении лекции.
- **Shortcut models** обучают $F(x_t, t, s)$ с stop-gradient interval-additivity: $F(t, s) \approx F(F(t, r), r, s)$.
- **Mean Flow (2025)** обучает $F(x_t, t, s)$ соответствовать *средней* velocity на $[t, s]$. **Mean Flow Identity** $F = v(x_t, t) - (s - t)\,\mathrm{d}F/\mathrm{d}t$ — сигнал обучения, причём полная производная реализована через JVP.

## Concepts touched

- [[ml_concepts/flow-map]] — объединяющий организующий концепт лекции; новая страница.
- [[ml_concepts/consistency-function]] — определение, self-consistency, граничное условие; новая страница.
- [[ml_concepts/step-distillation]] — объяснение one-to-many vs one-to-one, one-step vs multi-step KD; новая страница.
- [[ml_concepts/diffusion-model]] — упоминается как медленный учитель; stub.
- [[ml_concepts/flow-matching]] — упоминается как instantaneous-velocity baseline; stub.
- [[ml_concepts/probability-flow-ode]] — ODE, в котором живёт траектория; stub.
- [[ml_concepts/score-function]] — используется при выводе CT; stub.
- [[methods/consistency-distillation]] — полный алгоритм; новая страница.
- [[methods/consistency-training]] — вывод через прямой путь; новая страница.
- [[methods/multistep-consistency-model]] — определение и цель multi-boundary CM; новая страница.
- [[methods/shortcut-model]] — interval-additivity loss; новая страница.
- [[methods/mean-flow]] — Mean Flow Identity и цель; новая страница.
- [[methods/progressive-distillation]] — упомянут как multi-step KD; stub.
- [[math_concepts/mean-flow-identity]] — вывод проходится шаг за шагом; новая страница.
- [[topics/few-step-generative-models]] — общая зонтичная тема; новая страница.

## Contradictions and revisions

Нет. Это первый содержательный ингест в вики, противоречить пока нечему.

## Questions raised

- [[questions/why-cant-cms-use-ode-solvers]]
- [[questions/how-is-mean-flow-time-derivative-computed]]
- [[questions/why-does-consistency-training-work-without-teacher]]

## Notes

- Последний слайд — русскоязычный мем («Айтишники всё!»), юмористическая концовка, не технический контент. Не ингестировался.
- В слайдах упоминается более длинный reading list: «Stable Consistency Tuning», «Consistency Models Made Easy», «One-step Diffusion via Shortcut Models», «Mean Flows for One-step Generative Modeling», «Inductive Moment Matching» и «Align Your Flow». Добавлены в reading queue на [[topics/few-step-generative-models]].

## Pointer back to raw

`raw/lectures/flow-map-models.pdf`
