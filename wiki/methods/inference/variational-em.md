---
title: Variational EM
type: method
tags: [variational-inference, em-algorithm, latent-variable-models, optimisation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
needs_rewrite: true
---

# Variational EM

> Максимизировать [[ml_concepts/elbo|ELBO]] чередованием: при фиксированном $\theta$ обновить вариационное распределение $q$ к ближайшему трактуемому приближению истинного posterior (E-step); при фиксированном $q$ обновить $\theta$ так, чтобы максимизировать expected complete-data log-likelihood (M-step). Обобщает классический EM на случай, когда точный posterior $p(z \mid x, \theta)$ нерасчётен.

## Motivation

Хотим подогнать [[ml_concepts/latent-variable-model]] по maximum likelihood: $\max_\theta \log p(x \mid \theta) = \max_\theta \log \int p(x \mid z, \theta) p(z)\, dz$. Классический EM справляется с этим, когда posterior $p(z \mid x, \theta)$ имеет закрытую форму: E-step считает posterior точно, M-step максимизирует expected complete-data log-likelihood под ним, и вместе они гарантируют монотонный неубывающий $\log p(x \mid \theta)$. Работает для Gaussian mixtures и HMM.

Для более богатых моделей — глубоких генеративных, сложных графовых — точный posterior нерасчётен. E-step ломается: подставлять нечего, а Monte Carlo из prior проваливается по той же причине, что и маргинал (почти ни один prior-сэмпл не объясняет данные). Без пригодного E-step аргумент монотонности рассыпается, и алгоритму нечего чередовать.

Variational EM чинит E-step, ограничивая $q$ трактуемым семейством $\mathcal{Q}$. Тождество [[ml_concepts/elbo|ELBO]] $\log p(x \mid \theta) = \mathrm{ELBO}(q, \theta) + \mathrm{KL}(q \,\|\, p(z \mid x, \theta))$ говорит, что максимизация границы по $q$ эквивалентна минимизации KL до истинного posterior, и значит E-step превращается в «проекцию posterior на $\mathcal{Q}$» — трактуемую задачу оптимизации. M-step без изменений. Монотонность сохраняется для границы, хотя её зазор до $\log p$ уже не закрывается. Покупаем трактуемость ценой фиксированного зазора аппроксимации; меняем гарантию «максимизируем $\log p$» на «максимизируем ELBO». Достаточно ли тугая эта граница — вопрос выбора $\mathcal{Q}$.

## Problem setting

Есть [[ml_concepts/latent-variable-model]] $p(x \mid \theta) = \int p(x \mid z, \theta) p(z)\,dz$, нужно максимизировать $\sum_i \log p(x_i \mid \theta)$. Интеграл нерасчётен, поэтому максимизируем его нижнюю границу $\mathrm{ELBO}(q, \theta)$ совместно по $q$ (вариационному распределению) и $\theta$.

## Algorithm

1. **Initialise** $\theta^{(0)}$.

2. **E-step.** При текущем $\theta^{(t)}$ обновляем вариационное распределение:

   $$
   q^{(t+1)} \;=\; \arg\max_{q}\,\mathrm{ELBO}(q, \theta^{(t)}).
   $$

   Поскольку $\log p(x \mid \theta)$ от $q$ не зависит, и $\log p(x \mid \theta) = \mathrm{ELBO}(q, \theta) + \mathrm{KL}(q \,\|\, p(z \mid x, \theta))$, максимизация ELBO по $q$ эквивалентна минимизации KL до истинного posterior:

   $$
   q^{(t+1)} \;=\; \arg\min_{q}\,\mathrm{KL}\!\big(q(z) \,\|\, p(z \mid x, \theta^{(t)})\big).
   $$

   Если $q$ пробегает все распределения, единственный минимум — истинный posterior $p(z \mid x, \theta^{(t)})$; это и есть классический EM E-step. Если $q$ ограничен трактуемым семейством $\mathcal{Q}$ (mean-field, параметрическое и т.п.), минимум — проекция posterior на $\mathcal{Q}$.

3. **M-step.** При фиксированном $q^{(t+1)}$ обновляем параметры модели:

   $$
   \theta^{(t+1)} \;=\; \arg\max_{\theta}\,\mathrm{ELBO}(q^{(t+1)}, \theta).
   $$

   Отбросив члены, не зависящие от $\theta$:

   $$
   \theta^{(t+1)} \;=\; \arg\max_{\theta}\,\mathbb{E}_{z \sim q^{(t+1)}(z)}\!\big[\log p(x, z \mid \theta)\big].
   $$

   Это expected complete-data log-likelihood под текущим $q$.

4. **Repeat** до сходимости.

## Why it works

Каждая итерация гарантирует неубывание $\log p(x \mid \theta)$:

- **E-step** двигает $q$ к максимуму границы, поэтому $\mathrm{ELBO}(q^{(t+1)}, \theta^{(t)}) \ge \mathrm{ELBO}(q^{(t)}, \theta^{(t)})$.
- **M-step** двигает $\theta$ к максимуму (теперь зафиксированной) границы, поэтому $\mathrm{ELBO}(q^{(t+1)}, \theta^{(t+1)}) \ge \mathrm{ELBO}(q^{(t+1)}, \theta^{(t)})$.

Вместе: граница монотонна. Поскольку $\log p(x \mid \theta) \ge \mathrm{ELBO}(q, \theta)$ всегда, а зазор $\mathrm{KL}(q \,\|\, p(z \mid x, \theta))$ закрывается на каждом E-step в точном случае, сам $\log p(x \mid \theta)$ тоже не убывает — это стандартный аргумент монотонности EM.

В приближённом случае (ограниченное $\mathcal{Q}$) граница монотонна, но зазор не закрывается, поэтому алгоритм сходится к фиксированной точке границы, не обязательно к максимуму $\log p$.

## Why VAEs don't do this verbatim

E-step требует либо точного posterior $p(z \mid x, \theta^{(t)})$ — обычно нерасчётного, — либо нахождения оптимума в каком-то семействе $\mathcal{Q}$. VAE избегают и того и другого:

- Posterior приближается [[ml_concepts/amortized-variational-inference|амортизованным]] энкодером $q(z \mid x, \phi)$.
- Вместо полной оптимизации $\phi$ на каждом шаге $\phi$ и $\theta$ обновляются совместно через SGD на той же loss.

Результат называют **stochastic/generalised variational EM**: каждый «E-step» — это несколько SGD-шагов по $\phi$, каждый «M-step» — несколько SGD-шагов по $\theta$, на практике перемешанных или слитых в одно совместное обновление. См. [[methods/vae]] про joint-update форму.

## Comparison: classical EM vs Variational EM

| Aspect              | Classical EM                                                  | Variational EM                                                                 |
|---------------------|---------------------------------------------------------------|--------------------------------------------------------------------------------|
| E-step              | Считаем $p(z \mid x, \theta^{(t)})$ точно                     | Приближаем внутри $\mathcal{Q}$ минимизацией KL                                |
| Трактуемость        | Нужен закрытый posterior (например, GMM, HMM)                 | Работает с нерасчётными posterior                                              |
| Монотонность в $\log p$ | Гарантирована                                             | Гарантирована для ELBO; для $\log p$ — только при точном E-step                |
| Примеры             | Gaussian mixtures, HMMs, mixture models                       | VAE, deep latent variable models, mean-field VI                                |

## Properties

- **Сходимость:** к локальному максимуму ELBO (не обязательно $\log p$). Инициализация имеет значение.
- **Стоимость итерации:** доминирует E-step (приближение posterior), когда M-step разрешается в закрытой форме.
- **Failure modes:** то же ограниченное семейство $q$, что делает алгоритм трактуемым, заодно ограничивает достижимое правдоподобие — тугое приближение posterior это жёсткое требование.

## Variants and successors

- **Classical EM** — когда точный posterior трактуем.
- **VAE** ([[methods/vae]]) — амортизованный, совместный SGD вместо строгого чередования.
- **Wake-sleep algorithm** — Helmholtz machines, более ранняя схема amortized inference, обновляющая энкодер и декодер в двух отдельных фазах.
- **VBEM / Mean-field VI** — variational Bayes EM с mean-field $q$, часто закрытая форма координатного восхождения.

## Sources

- [[sources/elbo-and-vae-lecture]] — вывод E-step / M-step из ELBO, эквивалентность «max ELBO по $q$ ≡ min KL до posterior» и причины, по которым обучение VAE отступает от строгого чередования.

## Up next

- [[methods/vae]] — заменяет строгое чередование амортизованным совместным SGD; современная инстанция, когда $q$ сам нейросеть.
