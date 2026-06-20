---
Created: 2026-01-29T10:37
Reviewed: Done
---
## Пререквизиты

Рассмотрим генеративную задачу, а именно генерацию изображений. Поставим цель — напрямую смоделировать плотность распределения данных $\pi(x)$ с помощью нейронной сети. Таким образом, мы аппроксимируем истинную плотность $\pi(x)$ параметрической моделью $p(x|\theta)$, где $\theta$ — параметры сети.

Ключевая проблема заключается в том, что выход нейронной сети, как правило, не гарантирует выполнения условия нормировки. Чтобы $p(x|\theta)$ являлась корректной функцией плотности вероятности, она должна удовлетворять следующему свойству:

$$\int p(x|\theta) dx = 1$$

Для решения этой проблемы вводится ненормированная модель $\hat{p}(x|\theta)$, которую часто называют энергетической функцией, представляющая собой непосредственный выход нейронной сети. Корректная плотность $p(x|\theta)$ тогда определяется через явную нормировку:

$$p(x|\theta) = \frac{\hat{p}(x|\theta)}{\int \hat{p}(x|\theta)dx}$$

Здорово, конечно, но абсолютно непонятно, как брать интеграл по всем возможным выходам нейронной сети — это аналитически и вычислительно неразрешимая задача.

## Score-функция

Для того чтобы обойти вычисление интеграла, рассмотрим логарифм плотности:

$$\log p(\mathbf{x}|\theta) = \log \hat{p}(\mathbf{x}|\theta) - \log \int \hat{p}(\mathbf{x}|\theta)dx$$

Теперь заметим, что если мы возьмем градиент $\nabla_\mathbf{x}$ по левой и правой частям, то чудесным образом нам удастся избавиться от интеграла. Так как интеграл взят по всему пространству $\mathbf{x}$, результат от $\mathbf{x}$ уже не зависит, и градиент по нему будет равен нулю:

$$\nabla_\mathbf{x} \log p(\mathbf{x}|\theta) = \nabla_\mathbf{x} \log \hat{p}(\mathbf{x}|\theta) - \nabla_\mathbf{x} \log \int \hat{p}(\mathbf{x}|\theta)d\mathbf{x} = \nabla_\mathbf{x} \log \hat{p}(\mathbf{x}|\theta)$$

Круто! Мы получили важный результат: градиент логарифма истинной нормированной плотности (левая часть) равен градиенту логарифма ненормированного выхода нейронной сети (правая часть). Эта величина $\nabla_\mathbf{x} \log p(\mathbf{x}|\theta)$ имеет собственное название — score-функция, её также можно обозначать как $s(\mathbf{x} \mid \theta)$.

Теперь вместо того чтобы моделировать саму плотность $p(\mathbf{x}|\theta)$, мы перешли к моделированию её градиента по $\mathbf{x}$. Геометрически score-функция — это векторное поле, которое в каждой точке $\mathbf{x}$ (т.е. для каждого изображения) указывает направление наискорейшего роста плотности вероятности. То есть показывает, как нам нужно сдвинуть значения пикселей в нашей картинке, чтобы семпл был более похож на наиболее вероятный семпл из распределения, которое мы пытаемся аппроксимировать.

![[images/energy-based-models/image.png]]

Постановка задачи: есть конкретные точки в пространстве и необходимо обучить score-функцию

## Задача оптимизации

Для того чтобы обучить score-функцию, можно воспользоваться дивергенцией Фишера:

$$\frac{1}{2} \, \mathbb{E}_{\mathbf{x} \sim \pi(\mathbf{x})} \left[ \left\| \nabla_{\mathbf{x}} \log p(\mathbf{x} \mid \theta) - \nabla_{\mathbf{x}} \log \pi(\mathbf{x}) \right\|_2^2 \right] \rightarrow \min_{\theta}$$

Интуитивно, минимизация этого функционала означает, что мы подбираем параметры $\theta$ так, чтобы градиенты логарифмов двух плотностей совпадали во всех точках пространства. Если градиенты двух функций совпадают всюду, то сами функции тоже отличаются лишь на константу.

Однако есть пара проблем. Во-первых, мы не знаем истинный score $\nabla_{\mathbf{x}} \log \pi(\mathbf{x})$ и поэтому непонятно, как минимизировать этот функционал напрямую. Во-вторых, на данный момент непонятно, как генерировать новые сэмплы, даже если мы будем знать истинный score или хотя бы его аппроксимацию.

