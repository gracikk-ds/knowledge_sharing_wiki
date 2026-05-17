---
title: Few-step Generative Models
type: topic
tags: [generative-models, diffusion, flow-matching, distillation, sampling]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Few-step Generative Models

> Методы, превращающие медленный multi-step ODE-генератор (diffusion, flow matching) в модель, выдающую сэмплы за 1–4 forward pass'а — либо distillation многошагового учителя, либо прямое обучение проинтегрированному решению генеративного ODE.

## The setting

Diffusion-модель генерирует, интегрируя детерминированный ODE назад во времени. Обученное поле скоростей (или score) указывает, как двигать шум к данным; ODE-солвер делает шаги. Траектория между шумом и данными изгибается в многомерном пространстве, поэтому один шаг Эйлера от $t = \sigma$ к $t = 0$ приземляется далеко от data manifold. На практике нужны десятки и сотни шагов, чтобы держать ошибку интегрирования малой. Каждый шаг — это полный forward pass через сеть. Сгенерировать одно изображение стоит как 50–100 запусков модели.

Few-step генеративные модели от этой цены отказываются. Они сохраняют diffusion-обученный фундамент — корректное распределение сэмплов, покрытие мод, устойчивое обучение, — но прижимают inference к нескольким вызовам сети. В дизайне доминируют две семьи. Либо приставить student'а к уже обученному multi-step учителю и заставить student'а воспроизвести его выход за меньшее число шагов, либо перепараметризовать обученный объект так, чтобы один forward pass уже представлял длинное интегрирование. Обе идеи проступают в методах ниже, часто в одной модели сразу.

## Core ideas

Фундамент — [[ml_concepts/generative/probability-flow-ode]]. У diffusion это детерминированный двойник noising SDE; у flow matching это ODE, переносящий prior в data вдоль обученного векторного поля. Сэмплирование = решение этого ODE, и стоимость сэмплирования = число шагов солвера.

[[ml_concepts/generative/flow-map]] — смена точки зрения, из которой вырастает остальная область. Вместо *мгновенной* скорости $v(x_t, t)$ — производной траектории в одной точке — выучить *проинтегрированное* решение $\Psi_{t \to s}(x_t)$ напрямую: функцию, которая берёт состояние в момент $t$ и возвращает состояние в момент $s$. Если у тебя есть $\Psi_{0 \leftarrow \sigma}$ на всём интервале, сэмплирование — один вызов сети. Вся few-step область — про то, как обучить flow map достаточно точно, чтобы обойтись без ODE-солвера.

Самая простая цель для flow-map — приземляться в данные. [[ml_concepts/generative/consistency-function]] — это flow map $\Psi_{0 \leftarrow t}$, определённый для каждого $t$, с одним ограничением: точки на одной траектории probability-flow должны переходить в один и тот же data-сэмпл. Именно это свойство и делает consistency models обучаемыми без явного учителя и даёт семье название.

[[ml_concepts/generative/step-distillation]] — более ранний фрейминг, из которого область выросла. Обучить быстрого student'а имитировать *выход* медленного multi-step учителя, рассматривая multi-step траекторию учителя как supervision-сигнал. Это работает независимо от того, есть ли у student'а flow-map структура. Методы ниже смешивают эти две идеи — flow-map параметризацию и step distillation — в разных пропорциях.

## Methods that grow from these ideas

[[methods/distillation/progressive-distillation]] первым продвинул few-step сэмплирование на масштабе. Обучить student'а воспроизводить два шага учителя за один, затем повторить distillation на новом student'е, пока не дойдём до одного шага. Каждый раунд делит число шагов пополам. Student — это перепараметризованный учитель — без flow-map структуры, без consistency-ограничения — поэтому ошибка копится с каждым урезанием шагов, и качество изображений резко падает в самом конце расписания.

