---
title: Evidence Lower Bound (ELBO)
type: ml_concept
tags: [variational-inference, latent-variable-models, generative-models, training-objectives, vae]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
needs_rewrite: true
---

# Evidence Lower Bound (ELBO)

> Трактуемая нижняя граница маргинального log-likelihood $\log p(x \mid \theta)$ для latent-variable модели, полученная введением вспомогательного распределения $q(z)$ над латентами. ELBO — центральная цель обучения variational inference и VAE.

## Motivation

У нас есть [[ml_concepts/probabilistic/latent-variable-model]] $p(x \mid \theta) = \int p(x \mid z, \theta)\,p(z)\,dz$. Чтобы обучить её через максимум правдоподобия, нужен этот интеграл. Закрытой формы у него нет, поэтому первый инстинкт — Монте-Карло: семплируем $z \sim p(z)$ и усредняем $p(x \mid z, \theta)$. Это ломается по конкретной причине: для фиксированного $x$ почти каждый сэмпл из prior попадает в такой $z$, который к $x$ отношения не имеет, и $p(x \mid z, \theta) \approx 0$. Из тысячи сэмплов вклад дают единицы; дисперсия оценки огромна.

ELBO решает эту проблему. Вместо $p(z)$ семплируем из более умного $q(z)$, сосредоточенного на тех латентах, что могут объяснить $x$. Величина, которую можно так оценить, — это *нижняя граница* на $\log p(x \mid \theta)$, не сам логарифм, но граница тугая, когда $q$ близок к истинному posterior, и зазор сужается по мере улучшения $q$.

Отсюда два прочтения границы, оба содержательные. Как Jensen's-граница она верна для *любого* допустимого $q$, поэтому можно выбрать $q$ из трактуемого семейства и всё равно получить пригодный сигнал обучения. Как точное тождество $\log p(x \mid \theta) = \mathrm{ELBO}(q, \theta) + \mathrm{KL}(q(z) \,\|\, p(z \mid x, \theta))$ — зазор между границей и истинным log-evidence равен KL от $q$ до истинного posterior. Равенство достигается, когда $q$ — истинный posterior. Поэтому при совместном обучении VAE по $\theta$ и $q$ происходят сразу две вещи: толкается маргинальная правдоподобность модели вверх, а $q$ тянется к истинному posterior.

## Formal description

**Derivation via Jensen's inequality.** Для любого $q(z)$, положительного там, где $p(x, z \mid \theta) > 0$, умножим и поделим на $q(z)$ внутри интеграла и применим [[math_concepts/jensens-inequality]] с вогнутым $\log$:

$$
\log p(x \mid \theta) = \log \int q(z)\,\frac{p(x, z \mid \theta)}{q(z)}\,dz = \log\,\mathbb{E}_{z \sim q}\!\Big[\frac{p(x, z \mid \theta)}{q(z)}\Big] \ge \mathbb{E}_{z \sim q}\!\Big[\log \frac{p(x, z \mid \theta)}{q(z)}\Big]
$$

Правая часть — **ELBO**:

$$
\mathrm{ELBO}(q, \theta) \;=\; \mathbb{E}_{z \sim q(z)}\!\Big[\log \frac{p(x, z \mid \theta)}{q(z)}\Big].
$$

**Exact identity with the posterior gap.** Через правило Байеса $p(x, z \mid \theta) = p(z \mid x, \theta)\,p(x \mid \theta)$:

$$
\mathrm{ELBO}(q, \theta) = \int q(z)\,\log\frac{p(z \mid x, \theta)\,p(x \mid \theta)}{q(z)}\,dz = \log p(x \mid \theta) - \mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta)\big).
$$

Эквивалентно:

$$
\boxed{\;\log p(x \mid \theta) \;=\; \mathrm{ELBO}(q, \theta) \;+\; \mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta)\big)\;}
$$

Поскольку [[math_concepts/kl-divergence]] неотрицательна, отсюда восстанавливается $\log p(x \mid \theta) \ge \mathrm{ELBO}(q, \theta)$ — и точно видно, когда достигается равенство: $q(z) = p(z \mid x, \theta)$.

