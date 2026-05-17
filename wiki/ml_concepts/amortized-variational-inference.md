---
title: Amortized Variational Inference
type: ml_concept
tags: [variational-inference, latent-variable-models, vae, neural-networks]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Amortized Variational Inference

> Заменить per-example вариационное распределение $q(z)$ единой сетью $q(z \mid x, \phi)$, отображающей любой $x$ в параметры его variational posterior. Одна модель, один набор параметров $\phi$ — на все примеры.

## Motivation

Хотим обучить [[ml_concepts/latent-variable-model]], максимизируя [[ml_concepts/elbo|ELBO]] одновременно по параметрам генеративной модели $\theta$ и по приближённому posterior $q(z)$. Классический [[ml_concepts/variational-inference]] работает с $q$ напрямую: на каждое наблюдение $x$ — свой $q_x(z)$, обучаемый с нуля. Это корректно, но не масштабируется. Каждый новый $x$ запускает свежую оптимизацию, и хранение per-example вариационных параметров растёт линейно с размером датасета. На тесте всё ещё хуже: предвычисленного $q$ нет, и оптимизировать нужно заново.

Обходной путь — перестать решать по одной задаче inference на $x$ и вместо этого выучить одну inference-*функцию*, решающую их все. Берём одну сеть $q(z \mid x, \phi)$ с общими параметрами $\phi$, где вход — $x$, а выход — параметры вариационного распределения (обычно среднее и дисперсия диагонального гауссиана). Inference на любом $x$, виденном или нет, схлопывается в один forward pass. Per-example $q$ заменён функцией $\phi$, которая отображает $x$ в $q(z \mid x)$.

Этот обмен не бесплатен. Функция конечной ёмкости не может для каждого $x$ дотянуть до оптимума, доступного per-example $q$. Этот недобор называется **amortization gap** и отделён от **variational gap**, вызванного выбором семейства распределений. Энкодер решает усреднённую задачу по data-распределению, а не настроенную задачу под пример, и это усреднение — цена ускорения. На практике зазор мал относительно сэкономленных вычислений, поэтому amortized inference — стандарт в [[methods/vae|VAE]] и родственных глубоких latent-variable моделях.

## Formal description

Берём семейство, параметризованное выходами нейросети. Для диагонально-гауссовского posterior энкодер выдаёт $(\mu_\phi(x), \sigma_\phi(x))$ и

$$
q(z \mid x, \phi) \;=\; \mathcal{N}\!\big(\mu_\phi(x),\,\mathrm{diag}(\sigma_\phi^2(x))\big).
$$

Обучение максимизирует [[ml_concepts/elbo|ELBO]] совместно по параметрам энкодера $\phi$ и параметрам генеративной модели $\theta$:

$$
\max_{\theta, \phi}\;\mathbb{E}_{x \sim \pi}\!\big[\mathrm{ELBO}(\phi, \theta; x)\big] \;=\; \max_{\theta, \phi}\;\mathbb{E}_{x \sim \pi}\!\Big[\mathbb{E}_{z \sim q(z \mid x, \phi)}\big[\log p(x \mid z, \theta)\big] - \mathrm{KL}\!\big(q(z \mid x, \phi) \,\|\, p(z)\big)\Big].
$$

Backprop через $\mathbb{E}_{q}[\cdot]$ использует [[ml_concepts/reparameterization-trick]]. KL-член для гауссовского $q$ и гауссовского $p(z)$ берётся в закрытой форме, поэтому Monte Carlo на него не нужен.

## Why this is "amortization"

Термин из бухгалтерии: вместо того чтобы платить за свежую оптимизацию на каждый пример, платим один раз во время обучения, чтобы выучить $\phi$, а потом амортизируем эту стоимость по всем будущим примерам. В заметках лекции это называют **amortised inference network** или просто **encoder** (в контексте VAE).

## Two failure modes

- **Amortization gap.** Даже при оптимальном $\phi$ распределение $q(z \mid x, \phi)$ для конкретного $x$ может быть худшим приближением к истинному posterior, чем подобранный per-example $q$. Энкодер решает среднюю задачу, не задачу для одного примера.
- **Posterior collapse.** Если декодер $p(x \mid z, \theta)$ слишком выразителен (например, сильный авторегрессивный декодер), $q(z \mid x, \phi)$ схлопывается к prior $p(z)$ — KL-член обнуляется, $z$ не несёт информации об $x$, и latent code становится бесполезным. Стандартные митигации: ослабить декодер, использовать KL annealing, добавить информационные бутылочные горлышки.

## Variations and related concepts

- [[ml_concepts/variational-inference]] — родительский фреймворк.
- [[ml_concepts/elbo]] — цель обучения.
- [[ml_concepts/reparameterization-trick]] — нужен для backprop через $\nabla_\phi$.
- [[methods/vae]] — каноническая amortized VI модель.

## Open questions

- {нет}

## Sources

- [[sources/elbo-and-vae-lecture]] — мотивирует энкодер как способ заменить per-example $q$ общей сетью, отображающей $x$ в параметры posterior.

## Up next

- [[ml_concepts/reparameterization-trick]] — как считать $\nabla_\phi \mathbb{E}_{q(z \mid x, \phi)}[\cdot]$, тот самый градиент, который вводит amortization.
- [[methods/vae]] — каноническая модель, объединяющая amortized inference и генеративный декодер в одном end-to-end графе.
