---
title: 2D Rotation Matrix
type: math_concept
tags: [linear-algebra, geometry, rotations, orthogonal-matrices]
created: 2026-05-17
updated: 2026-05-17
sources: 1
status: draft
---

# 2D Rotation Matrix

> Линейное преобразование $R(\theta) \in \mathbb{R}^{2 \times 2}$, поворачивающее любой 2D-вектор на угол $\theta$ относительно начала координат, не меняя его длины. В матричной форме $R(\theta) = \begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}$.

## Plain-English statement

Вектор $X = (x_1, x_2)^\top$ на плоскости можно представить как точку с длиной $|X|$ и углом $\varphi$ к оси $x_1$. Координаты — это проекции: $x_1 = |X|\cos\varphi$, $x_2 = |X|\sin\varphi$. Повернуть вектор на угол $\theta$ против часовой стрелки означает прибавить $\theta$ к $\varphi$: длина не меняется, угол становится $\varphi + \theta$. Возникает вопрос — как выразить новые координаты $(x_1', x_2')$ как линейную функцию старых $(x_1, x_2)$, не зная при этом ни $|X|$, ни $\varphi$ явно.

Ответ — матрица $R(\theta)$. Её строки совпадают с теми коэффициентами, которые дают формулы синус-косинуса от суммы углов. Преобразование линейное, так что одна и та же матрица действует на любой вектор, и это превращает геометрический поворот в обычное матричное умножение.

Для RoPE и других применений важны три структурных свойства: длина сохраняется (матрица ортогональна), повороты складываются по углам (композиция), и обратный поворот — это поворот в обратную сторону, равный транспонированию.

## Step-by-step: вывод формулы

Запишем повёрнутый вектор $X'$ через его новый угол $\varphi + \theta$:

$$x_1' = |X|\cos(\varphi + \theta), \qquad x_2' = |X|\sin(\varphi + \theta).$$

Раскроем синус и косинус суммы:

$$
\begin{aligned}
\cos(\varphi + \theta) &= \cos\varphi\cos\theta - \sin\varphi\sin\theta, \\
\sin(\varphi + \theta) &= \sin\varphi\cos\theta + \cos\varphi\sin\theta.
\end{aligned}
$$

Подставим $\cos\varphi = x_1 / |X|$, $\sin\varphi = x_2 / |X|$ — оба следуют из определения старых координат. После сокращения $|X|$:

$$
\begin{aligned}
x_1' &= x_1\cos\theta - x_2\sin\theta, \\
x_2' &= x_1\sin\theta + x_2\cos\theta.
\end{aligned}
$$

Это и есть линейная функция старых координат. Перепишем матрично:

$$
\begin{bmatrix} x_1' \\ x_2' \end{bmatrix} = \underbrace{\begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}}_{R(\theta)} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}.
$$

![[raw/lectures/RoPE/images/image 2.png]]
*Координаты $(x_1, x_2)$ как проекции вектора длины $1$ под углом $\varphi$ — отправная точка вывода.*

## Свойства

**Ортогональность и обратное преобразование.** Прямая проверка: $R(\theta)^\top R(\theta) = I$, поэтому $R(\theta)^{-1} = R(\theta)^\top$. Транспонирование даёт

$$
R(\theta)^\top = \begin{bmatrix}\cos\theta & \sin\theta \\ -\sin\theta & \cos\theta\end{bmatrix} = \begin{bmatrix}\cos(-\theta) & -\sin(-\theta) \\ \sin(-\theta) & \cos(-\theta)\end{bmatrix} = R(-\theta),
$$

где использовали $\cos(-\theta) = \cos\theta$ и $\sin(-\theta) = -\sin\theta$. Геометрически: транспонирование — поворот на тот же угол в обратную сторону.

**Композиция: углы складываются.** Прямое перемножение блочно даёт

$$
R(\alpha)\,R(\beta) = \begin{bmatrix}\cos(\alpha+\beta) & -\sin(\alpha+\beta) \\ \sin(\alpha+\beta) & \cos(\alpha+\beta)\end{bmatrix} = R(\alpha + \beta),
$$

потому что внутренние произведения раскрываются через те же формулы суммы синус-косинуса, что и при выводе самой матрицы.

**Сохранение нормы.** Поскольку $R(\theta)^\top R(\theta) = I$,

$$
\lVert R(\theta) x \rVert^2 = x^\top R(\theta)^\top R(\theta)\, x = x^\top x = \lVert x \rVert^2.
$$

**Сохранение скалярных произведений.** Тот же расчёт даёт $(R(\theta) x)^\top (R(\theta) y) = x^\top y$ для любых $x, y$ — поворот не меняет ни длин, ни углов между векторами.

## Worked example

Возьмём $\theta = \pi/2$ (90° против часовой стрелки). Тогда $\cos\theta = 0$, $\sin\theta = 1$, и

$$
R(\pi/2) = \begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}.
$$

Применим к $x = (1, 0)^\top$ (вектор по оси $x_1$):

$$
R(\pi/2) \begin{bmatrix}1 \\ 0\end{bmatrix} = \begin{bmatrix}0 \\ 1\end{bmatrix}.
$$

Ось $x_1$ переходит в ось $x_2$ — то, чего ждём от поворота на 90°. Норма сохранилась: $\lVert x \rVert = \lVert R(\pi/2) x \rVert = 1$.

Проверим композицию: $R(\pi/2)\,R(\pi/2)$ должно равняться $R(\pi)$. Прямое умножение:

$$
\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}\begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix} = \begin{bmatrix}-1 & 0 \\ 0 & -1\end{bmatrix} = R(\pi),
$$

— разворот на 180°. Углы сложились, как и обещано.

Проверим транспонирование как обратное: $R(\pi/2)^\top = \begin{bmatrix}0 & 1 \\ -1 & 0\end{bmatrix} = R(-\pi/2)$, что возвращает $(0, 1)^\top$ обратно в $(1, 0)^\top$ — тоже работает.

## Where it shows up in ML

- [[ml_concepts/attention/positional-encodings/rotary-position-embedding]] — RoPE поворачивает $q_m$ и $k_n$ на углы, пропорциональные позиции; свойства композиции и транспонирования и обеспечивают переход $m\theta, n\theta \to (n-m)\theta$ в скалярном произведении.
- [[methods/positional/rope]] — блочно-диагональная матрица из $d/2$ независимых 2D-поворотов; норма $q$ и $k$ сохраняется per-пара и значит per-вектор.

## Common pitfalls

- **Знак $\sin\theta$ в недиагональных позициях.** Для поворота против часовой стрелки $R(\theta)$ имеет $-\sin\theta$ в правом верхнем углу. Перепутать знак — поворот пойдёт по часовой стрелке.
- **Левосторонняя vs правосторонняя система координат.** Формула выше работает в стандартной правосторонней системе с осью $x_2$ направленной вверх. В системах с инвертированной осью (например, экранные координаты с $y$ вниз) то, что выглядит «против часовой», на самом деле «по часовой».
- **Композиция в 2D vs в высших размерностях.** В 2D повороты коммутируют ($R(\alpha)R(\beta) = R(\beta)R(\alpha)$), потому что складываются только углы. В 3D и выше повороты вокруг разных осей в общем случае не коммутируют — это уже не работает.
- **Радианы vs градусы.** Все формулы выше — в радианах. $\sin(90)$ в Python даёт не то, что ждёт человек, который имел в виду градусы.

## Sources

- [[sources/rope-lecture]] — вывод матрицы поворота через проекции и угловое сложение приводится как разогрев перед RoPE.