[[methods/distillation/consistency-distillation]] — flow-map аналог. Обучить consistency function, требуя, чтобы соседние точки на сгенерированной учителем траектории отображались в один выход: student видит $x_t$ из одного шага учителя и $x_{t - \Delta t}$ из следующего, и loss заставляет оба давать одинаковое предсказание. Учитель даёт ground-truth траектории; consistency-ограничение даёт структурное свойство. Один forward pass из любого $t$ в $0$ даёт сэмпл.

[[methods/distillation/consistency-training]] полностью убирает учителя. Берём два момента $t < s$, рисуем *одинаковый* гауссовский шум $\varepsilon$, строим две зашумлённые версии $x_t = x_0 + t\varepsilon$ и $x_s = x_0 + s\varepsilon$ — обе лежат на одной прямой траектории между $x_0$ и шумовой границей — и накладываем на эти две точки consistency-ограничение. Ни учителя, ни предобученной diffusion-сети. Трюк в том, что одинаковая $\varepsilon$ гарантирует, что обе точки лежат на одной траектории в прямом transport'е.

[[methods/distillation/multistep-consistency-model]] — естественное ослабление, когда одна consistency function недостаточно точна на всём $[0, \sigma]$. Разбить интервал на $K$ под-интервалов, выучить отдельный flow map на каждый, и сэмплировать цепочкой из $K$ forward pass'ов — обычно $K = 2$ или $K = 4$. Это закрывает разрыв в качестве между one-step CMs и многошаговым diffusion: за точность платят forward pass'ами, а не раундами distillation.

[[methods/generative/shortcut-model]] обобщает «все flow map приземляются в ноль». Выучить $F(x_t, t, s)$ для произвольных $t, s$ и наложить interval-additivity: переход $t \to s$ должен совпадать с $t \to u \to s$ для любого промежуточного $u$. Это self-consistency loss, который вместе со stop-gradient на одной стороне равенства даёт одной сети целое семейство $\Psi_{t \to s}$ без учителя.

[[methods/generative/mean-flow]] переосмысливает тот же flow map как *среднюю скорость* на $[t, s]$. Средняя скорость — естественная для обучения величина, но на вид неинтегрируемая: чтобы её усреднить, нужна та самая траектория, от которой мы пытаемся избавиться. [[math_concepts/mean-flow-identity]] выражает среднюю скорость через один вызов мгновенной скорости плюс производную $F$ по времени, делая цель обучения локальной. Модель учится удовлетворять тождеству в каждой тройке $(x_t, t, s)$.

## Open threads

- [[questions/why-cant-cms-use-ode-solvers]] — почему consistency models не работают со стандартными ODE-солверами.
- [[questions/how-is-mean-flow-time-derivative-computed]] — как $\mathrm{d}F/\mathrm{d}t$ вдоль траектории считается в коде (JVP через autograd).
- [[questions/why-does-consistency-training-work-without-teacher]] — почему трюк «одинаковый $\varepsilon$ → прямой путь» закрывает consistency-ограничение.

## Reading order (recap)

1. [[ml_concepts/generative/probability-flow-ode]]
2. [[ml_concepts/generative/flow-map]]
3. [[ml_concepts/generative/consistency-function]]
4. [[ml_concepts/generative/step-distillation]]
5. [[methods/distillation/progressive-distillation]]
6. [[methods/distillation/consistency-distillation]]
7. [[methods/distillation/consistency-training]]
8. [[methods/distillation/multistep-consistency-model]]
9. [[methods/generative/shortcut-model]]
10. [[math_concepts/mean-flow-identity]] → [[methods/generative/mean-flow]]

## Reading queue

- Song et al., «Consistency Models» (2023) — оригинальная статья CMs.
- Heek et al., «Multistep Consistency Models» (2024).
- Frans et al., «One-step Diffusion via Shortcut Models» (2024).
- Geng et al., «Mean Flows for One-step Generative Modeling» (2025).
- Sabour et al., «Align Your Flow: Scaling Continuous-Time Flow-Map Distillation» (2025).

## Sources

- [[sources/flow-map-models-lecture]] — лекция с объединяющим flow-map взглядом на CMs, ShortCut и Mean Flow.