**Reconstruction–regularisation decomposition.** Разложение $p(x, z \mid \theta) = p(x \mid z, \theta)\,p(z)$ даёт форму, используемую в VAE:

$$
\mathrm{ELBO}(q, \theta) \;=\; \underbrace{\mathbb{E}_{z \sim q}\!\big[\log p(x \mid z, \theta)\big]}_{\text{reconstruction}} \;-\; \underbrace{\mathrm{KL}\!\big(q(z) \,\|\, p(z)\big)}_{\text{regularisation}}.
$$

Первый член заставляет декодер $p(x \mid z, \theta)$ ставить высокую вероятность на $x$, когда $z$ берётся из $q$. Для гауссовского декодера это (с точностью до констант) MSE; для бернуллиевского — cross-entropy. Второй член не даёт $q$ слишком уехать от prior $p(z)$ — иначе модель могла бы переобучиться, подбирая под каждый $x$ свой конкретный $z$.

## Optimisation

Поскольку $\log p(x \mid \theta) \ge \mathrm{ELBO}(q, \theta)$, максимизация границы совместно по $\theta$ и $q$ — это прокси для maximum likelihood:

$$
\max_\theta \log p(x \mid \theta) \;\Rightarrow\; \max_{\theta, q}\,\mathrm{ELBO}(q, \theta).
$$

Две парадигмы:

- **[[methods/inference/variational-em]]** — чередовать: при фиксированном $\theta$ выставить $q$ так, чтобы максимизировать ELBO (E-step); при фиксированном $q$ обновить $\theta$ (M-step). При фиксированном $\theta$ $\log p(x \mid \theta)$ от $q$ не зависит, поэтому максимизация ELBO по $q$ эквивалентна минимизации $\mathrm{KL}(q \,\|\, p(z \mid x, \theta))$, то есть подгонке $q$ к истинному posterior.
- **VAE** — параметризуем $q$ как $q(z \mid x, \phi)$ через [[ml_concepts/probabilistic/amortized-variational-inference]] (encoder network) и обновляем $(\phi, \theta)$ совместно через SGD. См. [[methods/architectures/vae]].

Две координаты градиента обрабатываются по-разному:

- $\nabla_\theta \mathrm{ELBO}$: $q$ от $\theta$ не зависит, поэтому градиент проходит внутрь ожидания, и оценка тривиально считается Monte Carlo.
- $\nabla_\phi \mathrm{ELBO}$: $q$ зависит от $\phi$. Наивная перестановка градиента и ожидания неверна; нужен [[ml_concepts/probabilistic/reparameterization-trick]] (или более высоко-дисперсная score-function оценка).

## Variations and related concepts

- [[ml_concepts/probabilistic/latent-variable-model]] — постановка, мотивирующая ELBO.
- [[ml_concepts/probabilistic/variational-inference]] — фреймворк вокруг ELBO.
- [[ml_concepts/probabilistic/amortized-variational-inference]] — общая сеть на все $x$ вместо per-example $q$.
- [[ml_concepts/probabilistic/reparameterization-trick]] — как протолкнуть backprop через $\nabla_\phi \mathrm{ELBO}$.
- [[methods/architectures/vae]] — ELBO с гауссовским амортизованным энкодером, end-to-end обучение.
- [[methods/inference/variational-em]] — ELBO, максимизированный чередованием $q$ и $\theta$.
- [[math_concepts/jensens-inequality]] — задаёт направление неравенства.
- [[math_concepts/kl-divergence]] — измеряет зазор границы и появляется в регуляризационном члене.

## Open questions

- {пока нет}

## Sources

- [[sources/elbo-and-vae-lecture]] — вывод через Jensen, тождество с зазором posterior, разложение reconstruction–regularisation и пути оптимизации EM/VAE.

## Up next

- [[ml_concepts/probabilistic/reparameterization-trick]] — как считается $\nabla_\phi \mathrm{ELBO}$ в моделях, где $q$ зависит от нейросети.
- [[methods/architectures/vae]] — канонический метод, построенный на ELBO.
