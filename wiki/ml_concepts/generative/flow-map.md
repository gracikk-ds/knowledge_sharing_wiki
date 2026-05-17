---
title: Flow Map
type: ml_concept
tags: [generative-models, diffusion, flow-matching, sampling, distillation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
needs_rewrite: true
---

# Flow Map

> Flow map — это обученное *проинтегрированное решение* генеративного ODE: функция $\Psi_{t \to s}(x_t)$, которая по точке в момент $t$ возвращает точку, в которую траектория приходит к моменту $s$ — без солвера на inference.

## Motivation

Стандартный diffusion и [[ml_concepts/flow-matching]] обучают векторное поле $v(x, t)$ — мгновенную скорость генеративного ODE. Сэмплирование — это интегрирование $\mathrm{d}x = v(x, t)\,\mathrm{d}t$ от шума к данным. Траектория искривлена, поэтому точный солвер требует много мелких шагов; каждый шаг — полный forward pass через сеть. 50–200 вычислений на сэмпл — стандартная цена.

Первая попытка уменьшить цену — взять более крупный шаг, но кривизна пути ограничивает, насколько далеко можно уйти одним Эйлеровским шагом, не сбившись с траектории. Лучшие солверы (Heun, DPM-Solver) помогают, но всё равно требуют десятков вычислений, потому что они по сути перестраивают кривую из локальных кусков. Бутылочное горлышко не в солвере — в *представлении*. Векторное поле говорит мгновенное направление, но никогда — пункт назначения.

Flow map меняет то, что сеть выдаёт. Вместо скорости в $(x, t)$ — выучить проинтегрированный endpoint $\Psi_{t \to s}(x_t)$, то есть где траектория окажется в будущий момент $s$. Один forward pass теперь делает работу полного ODE rollout от $t$ до $s$. Сэмплирование за 1–4 шага вместо 50–200 у vector-field аналога.

Цена этого — обучение. Векторное поле в $(x, t)$ — локальная величина; её можно прочитать с инфинитезимальных данных. Flow map в $(x, t, s)$ — *результат* интегрирования того же поля, поэтому сеть должна сжать целое семейство интегралов — по одному на каждую пару $(t, s)$ — в свои веса. Интересно, как методы это супервизируют, не разворачивая ODE на каждом градиентном шаге: distillation от учителя, структурные self-consistency тождества как у [[ml_concepts/consistency-function|consistency models]], или граничный якорь при $s = t$. Различия методов в этой семье — именно в выборе supervision.

## Formal description

Пусть генеративный процесс — это ODE

$$
\frac{\mathrm{d}x}{\mathrm{d}u} = v(x, u),\qquad u \in [0, \sigma].
$$

Его solution operator (flow):

$$
\Psi_{t \to s}(x_t) \;=\; x_t + \int_t^s v(x_u, u)\,\mathrm{d}u .
$$

**Flow map** — это нейросеть $F_\theta(x_t, t, s)$, обученная так, чтобы

$$
\Psi_{t \to s}(x_t) \;\approx\; x_t + (s - t)\,F_\theta(x_t, t, s),
$$

то есть $F_\theta$ представляет *среднюю скорость* на $[t, s]$. Эквивалентно сеть можно параметризовать так, чтобы выдавать сразу destination: $G_\theta(x_t, t, s) \approx \Psi_{t \to s}(x_t)$. Две параметризации взаимозаменяемы.

На inference берём грубое расписание $t_N > t_{N-1} > \ldots > t_0$, инициализируем $x_N \sim \mathcal{N}(0, \sigma^2 I)$ и итерируем

$$
x_{n-1} \;=\; x_n + (t_{n-1} - t_n)\,F_\theta(x_n, t_n, t_{n-1}).
$$

При $N = 1$ модель прыгает из чистого шума в сэмпл за один forward pass.

[[ml_concepts/consistency-function]] — частный случай, когда целевое время фиксировано как $t = 0$: $f_\theta(x_t, t) = \Psi_{t \to 0}(x_t)$.

## Why it can be learnt

Flow map корректно определён, потому что генеративный ODE **детерминирован**: каждая $(x_t, t)$ лежит ровно на одной траектории, поэтому $\Psi_{t \to s}(x_t)$ — функция. Три способа его супервизии:

1. **Distillation from a teacher** — гонит ODE-солвер учителя из $(x_t, t)$ в $s$, регрессирует student'а к этому endpoint'у. Используется в [[methods/progressive-distillation]] и [[methods/consistency-distillation]].
2. **Self-consistency** — эксплуатирует структурное тождество, выполняемое истинным flow. У consistency models это $f(x_t, t) = f(x_{t - \Delta}, t - \Delta)$ вдоль траектории; у shortcut models — interval additivity $F(x_t, t, s) = F(F(x_t, t, r), r, s)$; у Mean Flow — [[math_concepts/mean-flow-identity]].
3. **Boundary anchoring** — при $s = t$ flow map вырождается в тождественное отображение (или в мгновенную скорость, в зависимости от параметризации). Фиксация этой границы не даёт схлопнуться к вырожденному решению вроде $F \equiv 0$.

Большинство методов комбинируют (1) или (2) с (3).

## Flow map vs vector field

| Property                  | Vector field $v(x, t)$         | Flow map $F(x, t, s)$ |
|---------------------------|--------------------------------|-----------------------|
| Что выдаёт                | Мгновенную скорость            | Проинтегрированное перемещение |
| Нужен солвер на inference?| Да — много шагов               | Нет — один forward pass на шаг |
| Domain                    | $(x, t)$                       | $(x, t, s)$ — лишний time-аргумент |
| Сложная часть обучения    | Many-to-one цель регрессии     | Сжатие семейства интегралов |
| Композируется с солверами?| Да — градиентное поле          | Нет — уже преинтегрирован |

Последняя строка — практический подвох: имея flow map, нельзя подключить его к Heun, DPM-Solver и т.п., потому что нет производной для интегрирования. Сэмплирование делается фиксированными расписаниями $\tau_0 < \tau_1 < \ldots < \tau_K$ с прямыми вызовами $F_\theta(x_{\tau_k}, \tau_k, \tau_{k+1})$.

## Variations and related concepts

- [[ml_concepts/consistency-function]] — flow map с target $s = 0$.
- [[ml_concepts/step-distillation]] — супервизирует flow map через учителя.
- [[methods/shortcut-model]] — flow-map метод через interval additivity.
- [[methods/mean-flow]] — flow-map метод через тождество средней скорости.
- [[methods/multistep-consistency-model]] — flow map, ограниченный на интервалы.
- [[ml_concepts/flow-matching]] — vector-field аналог, который flow-map методы пытаются «преинтегрировать».

## Open questions

- [[questions/why-cant-cms-use-ode-solvers]]
- [[questions/how-is-mean-flow-time-derivative-computed]]

## Sources

- [[sources/flow-map-models-lecture]] — вводит термин «flow map» как объединяющий взгляд на CMs, ShortCut и Mean Flow.

## Up next

- [[ml_concepts/consistency-function]] — самый изученный flow map, у которого целевое время фиксировано как $s = 0$.
- [[methods/shortcut-model]] — flow map, обученный через тождество interval additivity $F(x_t, t, s) = F(F(x_t, t, r), r, s)$.
