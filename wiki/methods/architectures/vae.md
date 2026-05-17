---
title: Variational Autoencoder (VAE)
type: method
tags: [variational-inference, generative-models, latent-variable-models, vae, neural-networks]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
needs_rewrite: true
---

# Variational Autoencoder (VAE)

> Глубокая latent-variable генеративная модель, обучаемая максимизацией [[ml_concepts/probabilistic/elbo|ELBO]] с [[ml_concepts/probabilistic/amortized-variational-inference|amortized]] гауссовским энкодером и [[ml_concepts/probabilistic/reparameterization-trick]] для end-to-end SGD. Энкодер отображает $x$ в параметры $q(z \mid x)$; декодер отображает $z$ в распределение на $x$.

## Motivation

Постановка — [[ml_concepts/probabilistic/latent-variable-model]] $p(x \mid \theta) = \int p(x \mid z, \theta)\, p(z)\, dz$ с нейросетевым декодером. Хотим обучить её по maximum likelihood на большом датасете немеченых $x$. Интеграл нерасчётен, поэтому в качестве цели обучения берём [[ml_concepts/probabilistic/elbo|ELBO]] — а ему нужно вспомогательное распределение $q(z)$ над латентами.

Взгляд [[methods/inference/variational-em|variational EM]] говорит: чередовать. При фиксированном $\theta$ подогнать $q$ под текущий posterior (E-step); при фиксированном $q$ обновить $\theta$ (M-step). Каждый E-step — отдельная внутренняя задача оптимизации, которую надо решать для *каждого* примера и переделывать всякий раз, когда $\theta$ сдвинется. С глубокими декодерами и миллионами обучающих точек это неподъёмно — per-example posterior не имеют закрытой формы, и нет способа амортизировать стоимость по примерам или шагам обучения.

VAE заменяет per-example оптимизацию [[ml_concepts/probabilistic/amortized-variational-inference|амортизацией]]: одна encoder-сеть $q(z \mid x, \phi)$ предсказывает параметры $q$ как функцию $x$. Стоимость inference на новом примере теперь — один forward pass через энкодер, а параметры энкодера $\phi$ обучаются совместно с параметрами декодера $\theta$ на одном и том же ELBO. Остаётся техническая проблема: $q$ зависит от $\phi$ под ожиданием, поэтому $\nabla_\phi \mathrm{ELBO}$ не проходит через шаг сэмплирования очевидным образом. [[ml_concepts/probabilistic/reparameterization-trick]] решает её: пишем $z = \mu_\phi(x) + \sigma_\phi(x) \odot \varepsilon$ с $\varepsilon \sim \mathcal{N}(0, I)$, и градиенты текут через $\mu_\phi, \sigma_\phi$ как через любое детерминированное вычисление. С этими двумя ингредиентами — амортизованный энкодер и reparameterized сэмплирование — ELBO становится одной дифференцируемой loss, минимизируемой одним оптимизатором end-to-end.

## Problem setting

Дано iid-данные $\{x_i\}$ из неизвестного $\pi(x)$. Нужно подогнать [[ml_concepts/probabilistic/latent-variable-model]] $p(x \mid \theta) = \int p(x \mid z, \theta) p(z)\,dz$ так, чтобы

- из $p(x \mid \theta)$ можно было рисовать новые сэмплы,
- $\log p(x \mid \theta)$ можно было (приближённо) оценивать на новых данных.

Maximum likelihood нерасчётен — у маргинального интеграла нет закрытой формы. VAE обходят это, максимизируя ELBO с амортизованным вариационным posterior.

## Architecture

Две сети с общим loss, но раздельными параметрами:

- **Encoder $q(z \mid x, \phi)$**: вход $x$, выход — параметры диагонального гауссиана над $z$, $(\mu_\phi(x), \sigma_\phi(x))$. Реализует [[ml_concepts/probabilistic/amortized-variational-inference]].
- **Decoder $p(x \mid z, \theta)$**: вход $z$, выход — параметры распределения на $x$ — обычно гауссиан (для непрерывных данных, со средним, предсказываемым сетью) или Bernoulli/categorical (для бинарных или дискретных).
- **Prior $p(z) = \mathcal{N}(0, I)$**: фиксированный стандартный нормальный.

Разделение на encoder–decoder — это «autoencoder»-структура; «вариационная» часть в том, что бутылочное горлышко стохастическое и обучается вероятностной loss.

## Algorithm

Для каждого минибатча $\{x_i\}$:

1. **Encode**: посчитать $\mu_\phi(x_i), \sigma_\phi(x_i)$ для каждого $x_i$.
2. **Sample latent via reparameterization**: $\varepsilon^{(l)} \sim \mathcal{N}(0, I)$; $z_i^{(l)} = \mu_\phi(x_i) + \sigma_\phi(x_i) \odot \varepsilon^{(l)}$.
3. **Decode**: посчитать $\log p(x_i \mid z_i^{(l)}, \theta)$.
4. **Compute loss** = негативный ELBO:

$$
\mathcal{L}_{\text{VAE}}(\phi, \theta; x_i) \;=\; -\frac{1}{L}\sum_{l=1}^L \log p\big(x_i \,\big|\, \mu_\phi(x_i) + \sigma_\phi(x_i) \odot \varepsilon^{(l)},\, \theta\big) \;+\; \frac{1}{2}\sum_{j=1}^d \!\Big(\mu_{\phi,j}^2(x_i) + \sigma_{\phi,j}^2(x_i) - \log \sigma_{\phi,j}^2(x_i) - 1\Big).
$$

5. **Backprop** через обе сети и оба члена совместно. Обновить $(\phi, \theta)$ SGD.

На практике стандарт — $L = 1$; большие $L$ уменьшают дисперсию пропорционально расходу compute.

## Why the loss has that form

Начнём с разложения ELBO:

$$
\mathrm{ELBO}(\phi, \theta; x) \;=\; \mathbb{E}_{z \sim q(z \mid x, \phi)}\!\big[\log p(x \mid z, \theta)\big] - \mathrm{KL}\!\big(q(z \mid x, \phi) \,\|\, p(z)\big).
$$

- **Reconstruction-член** $\mathbb{E}_q[\log p(x \mid z, \theta)]$: оценивается Monte Carlo'м на reparameterized сэмплах. С гауссовским декодером $\log p$ сводится к $-\tfrac{1}{2\sigma^2}\|x - \mu_\theta(z)\|^2 + \text{const}$ — это MSE с точностью до констант. С Bernoulli-декодером — binary cross-entropy.
- **KL-член** $\mathrm{KL}(q(z \mid x, \phi) \,\|\, p(z))$: закрытая форма для Gaussian-vs-Gaussian, Monte Carlo не нужен. См. [[math_concepts/kl-divergence]]:

$$
\mathrm{KL}\!\big(\mathcal{N}(\mu_\phi(x), \mathrm{diag}(\sigma_\phi^2(x))) \,\|\, \mathcal{N}(0, I)\big) \;=\; \tfrac{1}{2}\sum_j \big(\mu_{\phi,j}^2(x) + \sigma_{\phi,j}^2(x) - \log \sigma_{\phi,j}^2(x) - 1\big).
$$

Градиент KL по $\phi$ точен (без сэмплирования). Градиент reconstruction по $\phi$ использует reparameterization trick, чтобы пройти через шаг сэмплирования.

## Why one optimiser, not EM

Взгляд [[methods/inference/variational-em|variational EM]] говорит: при фиксированном $\theta$ выставить $q$, чтобы максимизировать ELBO (E-step); при фиксированном $q$ обновить $\theta$ (M-step). VAE делают и то и другое сразу, потому что:

1. «Точный E-step» $q = p(z \mid x, \theta)$ нерасчётен — $q$ параметризован нейросетью, поэтому мы только приближаем максимум.
2. И reconstruction-член, и KL уже дифференцируемы по $(\phi, \theta)$ внутри одного графа вычислений. Технической причины разделять обновления нет.

На практике loss считается один раз и backprop'ается через обе сети одновременно, в точности как при обучении любой детерминированной глубокой сети.

## Properties

- **Compute:** один forward pass через энкодер, один сэмпл $z$, один forward pass через декодер. Два backward pass'а (decoder, encoder).
- **Гиперпараметры:** размерность latent $d$; модель шума декодера (Gaussian vs Bernoulli); KL-вес $\beta$ в варианте $\beta$-VAE.
- **Failure modes:**
  - **Posterior collapse** — энкодер отображает всё в prior; latent code не несёт информации. Митигация: ослабить декодер, KL annealing, free bits.
  - **Blurry samples** — гауссовский декодер с фиксированной дисперсией даёт размытые $x$. Митигация: per-pixel variance, иерархические декодеры, замена гауссовского декодера на flow или авторегрессионную модель.
  - **Amortization gap** — энкодер недотягивает до оптимального per-example posterior. Митигация: более выразительный энкодер, итеративное уточнение на inference.

## Variants and successors

- **$\beta$-VAE** — домножить KL-член на $\beta > 1$ для disentangled latent'ов (Higgins et al., 2017).
- **Conditional VAE (CVAE)** — условить энкодер и декодер на побочном входе $c$, чтобы моделировать $p(x \mid c)$.
- **IWAE** — более тугая importance-weighted граница, заменяющая single-sample ELBO (Burda et al., 2016).
- **VQ-VAE** — дискретные латенты, обучаемые vector quantisation и straight-through estimator.
- **Hierarchical VAE (например, NVAE)** — многоуровневые latent code, лечит posterior collapse при слабых декодерах.

## Sources

- [[sources/elbo-and-vae-lecture]] — вывод loss, роль reparameterization, закрытая форма гауссовского KL и аргументы за совместную оптимизацию вместо чередующего EM.

## Up next

- [[topics/variational-inference]] — более широкая область: ELBO, амортизованный inference, reparameterization и место VAE в этой картине.