## Denoising Objective

Начнём с решения первой проблемы. Мы действительно не знаем истинную score-функцию $\nabla_{\mathbf{x}} \log \pi(\mathbf{x})$. Другими словами, у нас нет таргета, а значит, мы не можем напрямую вычислить дивергенцию Фишера и минимизировать её. Однако для нас был проложен обходной путь, позволяющий разрешить эту проблему. Давайте по нему и проследуем.

Возьмем наши данные $\mathbf{x} \sim \pi(\mathbf{x})$, которые были получены из оригинального распределения, и подмешаем в них немного гауссовского шума:

$$\mathbf{x}_\sigma = \mathbf{x} + \sigma \cdot \boldsymbol{\epsilon}, \quad \boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

В таком случае, условное распределение зашумлённого сэмпла при известном $\mathbf{x}$ будет иметь следующий вид:

$$q(\mathbf{x}_\sigma \mid \mathbf{x}) = \mathcal{N}(\mathbf{x}, \sigma^2 \mathbf{I})$$

С этим распределением все понятно, это просто нормально распределение со средним равным оригинальному семплу и дисперсией, которая контролируется параметром $\sigma$. Далее получим безусловное распределение зашумленных данных $q(\mathbf{x}_\sigma)$, проинтегрировав условное распределение по всем возможным $\mathbf{x}$:

$$q(\mathbf{x}_\sigma) = \int q(\mathbf{x}_\sigma \mid \mathbf{x}) \, \pi(\mathbf{x}) \, d\mathbf{x}$$

Для этого зашумлённого распределения мы так же можем записать дивергенцию Фишера, как делали это для распределения чистых данных:

$$\frac{1}{2} \, \mathbb{E}_{\mathbf{x}_\sigma \sim q(\mathbf{x}_\sigma)} \left[ \left\| \nabla_{\mathbf{x}_\sigma} \log p(\mathbf{x}_\sigma \mid \theta) - \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma) \right\|_2^2 \right] \rightarrow \min_{\theta}$$

И тут мы можем сделать осторожное предположение, что при _достаточно малых_ значениях шума $\sigma$ score-функция зашумлённых данных будет приближать score-функцию исходных данных:

$$\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma) \approx \nabla_{\mathbf{x}} \log \pi(\mathbf{x}) \quad \text{при } \sigma \to 0$$

На первый взгляд кажется, что мы ничего не выиграли: score зашумлённого распределения $\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma)$ вычислить напрямую так же невозможно, как и $\nabla_{\mathbf{x}} \log \pi(\mathbf{x})$. Ведь $q(\mathbf{x}_\sigma)$ — это интеграл по всем возможным $\mathbf{x}$, который мы не умеем брать аналитически. Однако именно здесь и появляется ключевой трюк, известный как **Denoising Score Matching**. Оказывается, что при достаточно мягких условиях регулярности справедливо следующее равенство:

$$
\mathbb{E}_{\mathbf{x}_\sigma \sim q(\mathbf{x}_\sigma)}
\left\|
\nabla_{\mathbf{x}_\sigma} \log p(\mathbf{x}_\sigma \mid \theta, \sigma)
-
\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma)
\right\|_2^2
=
\mathbb{E}_{\mathbf{x} \sim \pi(\mathbf{x})} \mathbb{E}_{\mathbf{x}_\sigma \sim {q(\mathbf{x}_\sigma | \mathbf{x})}}
\left\|
\nabla_{\mathbf{x}_\sigma} \log p(\mathbf{x}_\sigma \mid \theta, \sigma)
-
\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x})
\right\|_2^2 + \text{const}(\theta)
$$

Ключевой выигрыш этого равенства в том, что оно заменяет неизвестное на известное: вместо $\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma)$, который мы не можем вычислить, появляется $\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x})$ — score условного распределения, заданного нами явно. Не хочу, чтобы этот переход казался нам некой магией, поэтому давайте для начала разберемся, как он оказался возможным, а потом уже до конца осознаем, что это нам дает.

## Доказательство

Сначала докажем, что мы можем перейти от $\mathbb{E}_{\mathbf{x}_\sigma \sim q(\mathbf{x}_\sigma)}$ к $\mathbb{E}_{\mathbf{x} \sim \pi(\mathbf{x})} \mathbb{E}_{\mathbf{x}_\sigma \sim q(\mathbf{x}_\sigma | \mathbf{x})}$. Пусть

