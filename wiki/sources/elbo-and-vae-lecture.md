---
title: "ELBO and VAE — lecture"
type: source
source_path: raw/lectures/ELBO_and_VAE.md
source_kind: lecture
source_date: 2025-10-26
ingested: 2026-05-15
tags: [variational-inference, latent-variable-models, elbo, vae, reparameterization, kl-divergence]
sources: 1
status: draft
---

# ELBO and VAE — lecture

> Самодостаточная лекция: ELBO выводится с нуля, разлагается на reconstruction и regularisation, и проходится полный сюжет обучения VAE, включая reparameterization trick и закрытую форму гауссовского KL.

## Key takeaways

- **Why MLE alone is not enough.** Минимизация forward KL $\mathrm{KL}(\pi \,\|\, p_\theta)$ сводится к максимизации $\mathbb{E}_\pi[\log p(x \mid \theta)]$. Даже если выучить $p(x \mid \theta)$ как параметрическую плотность, сэмплировать из неё всё ещё может быть тяжело — отсюда и мотивация для латентной структуры.
- **Latent-variable models** факторизуют $p(x \mid \theta) = \int p(x \mid z, \theta) p(z) dz$. Сэмплирование становится тривиальным; маргинал может быть сколь угодно сложным даже из простых компонент.
- **Naïve Monte Carlo over the prior fails.** Для конкретного $x$ значение имеют только те $z$, что его объясняют; почти все сэмплы из prior к делу не относятся. Нужное число сэмплов растёт вместе с расхождением между prior и posterior.
- **ELBO via Jensen.** Вставляем $q(z)/q(z)$, применяем Jensen к вогнутому $\log$: $\log p(x \mid \theta) \ge \mathbb{E}_q[\log p(x, z \mid \theta)/q(z)]$. Граница работает для любого допустимого $q$.
- **ELBO via Bayes.** Через $p(x, z) = p(z \mid x) p(x)$ получается точное тождество $\log p(x \mid \theta) = \mathrm{ELBO}(q, \theta) + \mathrm{KL}(q(z) \,\|\, p(z \mid x, \theta))$. Зазор — это в точности KL от $q$ до истинного posterior; равенство iff $q = p(z \mid x, \theta)$.
- **Decomposition into reconstruction + regularisation.** Разложение $p(x, z) = p(x \mid z) p(z)$ даёт $\mathrm{ELBO} = \mathbb{E}_q[\log p(x \mid z, \theta)] - \mathrm{KL}(q(z) \,\|\, p(z))$ — функционал потерь VAE.
- **Variational EM.** Поочерёдно: E-step при фиксированном $\theta$ максимизирует ELBO по $q$ (эквивалентно минимизации KL до posterior); M-step при фиксированном $q$ максимизирует ELBO по $\theta$.
- **Amortised inference.** Заменяем per-example $q$ сетью $q(z \mid x, \phi)$, чтобы закрыть две проблемы разом: труднообъемность точного posterior и необходимость отдельного $q$ под каждый $x$.
- **Reparameterization trick.** Переписываем $z \sim q(z \mid x, \phi)$ как $z = g_\phi(x, \varepsilon)$ с фиксированным $\varepsilon \sim p(\varepsilon)$. По LOTUS ожидание теперь по $\phi$-независимой мере; градиенты текут через $g_\phi$. Альтернатива через score-function unbiased, но с высокой дисперсией.
- **Final VAE loss.** С гауссовским энкодером и prior $\mathcal{N}(0, I)$ KL берётся в закрытой форме (сумма $\mu_j^2 + \sigma_j^2 - \log\sigma_j^2 - 1$ по latent-измерениям). Reconstruction-член использует один reparameterized сэмпл; вся loss — один SGD-шаг по $(\phi, \theta)$.

## Concepts touched

- [[ml_concepts/probabilistic/elbo]] — центральный концепт лекции; выведен двумя способами (Jensen и Bayes), разложен тремя способами (исходный, с зазором до posterior, reconstruction+regularisation). Новая страница.
- [[ml_concepts/probabilistic/latent-variable-model]] — постановка; аналогия с законом полной вероятности; режим отказа наивного Монте-Карло. Новая страница.
- [[ml_concepts/probabilistic/variational-inference]] — фреймворк; тождество, позволяющее оптимизировать ELBO, не вычисляя истинный KL. Новая страница.
- [[ml_concepts/probabilistic/amortized-variational-inference]] — энкодер как сеть, отображающая $x$ в параметры posterior; мотивация — труднообъемность и проблема «отдельный $q$ под каждый $x$». Новая страница.
- [[ml_concepts/probabilistic/reparameterization-trick]] — вывод через LOTUS; канонический гауссовский случай; контраст со score-function оценкой. Новая страница.
- [[math_concepts/kl-divergence]] — задаёт зазор bound; закрытая форма гауссовского KL, используемая в loss VAE; доказательство неотрицательности. Новая страница.
- [[math_concepts/jensens-inequality]] — позволяет превратить $\log \mathbb{E}_q[\cdot]$ в $\mathbb{E}_q[\log \cdot]$. Новая страница.
- [[methods/architectures/vae]] — алгоритм, архитектура, почему один совместный оптимизатор вместо EM. Новая страница.
- [[methods/inference/variational-em]] — фреймворк чередования, эквивалентность «max ELBO по $q$ ≡ min KL до posterior», почему VAE не делает строгий EM. Новая страница.

## Contradictions and revisions

Нет. Это первый ингест в области variational inference; противоречить пока нечему.

## Questions raised

Пока никаких. Возможные продолжения для будущих источников: amortization gap (количественный эффект), posterior collapse (почему некоторые декодеры его триггерят), более тугие bound'ы (IWAE), и роль forward vs reverse KL в разных парадигмах генеративного моделирования.

## Notes

- Лекция написана русской прозой с английскими формулами. Концепты и обозначения стандартные.
- В лекции есть кросс-ссылки между подсекциями в стиле Notion; они указывают на внутреннюю структуру самого источника и не требуют отдельных страниц вики.
- Пример отказа наивного Монте-Карло ($x = 10$, $z \sim \mathcal{N}(0, 1)$, $\sigma = 0.1$) — конкретная иллюстрация расхождения prior–posterior; зафиксирован на [[ml_concepts/probabilistic/latent-variable-model]] в секции «Why naïve Monte Carlo fails».
- Score-function оценка упоминается только как высокодисперсная альтернатива reparameterization и не выводится подробно; кратко описана на [[ml_concepts/probabilistic/reparameterization-trick]]. Отдельный источник мог бы развернуть её в собственную страницу.

## Pointer back to raw

`raw/lectures/ELBO_and_VAE.md`
