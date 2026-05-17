---
title: Consistency Training (CT)
type: method
tags: [consistency-models, generative-models, few-step-generation, training-free-teacher]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
needs_rewrite: true
---

# Consistency Training (CT)

> Обучить [[ml_concepts/consistency-function]] с нуля — без diffusion-учителя — используя прямой reference-путь $x_t = x_0 + t\,\epsilon$ и переиспользуя *одинаковый* $\epsilon$ для обоих концов пары на траектории.

## Motivation

[[methods/consistency-distillation]] требует предобученной [[ml_concepts/diffusion-model]], чтобы строить согласованные пары на траекториях $(x_t, \hat{x}_{t-\Delta})$. Это тяжёлая предпосылка: нужно полностью оплатить обучение multi-step учителя, прежде чем приступать к обучению one-step student'а. Вопрос — можно ли обойтись без учителя и всё равно обучить [[ml_concepts/consistency-function]], сохраняющую инвариантность вдоль траектории.

Препятствие — само построение пары. Чтобы обеспечить $f_\theta(x_t, t) = f_\theta(x_s, s)$, нужны две точки на *одной* ODE-траектории. Только учитель знал, какой $x_s$ соответствует данному $x_t$, потому что траектория сворачивает по data manifold сложным образом, зависящим от обученной [[ml_concepts/score-function]]. Сэмплируем свежий $\epsilon$ для каждого момента — и две точки оказываются на *разных* траекториях; ограничение инвариантности превращается в шум.

CT выходит из положения, меняя сам ODE, который consistency function должна отслеживать. Если приблизить score conditional score'ом в одной data-точке, [[ml_concepts/probability-flow-ode]] схлопывается в прямую $x_t = x_0 + t \epsilon$, и спаривание становится тривиальным: берём один $\epsilon$, считаем прямую в двух моментах — пара готова. Student теперь учит consistency function *спрямлённой* траектории, что заодно и есть то, что нужно one-step сэмплерам — прямой ODE как раз тот, что один шаг Эйлера решает без ошибки. Два forward pass'а на шаг обучения, ни учителя, ни вызова солвера. Цена — нижележащий ODE уже не настоящий diffusion ODE; CT наследует любой bias, привнесённый приближением прямого пути.

## Problem setting

Нет предобученной diffusion-модели, либо не хочется платить за её обучение. Consistency function всё равно нужна.

## The trick

Consistency distillation требует пар $(x_n, x_{n-1})$ на *одной* ODE-траектории. Без учителя — откуда их брать?

CT опирается на одно простое наблюдение. Если нижележащий score-based ODE —

$$
\mathrm{d}x \;=\; -\,t\,\nabla_x \log p_t(x)\,\mathrm{d}t,
$$

и заменить score conditional score'ом в одном сэмпле,

$$
\nabla_x \log p_t(x) \;\approx\; -\,\frac{1}{t^2}\,(x - x_0),
$$

ODE превращается в **прямую**

$$
\mathrm{d}x \;=\; \frac{1}{t}(x - x_0)\,\mathrm{d}t,
$$

с закрытым решением $x_t = x_0 + t\,\epsilon$, $\epsilon \sim \mathcal{N}(0, I)$. Тогда пара $(x_n, x_{n-1})$ лежит на одной *спрямлённой* траектории тогда и только тогда, когда она построена из **одного и того же $\epsilon$** в двух моментах $t_n$, $t_{n-1}$.

## Algorithm

Дискретизируем время: $t_0 < t_1 < \ldots < t_N$. Один шаг обучения:

1. Сэмплируем $x_0 \sim p_{\text{data}}$, $n \sim \mathcal{U}\{1, \ldots, N\}$, $\epsilon \sim \mathcal{N}(0, I)$.
2. Строим пару из **одного $\epsilon$**:
   $$x_n \;=\; x_0 + t_n\,\epsilon,\qquad x_{n-1} \;=\; x_0 + t_{n-1}\,\epsilon.$$
3. Применяем student'а к обеим точкам и минимизируем:
   $$\mathcal{L}_{\text{CT}}(\theta) \;=\; \mathbb{E}\big\lVert f_\theta(x_{n-1}, t_{n-1}) - f_\theta(x_n, t_n) \big\rVert_2^2.$$
4. Обеспечиваем границу $f_\theta(x_0, t_0) = x_0$ через skip-connection параметризацию.

Всё обучение сводится к двум forward pass'ам на шаг (плюс ветвь EMA-target сети на практике).

## Why it works

CT не приближает *настоящую* diffusion-траекторию — он приближает её **спрямлённую** версию. Лекция говорит это явно: «Consistency Training forces the trajectories to be straight.» Оптимальный $f_\theta$ под CT — это consistency function flow-matching-стиля прямого ODE, который, кстати, тоже является корректной генеративной моделью, когда распределение $\epsilon$ совпадает с распределением шума, используемого на inference.

Иначе говоря, CT обучает flow-map для **rectified-flow** ODE, а не для diffusion ODE. По этой же причине его сэмплы могут получаться чёткими за один шаг: лежащий под ним ODE по построению прямой.

## Properties

- **Число шагов на inference:** 1 шаг (greedy) или 4–5 стохастических, как и у CD.
- **Учитель нужен:** нет.
- **Стоимость обучения:** два forward pass'а на шаг; никаких дополнительных вызовов солвера.
- **Caveat:** приближение прямого пути точно только в пределе бесконечного процесса спрямления (rectified flow). На конечных данных оптимальный flow map не буквально diffusion flow map — но лекция аргументирует, что это фича, а не баг, потому что прямые траектории — именно то, что нужно one-step сэмплерам.

## Variants and successors

- «Consistency Models Made Easy» (2024) — variance reduction.
- «Consistency Flow Matching» (2024) — явный straight-flow target.
- [[methods/consistency-distillation]] — teacher-based аналог.

## Sources

- [[sources/flow-map-models-lecture]] — вывод трюка с прямым путём из score-based ODE и сам loss.

## Up next

- [[methods/consistency-distillation]] — teacher-based аналог; сравнение двух методов проясняет, что именно покупал учитель.
- [[topics/few-step-generative-models]] — более широкий ландшафт one-step сэмплеров; CT стоит рядом с shortcut models и mean flow.