$$h(\mathbf{x}_\sigma) = \left\| \nabla_{\mathbf{x}_\sigma} \log p(\mathbf{x}_\sigma \mid \theta, \sigma) - \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma) \right\|_2^2$$

Тогда наше исходное выражение примет следующий вид:

$$\mathbb{E}_{\mathbf{x}_\sigma \sim q(\mathbf{x}_\sigma)} h(\mathbf{x}_\sigma)$$

По определению математического ожидания:

$$\mathbb{E}_{q(\mathbf{x}_\sigma)} h(\mathbf{x}_\sigma) = \int q(\mathbf{x}_\sigma) \, h(\mathbf{x}_\sigma) \, d\mathbf{x}_\sigma$$

Мы знаем, что маргинальное распределение $q(\mathbf{x}_\sigma)$ получается интегрированием совместного распределения по $\mathbf{x}$:

$$q(\mathbf{x}_\sigma) = \int \pi(\mathbf{x}) \, q(\mathbf{x}_\sigma | \mathbf{x}) \, d\mathbf{x}$$

Подставим это в наше выражение:

$$\mathbb{E}_{q(\mathbf{x}_\sigma)} h(\mathbf{x}_\sigma) = \int \left[ \int \pi(\mathbf{x}) \, q(\mathbf{x}_\sigma | \mathbf{x}) \, d\mathbf{x} \right] h(\mathbf{x}_\sigma) \, d\mathbf{x}_\sigma$$

Получился двойной интеграл. По теореме Фубини, если подынтегральная функция абсолютно интегрируема, мы можем поменять порядок интегрирования:

$$\iint \pi(\mathbf{x}) \, q(\mathbf{x}_\sigma | \mathbf{x}) \, h(\mathbf{x}_\sigma) \, d\mathbf{x}_\sigma \, d\mathbf{x}$$

Перегруппируем: сначала интегрируем по $\mathbf{x}_\sigma$ при фиксированном $\mathbf{x}$, затем по $\mathbf{x}$:

$$\int \pi(\mathbf{x}) \left[ \int q(\mathbf{x}_\sigma | \mathbf{x}) \, h(\mathbf{x}_\sigma) \, d\mathbf{x}_\sigma \right] d\mathbf{x}$$

Внутренний интеграл — это $\mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} h(\mathbf{x}_\sigma)$, внешний — $\mathbb{E}_{\pi(\mathbf{x})}$. Итого:

$$\mathbb{E}_{q(\mathbf{x}_\sigma)} h(\mathbf{x}_\sigma) = \mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} h(\mathbf{x}_\sigma)$$

Замечательно, первый шаг выполнен. Теперь сосредоточим свое внимание на функции $h(\mathbf{x}_\sigma)$ и докажем, что мы можем перейти от использования $\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma)$ в качестве таргета к $\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x})$. Для краткости обозначим $\nabla_{\mathbf{x}_\sigma} \log p(\mathbf{x}_\sigma \mid \theta, \sigma)$ как $\mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma)$. И раскроем квадрат l2-нормы:

$$
\begin{aligned}
\mathbb{E}_{q(\mathbf{x}_\sigma)}h(\mathbf{x}_\sigma) &= \mathbb{E}_{q(\mathbf{x}_\sigma)}
\| \mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma) - \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma) \|^2
=\\
&= \mathbb{E}_{q(\mathbf{x}_\sigma)}\left[\| \mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma) \|^2 - 2 \langle \mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma), \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma) \rangle + \|\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma)\|^2
\right]
\end{aligned}
$$

Последний член не зависит от параметров $\theta$, поэтому при оптимизации его можно отбросить. Первый член уже имеет нужный нам вид. Разберёмся со вторым членом — скалярным произведением.

Покажем, что:

$$\mathbb{E}_{q(\mathbf{x}_\sigma)} \langle \mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma), \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma) \rangle = \mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} \langle \mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma), \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x}) \rangle$$

Раскроем левую часть по определению математического ожидания и воспользуемся тождеством $\nabla \log f = \frac{\nabla f}{f}$:

