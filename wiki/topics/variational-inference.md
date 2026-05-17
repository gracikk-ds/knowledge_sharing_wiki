---
title: Variational Inference
type: topic
tags: [variational-inference, latent-variable-models, generative-models, elbo, vae]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Variational Inference

> Семейство генеративных моделей, которое обучает latent-variable модель, аппроксимируя её труднообъемный posterior трактуемым распределением и максимизируя [[ml_concepts/elbo|ELBO]] вместо истинного log-likelihood.

## The setting

Latent-variable генеративные модели предполагают, что каждый data point $x$ порождается из ненаблюдаемого $z$: рисуем $z \sim p(z)$ из простого prior, затем $x \sim p(x \mid z, \theta)$ из conditional. Истинная цель — maximum likelihood — требует маргинал $p(x \mid \theta) = \int p(x \mid z, \theta) p(z) dz$, проинтегрированный по всем возможным latent'ам.

В общем случае этот интеграл нерасчётен. Закрытой формы нет ни для одной достаточно содержательной модели, а наивный Монте-Карло — семплируем $z \sim p(z)$ и усредняем conditional — ломается. Для конкретного $x$ те latent'ы, что могут его правдоподобно объяснить, занимают тонкую область prior, и почти каждый prior-сэмпл приземляется вне неё. Подынтегральное выражение для этих сэмплов почти ноль; в оценке доминирует шум, и градиент бесполезен для обучения.

Variational inference атакует это одним ходом: ввести второе распределение $q(z)$, чья масса сидит там, где подынтегральное выражение велико, и ограничить $\log p(x \mid \theta)$ величиной, которую можно оценить по $q$-сэмплам. Эта граница — ELBO. Остальная область — дизайн вокруг этого хода: какой формы $q$, как его подогнать, как через него протолкнуть градиент.

## Core ideas

Стартовая точка — сам [[ml_concepts/latent-variable-model]]: генеративная история, в которой $x$ наблюдается, $z$ нет, и эти двое связаны prior $p(z)$ и conditional $p(x \mid z, \theta)$. Маргинальный интеграл — то место, где всё ломается. Всё ниже — обходные пути.

Центральная идея фреймворка — [[ml_concepts/variational-inference]]: аппроксимировать истинный posterior $p(z \mid x, \theta)$ ближайшим в каком-то трактуемом семействе $q$ под reverse KL. Направление «reverse», потому что ожидание берётся по $q$ — тому, из чего реально можно сэмплировать. Reverse KL mode-seeking: он кладёт массу $q$ на самые высокие пики posterior и игнорирует low-mass области, со всеми последствиями, описанными на странице.

Отсюда выпадает [[ml_concepts/elbo]]: трактуемая нижняя граница $\log p(x \mid \theta)$, оцениваемая по $q$-сэмплам. Зазор границы в точности равен $\mathrm{KL}(q \,\|\, p(z \mid x))$, поэтому максимизация границы по $q$ и $\theta$ заодно толкает $q$ к истинному posterior. Под этим лежат две математические опоры: [[math_concepts/jensens-inequality]] задаёт направление границы, а [[math_concepts/kl-divergence]] измеряет и зазор, и регуляризационный член, появляющийся в loss на практике.

Две идеи превращают фреймворк в обучаемую систему. [[ml_concepts/amortized-variational-inference]] заменяет per-example $q$ единой нейросетью $q(z \mid x, \phi)$, общей на все $x$ — дешевле на inference, чуть хуже на каждом примере. [[ml_concepts/reparameterization-trick]] переписывает сэмпл $z \sim q(z \mid x, \phi)$ как детерминированное преобразование $z = g_\phi(x, \varepsilon)$ фиксированного шума $\varepsilon$, чтобы градиент $\nabla_\phi \mathbb{E}_q[\cdot]$ стал ожиданием по $\varepsilon$, и через шаг сэмплирования можно было прогнать backprop.

## Methods that grow from these ideas

[[methods/variational-em]] — учебниковый способ. Чередовать E-step, обновляющий $q$ при фиксированном $\theta$, с M-step, обновляющим $\theta$ при фиксированном $q$. Этот метод старше deep learning на десятилетия и работает всегда, когда $q$ имеет трактуемую форму и E-step разрешается в закрытой форме. Он полезен, чтобы понять, что ELBO *пытается* делать на каждом шаге, но плохо масштабируется на высокоразмерные модели, где точный E-step сам неразрешим.

Современный метод — [[methods/vae]]. Энкодер (амортизованный $q$) и декодер ($p(x \mid z, \theta)$) — обе нейросети. KL-член превращается в закрытую формулу Gaussian-vs-Gaussian; reconstruction-член — Monte Carlo оценка по одному reparameterized сэмплу; градиент проходит через оба члена в одном вычислительном графе. Отказ от EM-чередования — при фиксированном $\theta$ точный E-step всё равно неразрешим, так как $q$ сам нейросеть — и делает VAE сквозно обучаемым.

## Open threads

- **Amortization gap.** Количественно, насколько общий энкодер недотягивает до per-example оптимума? Упоминается на [[ml_concepts/amortized-variational-inference]], но не разбирается.
- **Posterior collapse.** Условия, при которых $q(z \mid x, \phi) \to p(z)$ и latent code становится неинформативным; способы митигации.
- **Score-function оценка.** Используется при дискретных latent'ах и не-reparameterizable случаях; кратко упомянута на [[ml_concepts/reparameterization-trick]].
- **Более тугие границы.** Importance-weighted ELBO (IWAE); $\beta$-VAE и теоретико-информационные цели.

## Reading order (recap)

1. [[ml_concepts/latent-variable-model]]
2. [[ml_concepts/variational-inference]]
3. [[ml_concepts/elbo]] — с обращением к [[math_concepts/jensens-inequality]] и [[math_concepts/kl-divergence]] по мере необходимости
4. [[methods/variational-em]]
5. [[ml_concepts/amortized-variational-inference]]
6. [[ml_concepts/reparameterization-trick]]
7. [[methods/vae]]

## Reading queue

- Kingma & Welling, «Auto-Encoding Variational Bayes» (2014) — оригинальная статья VAE.
- Rezende, Mohamed, Wierstra, «Stochastic Backpropagation and Approximate Inference in Deep Generative Models» (2014) — параллельная статья про reparameterization trick.
- Burda, Grosse, Salakhutdinov, «Importance Weighted Autoencoders» (IWAE, 2016) — более тугая граница.
- Higgins et al., «$\beta$-VAE» (2017) — disentanglement через перевзвешенный KL.
- Kingma & Welling, «An Introduction to Variational Autoencoders» (Foundations and Trends, 2019) — длинный обзор.
