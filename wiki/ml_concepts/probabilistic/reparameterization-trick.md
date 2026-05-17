---
title: Reparameterization Trick
type: ml_concept
tags: [variational-inference, vae, gradient-estimation, stochastic-computation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
needs_rewrite: true
---

# Reparameterization Trick

> Переписать сэмпл $z \sim q(z \mid x, \phi)$ как детерминированное преобразование $z = g_\phi(x, \varepsilon)$ шума $\varepsilon \sim p(\varepsilon)$ из фиксированного распределения. Параметры $\phi$ теперь живут внутри $g_\phi$, а не внутри распределения сэмплирования, поэтому $\nabla_\phi \mathbb{E}_q[f(z)]$ превращается в низкодисперсный pathwise-градиент.

## Motivation

Чтобы обучать [[ml_concepts/amortized-variational-inference]], нужен градиент

$$
\nabla_\phi\,\mathbb{E}_{z \sim q(z \mid x, \phi)}\big[f(z)\big],
$$

где $f(z) = \log p(x \mid z, \theta)$ — reconstruction-член в [[ml_concepts/elbo|ELBO]]. Препятствие структурное: распределение, из которого мы сэмплируем, зависит от параметров, по которым берётся производная. Ожидание и градиент нельзя свободно поменять местами, потому что изменение $\phi$ меняет *какие $z$ сэмплируются*, а не только значение $f$ на них.

Наивный подход — сэмплировать $z \sim q(z \mid x, \phi)$, считать $\nabla_\phi f(z)$ и называть это оценкой градиента — просто неверен. Полученный $z$ зависит от $\phi$ через sampler, а это недифференцируемая операция. Backprop через `sample()` не определён.

Существует общая несмещённая оценка, работающая для любого $q$ — **score-function (REINFORCE) estimator**:

$$
\nabla_\phi\,\mathbb{E}_{q(z \mid x, \phi)}[f(z)] \;=\; \mathbb{E}_{q}\!\big[f(z) \cdot \nabla_\phi \log q(z \mid x, \phi)\big].
$$

Она корректна, но трактует $f(z)$ как чёрный ящик — скалярный множитель на зашумлённом score, игнорируя структуру $f$. Дисперсия достаточно велика, чтобы обучение непрерывных латентов шло медленно или нестабильно.

Reparameterization trick устраняет причину проблемы, а не обходит её. Переписать $z$ как детерминированное преобразование *фиксированного* шума: $z = g_\phi(x, \varepsilon)$ с $\varepsilon \sim p(\varepsilon)$, не зависящего от $\phi$. Теперь распределение, из которого сэмплируем, от $\phi$ не зависит; зависит только детерминированная функция $g_\phi$. Градиенты становятся обычным правилом цепочки через $g_\phi$, весь граф дифференцируем end-to-end, а один сэмпл $\varepsilon$ даёт низкодисперсный pathwise-градиент, передающий информацию через $f$, а не усредняющий её. Поэтому [[methods/vae|VAE]] используют его как default, а score-function оставляют для случаев, когда reparameterization недоступен (дискретные латенты, смеси).

## Formal description

Пусть $z \sim q(z \mid x, \phi)$ допускает представление $z = g_\phi(x, \varepsilon)$ с $\varepsilon \sim p(\varepsilon)$, не зависящим от $\phi$. По law of the unconscious statistician (LOTUS),

$$
\mathbb{E}_{z \sim q(z \mid x, \phi)}\big[f(z)\big] \;=\; \mathbb{E}_{\varepsilon \sim p(\varepsilon)}\big[f(g_\phi(x, \varepsilon))\big].
$$

В правой части нет меры, зависящей от параметров, поэтому при стандартных условиях регулярности:

$$
\nabla_\phi\,\mathbb{E}_{z \sim q}[f(z)] \;=\; \mathbb{E}_{\varepsilon \sim p(\varepsilon)}\!\big[\nabla_\phi f(g_\phi(x, \varepsilon))\big].
$$

По правилу цепочки на подынтегральном выражении:

$$
\nabla_\phi f(g_\phi(x, \varepsilon)) \;=\; \big(\nabla_z f(z)\big)\big|_{z = g_\phi(x, \varepsilon)} \cdot \nabla_\phi g_\phi(x, \varepsilon).
$$

Monte Carlo c $L$ сэмплами (часто $L = 1$ на пример):

$$
\nabla_\phi\,\mathbb{E}_{z \sim q}[f(z)] \;\approx\; \frac{1}{L}\sum_{l=1}^L \nabla_\phi f(g_\phi(x, \varepsilon^{(l)})), \qquad \varepsilon^{(l)} \sim p(\varepsilon).
$$

## Canonical instance: diagonal Gaussian

Для диагонально-гауссовского posterior $q(z \mid x, \phi) = \mathcal{N}(\mu_\phi(x), \mathrm{diag}(\sigma_\phi^2(x)))$ берём $p(\varepsilon) = \mathcal{N}(0, I)$ и

$$
z \;=\; g_\phi(x, \varepsilon) \;=\; \mu_\phi(x) + \sigma_\phi(x) \odot \varepsilon.
$$

Энкодер выдаёт $\mu_\phi$ и $\sigma_\phi$ (или $\log \sigma_\phi$); обе величины — дифференцируемые функции $\phi$. Случайность идёт через $\varepsilon$ и в градиент не вносит вклада.

Для более общих распределений есть альтернативы: location-scale семейства легко репараметризуются; для смесей и дискретных распределений нужны другие инструменты (Gumbel-softmax, straight-through estimators и т.п.).

## Contrast with the score-function estimator

Общее тождество для дифференцирования ожидания по параметризованной мере — **score-function (REINFORCE) estimator**:

$$
\nabla_\phi\,\mathbb{E}_{q(z \mid x, \phi)}[f(z)] \;=\; \mathbb{E}_{q}\!\big[f(z) \cdot \nabla_\phi \log q(z \mid x, \phi)\big].
$$

Она несмещённая для *любого* $q$, включая дискретные, но трактует $f(z)$ как скалярный множитель на зашумлённом score. Дисперсия обычно много выше, чем у reparameterization, потому что reparameterization прокидывает градиентную информацию через структуру $f$ по правилу цепочки, а не через скалярный коэффициент.

В VAE по умолчанию reparameterization; score-function оставляют для дискретных латентов или распределений, где reparameterization невозможен.

## Variations and related concepts

- [[ml_concepts/elbo]] — потеря, для которой нужен этот трюк в $\phi$-градиенте.
- [[ml_concepts/amortized-variational-inference]] — постановка, где $\phi$ — веса энкодера.
- [[methods/vae]] — каноническое использование reparameterization.
- [[ml_concepts/variational-inference]] — фреймворк вокруг всего этого.

## Open questions

- {нет}

## Sources

- [[sources/elbo-and-vae-lecture]] — вывод через LOTUS и контраст со score-function оценкой.

## Up next

- [[methods/vae]] — каноническая модель, в которой reparameterization trick позволяет обучать энкодер, декодер и ELBO одним SGD.