$$
\mathbb{E}_{q(\mathbf{x}_\sigma)} \langle \mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma), \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma) \rangle = \int \cancel{q(\mathbf{x}_\sigma)} \left[ \mathbf{s}_{\theta,\sigma}^T(\mathbf{x}_\sigma)
\frac
{\nabla_{\mathbf{x}_\sigma}q(\mathbf{x}_\sigma)}
{\cancel{q(\mathbf{x}_\sigma)}} \right] d\mathbf{x}_\sigma
$$

Сокращаем $q(\mathbf{x}_\sigma)$ и подставляем $q(\mathbf{x}_\sigma) = \int q(\mathbf{x}_\sigma | \mathbf{x}) \pi(\mathbf{x}) d\mathbf{x}$:

$$= \int \left[ \mathbf{s}_{\theta,\sigma}^T(\mathbf{x}_\sigma) \nabla_{\mathbf{x}_\sigma} \left( \int q(\mathbf{x}_\sigma | \mathbf{x}) \pi(\mathbf{x}) d\mathbf{x} \right) \right] d\mathbf{x}_\sigma$$

Градиент по $\mathbf{x}_\sigma$ не действует на $\pi(\mathbf{x})$, поэтому вносим его под интеграл. $\mathbf{s}_{\theta,\sigma}^T(\mathbf{x}_\sigma)$ константа по $d\mathbf{x}$ и может быть внесена под знак интеграла. Затем по теореме Фубини меняем порядок интегрирования:

$$= \iint \pi(\mathbf{x}) \,\mathbf{s}_{\theta,\sigma}^T(\mathbf{x}_\sigma) \textcolor{blue}{\nabla_{\mathbf{x}_\sigma} q(\mathbf{x}_\sigma | \mathbf{x})} d\mathbf{x}_\sigma d\mathbf{x}$$

Применяем тождество $\textcolor{blue}{\nabla f = f \cdot \nabla \log f}$ в обратную сторону:

$$= \iint \pi(\mathbf{x})\, \textcolor{blue}{q(\mathbf{x}_\sigma | \mathbf{x})} \left[ \mathbf{s}_{\theta,\sigma}^T(\mathbf{x}_\sigma) \textcolor{blue}{\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x})} \right] d\mathbf{x}_\sigma d\mathbf{x}$$

Записываем как двойное математическое ожидание:

$$= \mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} \langle \mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma), \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x}) \rangle$$

Таким образом, мы показали, что средний член в разложении $h(\mathbf{x}_\sigma)$ можно переписать, заменив score маргинального распределения на score условного. Если собрать все вместе, то получим

$$\mathbb{E}_{q(\mathbf{x}_\sigma)} h(\mathbf{x}_\sigma) = \mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} \| \mathbf{s}_{\theta,\sigma} \|^2 - 2 \mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} \langle \mathbf{s}_{\theta,\sigma}, \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x}) \rangle + \text{const}(\theta)$$

Выносим $\mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})}$ за скобку:

$$= \mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} \left[ \| \mathbf{s}_{\theta,\sigma} \|^2 - 2 \langle \mathbf{s}_{\theta,\sigma}, \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x}) \rangle \right] + \text{const}(\theta)$$

Теперь трюк: добавим и вычтем $\mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})}\|\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x})\|^2$:

$$= \mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} \left[ \| \mathbf{s}_{\theta,\sigma} \|^2 - 2 \langle \mathbf{s}_{\theta,\sigma}, \nabla \log q(\mathbf{x}_\sigma | \mathbf{x}) \rangle + \|\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x})\|^2 \right] + \text{const}'(\theta)$$

где $\text{const}'(\theta) = \text{const}(\theta) - \mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} \|\nabla \log q(\mathbf{x}_\sigma | \mathbf{x})\|^2$ - по-прежнему не зависит от $\theta$.

Выражение в скобках — это в точности квадрат нормы разности:

$$= \mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} \| \mathbf{s}_{\theta,\sigma} - \nabla \log q(\mathbf{x}_\sigma | \mathbf{x}) \|^2 + \text{const}'(\theta)$$

Что и требовалось доказать.

## Итоговый лосс для оптимизации

Давайте соберём воедино всё, что мы доказали, и посмотрим, как преобразовался наш исходный функционал.

**Исходная задача.** Мы начинали с дивергенции Фишера, которая требует знания истинной score-функции:

$$\mathbb{E}_{\mathbf{x} \sim {\pi(\mathbf{x})}} \| \mathbf{s}_\theta(\mathbf{x}) - \nabla_{\mathbf{x}} \log \pi(\mathbf{x}) \|_2^2 \rightarrow \min_\theta$$

