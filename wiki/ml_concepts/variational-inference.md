---
title: Variational Inference
type: ml_concept
tags: [variational-inference, latent-variable-models, generative-models, probabilistic-modelling]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Variational Inference

> Фреймворк для аппроксимации труднообъемного posterior $p(z \mid x, \theta)$ более простым распределением $q(z)$ из трактуемого семейства; качество приближения измеряется $\mathrm{KL}(q \,\|\, p(z \mid x, \theta))$.

## Motivation

В [[ml_concepts/latent-variable-model]] нам постоянно нужен posterior $p(z \mid x, \theta)$ — для предсказаний, для ожиданий, возникающих в целях обучения, для анализа того, чему модель научилась. Правило Байеса его выписывает:

$$
p(z \mid x, \theta) \;=\; \frac{p(x \mid z, \theta)\,p(z)}{p(x \mid \theta)}.
$$

В знаменателе — маргинальное правдоподобие, тот самый интеграл, который мы посчитать не можем. То есть posterior известен с точностью до неизвестной нормализующей константы. Один путь — подставлять MCMC-сэмплы, но это медленно, плохо смешивается в высокой размерности и плохо амортизируется по многим примерам.

Variational inference заменяет inference на оптимизацию. Берём трактуемое семейство $\mathcal{Q} = \{q\}$ — диагональные гауссианы, mean-field факторизации, более сложные параметрические семейства — и ищем внутри него $q$, ближайший к истинному posterior, по [[math_concepts/kl-divergence]]. Найденный $q^*$ используется как прокси: ожидания под истинным posterior заменяются ожиданиями под $q^*$, и эти последние мы посчитать можем, потому что $q^*$ взят из трактуемого семейства.

Прямая попытка минимизировать $\mathrm{KL}(q \,\|\, p(z \mid x, \theta))$ упирается в ту же стену, что и раньше: KL содержит $\log p(z \mid x, \theta)$, а это та же неизвестная нормировка. Выход — тождество $\log p(x \mid \theta) = \mathrm{ELBO}(q, \theta) + \mathrm{KL}(q \,\|\, p(z \mid x, \theta))$. Левая часть от $q$ не зависит, поэтому минимизировать KL по $q$ — это в точности то же, что максимизировать [[ml_concepts/elbo|ELBO]] по $q$. ELBO нуждается только в joint $p(x, z \mid \theta) = p(x \mid z, \theta)\,p(z)$, который у нас есть. Это и есть базовый ход VI: трудный объект и трактуемый суррогат различаются на константу по $q$, поэтому оптимизация суррогата эквивалентна оптимизации настоящей величины.

Остаётся выбор дизайна — семейство $\mathcal{Q}$. Богаче семейство — ближе к истинному posterior, но сложнее в оптимизации и выше дисперсия градиентных оценок. Mean-field $q(z) = \prod_j q_j(z_j)$ — классический default; диагональные гауссианы доминируют в amortized-постановках. Этот компромисс — bias от $\mathcal{Q}$ против стоимости оптимизации — главная ручка, которую крутит VI-практик.

## Formal description

Для фиксированных $x$ и $\theta$ VI решает

$$
q^* \;=\; \arg\min_{q \in \mathcal{Q}}\,\mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta)\big).
$$

KL напрямую нерасчётен (содержит $\log p(z \mid x, \theta)$), но можно обойти это через тождество

$$
\log p(x \mid \theta) \;=\; \mathrm{ELBO}(q, \theta) \;+\; \mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta)\big).
$$

Левая часть от $q$ не зависит. Поэтому при фиксированном $\theta$:

$$
\arg\min_{q} \mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta)\big) \;\equiv\; \arg\max_{q} \mathrm{ELBO}(q, \theta).
$$

Истинный posterior для подгонки $q$ не нужен — максимизация [[ml_concepts/elbo|ELBO]] по $q$ — та же оптимизация, что минимизация KL к posterior. Это базовое тождество VI.

## Why reverse KL (not forward)

VI минимизирует $\mathrm{KL}(q \,\|\, p)$, а не $\mathrm{KL}(p \,\|\, q)$. Асимметрия играет роль:

- $\mathrm{KL}(q \,\|\, p)$ «mode-seeking»: $q$ платит большой штраф за массу там, где $p$ почти ноль, но не наоборот. Оптимизатор склонен подгонять $q$ к одной моде многомодального posterior.
- $\mathrm{KL}(p \,\|\, q)$ «mass-covering»: $q$ должен покрыть весь носитель $p$, иначе оценка взрывается. Считать тяжело — ожидание под $p$.

Reverse KL выбран потому, что $q$ — это proposal, из которого мы сэмплируем; ожидания под $q$ трактуемы. Детали асимметрии — на [[math_concepts/kl-divergence]].

## Choosing the family

Классический выбор — **mean-field** семейство: $q(z) = \prod_j q_j(z_j)$, каждый множитель в простом параметрическом семействе. Полностью факторизованное, легко сэмплируется, но не выражает корреляций между латентами.

Для amortized-постановок (одна inference-сеть на все $x$) типичный выбор — **диагональный гауссиан** $q(z \mid x, \phi) = \mathcal{N}(\mu_\phi(x), \mathrm{diag}(\sigma_\phi^2(x)))$ с $\mu_\phi, \sigma_\phi$ как выходами нейросети. Это и есть выбор [[methods/vae]]. Более богатые семейства существуют (normalising flows для $q$, structured posteriors) ценой дополнительной сложности.

## Variations and related concepts

- [[ml_concepts/elbo]] — суррогат, оптимизируемый вместо нерасчётного KL.
- [[ml_concepts/amortized-variational-inference]] — общая $q(z \mid x, \phi)$ на все примеры.
- [[ml_concepts/reparameterization-trick]] — backprop через $\nabla_\phi \mathbb{E}_{q}[\cdot]$.
- [[methods/variational-em]] — чередовать VI ($q$-обновления) с обновлениями модели.
- [[methods/vae]] — VI, end-to-end параметризованная как глубокий автоэнкодер.
- [[math_concepts/kl-divergence]] — мера «близости», которую минимизируем.

## Open questions

- {нет}

## Sources

- [[sources/elbo-and-vae-lecture]] — вывод того, что минимизация KL к posterior — та же задача, что максимизация ELBO, плюс EM-путь оптимизации.

## Up next

- [[ml_concepts/elbo]] — суррогатная цель, превращающая нерасчётную KL-минимизацию в трактуемую задачу максимизации.
- [[ml_concepts/amortized-variational-inference]] — общая нейросеть на все $x$ вместо per-example подгонки $q$.