**Переход к зашумлённым данным.** Так как $\nabla_{\mathbf{x}} \log \pi(\mathbf{x})$ нам неизвестен, мы добавили гауссовский шум к данным и перешли к оптимизации на зашумлённом распределении:

$$\mathbb{E}_{\mathbf{x}_\sigma \sim {q(\mathbf{x}_\sigma)}} \| \mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma) - \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma) \|_2^2 \rightarrow \min_\theta$$

Но $\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma)$ тоже нельзя вычислить напрямую — маргинальное распределение $q(\mathbf{x}_\sigma)$ задано интегралом, который не берётся аналитически.

**Denoising Score Matching.** Нам удалось доказать, что этот функционал эквивалентен (с точностью до константы, не зависящей от $\theta$) следующему:

$$\mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{q(\mathbf{x}_\sigma | \mathbf{x})} \| \mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma) - \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x}) \|_2^2 \rightarrow \min_\theta$$

Теперь вместо score-функции маргинала появилась score-функция условного распределения $q(\mathbf{x}_\sigma | \mathbf{x})$, которое мы сами задали.

$$q(\mathbf{x}_\sigma | \mathbf{x}) = \mathcal{N}(\mathbf{x}, \sigma^2 \mathbf{I})$$

Логарифм нормального распределения будет равен следующему выражению:

$$\log q(\mathbf{x}_\sigma | \mathbf{x}) = -\frac{\|\mathbf{x}_\sigma - \mathbf{x}\|^2}{2\sigma^2} + \text{const}$$

А если мы возьмем градиент по $\mathbf{x}_\sigma$ от него, то:

$$\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x}) = -\frac{\mathbf{x}_\sigma - \mathbf{x}}{\sigma^2}$$

Вспомним, что $\mathbf{x}_\sigma = \mathbf{x} + \sigma \cdot \boldsymbol{\epsilon}$, где $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$. Тогда:

$$
\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma | \mathbf{x}) =
-\frac{(\mathbf{x} + \sigma \cdot \boldsymbol{\epsilon}) - \mathbf{x}}{\sigma^2}
=
-\frac{\sigma \cdot \boldsymbol{\epsilon}}{\sigma^2} = -\frac{\boldsymbol{\epsilon}}{\sigma}
$$

**Финальный лосс.** Подставляем найденный таргет и переписываем математическое ожидание по $q(\mathbf{x}_\sigma | \mathbf{x})$ как ожидание по $\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$:

$$\mathbb{E}_{\pi(\mathbf{x})} \mathbb{E}_{\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left\| \mathbf{s}_{\theta,\sigma}(\mathbf{x} + \sigma \cdot \boldsymbol{\epsilon}) + \frac{\boldsymbol{\epsilon}}{\sigma} \right\|_2^2 \rightarrow \min_\theta$$

Это и есть **Denoising Score Matching objective**. Обратите внимание:

- Таргет $-\boldsymbol{\epsilon}/\sigma$ известен аналитически — мы сами сэмплируем шум $\boldsymbol{\epsilon}$

- Не нужно знать ни $\nabla_{\mathbf{x}} \log \pi(\mathbf{x})$, ни $\nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma)$

- Достаточно уметь сэмплировать из данных $\mathbf{x} \sim \pi(\mathbf{x})$ и генерировать гауссовский шум

Интуитивно, мы учим нейросеть $\mathbf{s}_{\theta,\sigma}$ предсказывать направление к чистым данным по зашумлённому сэмплу — то есть **убирать шум**.

## Сэмплирование: динамика Ланжевена

Мы научились обучать score-функцию $\mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma) \approx \nabla_{\mathbf{x}_\sigma} \log q(\mathbf{x}_\sigma)$. Осталось понять, как использовать ее для генерации новых семплов из распределения $\pi(x)$. Первое, что приходит на ум, — это старый добрый градиентный ~~спуск~~ подъём: делаем шаги в направлении score, пока не достигнем области максимальной плотности.

К сожалению, такой алгоритм приведет к mode collapse: вместо разнообразных сэмплов из $\pi(\mathbf{x})$ мы раз за разом будем получать плюс-минус одну и ту же точку вблизи моды распределения. Чтобы сэмплировать из распределения, а не просто находить его максимум, к градиентному шагу добавляют случайный шум. Такая модификация алгоритма градиентного подъема называется динамикой Ланжевена.  

![[images/energy-based-models/image 1.png]]

Динамика Ланжевена — это итеративный процесс. Инициализируем $\mathbf{x}_0$ из нормального распределения $\mathcal{N}(\mathbf{0}, \mathbf{I})$, а далее повторяем $T$ раз:

$$\mathbf{x}_{t+1} = \mathbf{x}_t + \frac{\eta}{2} \nabla_{\mathbf{x}} \log p(\mathbf{x}_t) + \sqrt{\eta} \cdot \boldsymbol{\epsilon}_t, \quad \boldsymbol{\epsilon}_t \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$$

где $\eta > 0$ — размер шага. Разберём, что здесь происходит:

- $\frac{\eta}{2} \nabla_{\mathbf{x}} \log p(\mathbf{x}_t)$ — детерминированный дрейф к областям высокой плотности (aka градиентный подъём);

- $\sqrt{\eta} \cdot \boldsymbol{\epsilon}_t$ — случайный шум, который не даёт застрять в локальном максимуме и обеспечивает правильное распределение

Таким образом, дрейф тянет к модам, а шум позволяет исследовать всё распределение, не застревая в локальных модах. Более того, можно показать, что при $\eta \to 0$ и $t \to \infty$ распределение $\mathbf{x}_t$ сходится к $\pi(\mathbf{x})$. На практике $\eta$ и число шагов конечны, поэтому сэмплы получаются приближённые, но и этого зачастую достаточно.

Однако важно помнить, что мы не знаем истинный score $\nabla_{\mathbf{x}} \log p(\mathbf{x})$, у нас есть только его аппроксимация — обученная нейросеть $\mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma)$. В самом начале повествования мы показали, что

$$\mathbf{s}_{\theta,\sigma}(\mathbf{x}_\sigma) \approx \nabla_{\mathbf{x}} \log \pi(\mathbf{x}) \quad \text{при } \sigma \to 0$$

Отсюда следует проблема: score-функция, обученная с малым $\sigma$, хорошо определена только в областях высокой плотности данных. Она практически не видела сильно зашумлённых сэмплов, с которых мы начинаем генерацию ($\mathbf{x}_0 \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$). Следовательно, может потребоваться очень много итераций, чтобы случайным блужданием добраться до тех областей, где $\mathbf{s}_{\theta,\sigma}(\mathbf{x})$ начнёт выдавать осмысленные значения.

![[images/energy-based-models/image 2.png]]

## Noised Conditioned Score Network

Для решения описанной выше проблемы было предложено использовать _annealed_ динамику Ланжевена. В рамках модифицированного алгоритма мы обучаем score-функцию не для одного, а сразу для нескольких уровней шума $\sigma_1 < \sigma_2 < \ldots < \sigma_L$.

![[images/energy-based-models/image 3.png]]

$$\mathcal{L}(\theta) = \sum_{i=1}^{L} \sigma_i^2 \cdot \mathbb{E}_{p(\mathbf{x})} \mathbb{E}_{\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})} \left\| \mathbf{s}_{\theta,\sigma_i}(\mathbf{x} + \sigma_i \boldsymbol{\epsilon}) + \frac{\boldsymbol{\epsilon}}{\sigma_i} \right\|_2^2$$

В теории, мы должны посчитать лосс по всем возможным уровням шума, которые будем использовать в рамках семплирования. При подсчете лосса важно добавить весовой коэффициент $\sigma_i^2$, так как target имеет норму порядка $\frac{1}{\sigma_i}$, поэтому без коррекции лоссы для малых $\sigma$ доминировали бы, и сеть игнорировала бы крупномасштабную структуру. Множитель $\sigma_i^2$ компенсирует этот эффект: $\sigma_i^2 \cdot \left\|\frac{\boldsymbol{\epsilon}}{\sigma_i}\right\|^2 = \|\boldsymbol{\epsilon}\|^2$, и все уровни шума вносят сопоставимый вклад.

На практике на каждом шаге обучения мы сэмплируем уровень шума $i \sim \mathrm{Uniform}\{1, \ldots, L\}$ и считаем лосс только для него — это стандартный приём стохастической оптимизации.

Далее, при семплировании начинаем с большого шума $\sigma_L$, формируя грубую структуру и лёгко переходя между модами данных. Далее, постепенно уменьшаем шум до $\sigma_1$, уточняя мелкие детали.