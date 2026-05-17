---
title: Latent Variable Model
type: ml_concept
tags: [generative-models, latent-variable-models, variational-inference, vae]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: draft
---

# Latent Variable Model

> Генеративная модель, которая рисует каждое наблюдение $x$ в два шага: сначала latent $z \sim p(z)$ из простого prior, затем $x \sim p(x \mid z, \theta)$ из обученного conditional. Маргинализация по $z$ превращает простой рецепт в гибкое распределение.

## Motivation

Хотим генеративную модель для данных $x$ — изображений, текста, аудио — чьё маргинальное распределение сложное и высокоразмерное. Прямая параметризация $p(x \mid \theta)$ — тупик: любая выразительная функциональная форма плотности на пространстве в миллион пикселей не нормализуется в разумной форме, а любая трактуемая (гауссиан, полностью факторизованная модель) слишком жёсткая, чтобы лечь на реальные данные.

Трюк — отказаться от одношагового задания плотности и построить её как двухшаговый процесс сэмплирования. Сначала рисуем latent $z$ из простого prior $p(z)$ — обычно $\mathcal{N}(0, I)$, — затем $x$ из параметрического conditional $p(x \mid z, \theta)$, обычно нейросеть. Каждый $z$ становится низкоразмерным резюме (стилем, классом, семантикой), и сеть отображает его в распределение на наблюдениях. Сэмплирование теперь — один forward pass: сэмпл $z$ из prior, потом $x$ при условии $z$. Маргинал $p(x \mid \theta) = \int p(x \mid z, \theta)\,p(z)\,dz$ может быть сколь угодно сложным, даже когда $p(z)$ и $p(x \mid z)$ простые. Это непрерывная версия закона полной вероятности: $P(A) = \sum_i P(A \mid B_i)\,P(B_i)$ пишет сложное распределение как смесь, индексированную простыми условными событиями; роль $B_i$ играет $z$.

Подвох обнаруживается при попытке обучить эту модель. Maximum likelihood требует $\log p(x \mid \theta)$, а тот — интеграла. Закрытой формы нет, а наивный Monte Carlo — усреднить $p(x \mid z, \theta)$ по $z$ из prior — ломается, потому что prior ничего не знает о том конкретном $x$, на котором мы условились. Почти каждый prior-сэмпл приземляется на $z$, к $x$ отношения не имеющий, $p(x \mid z, \theta) \approx 0$, и дисперсия оценки почти бесконечна.

Это и есть бутылочное горлышко, мотивирующее [[ml_concepts/variational-inference]] и [[ml_concepts/elbo|ELBO]]. Вместо слепого сэмплирования $z$ — берём из распределения $q(z)$, сосредоточенного на latent'ах, которые могли бы породить $x$. Цена смены меры — нижняя граница на log-evidence вместо самого log-evidence: трактуемый суррогат, на котором стоит обучение всех современных latent-variable моделей.

## Formal description

Latent-variable генеративная модель задаётся prior и likelihood:

$$
z \sim p(z), \qquad x \mid z \sim p(x \mid z, \theta).
$$

Маргинал по наблюдениям:

$$
p(x \mid \theta) \;=\; \int p(x \mid z, \theta)\,p(z)\,dz.
$$

Обучение максимизирует $\sum_i \log p(x_i \mid \theta)$ по данным; эквивалентно — минимизирует forward KL $\mathrm{KL}(\pi(x) \,\|\, p(x \mid \theta))$ между распределением данных $\pi$ и моделью.

## Why naïve Monte Carlo fails

Маргинал можно записать как ожидание по prior, $p(x \mid \theta) = \mathbb{E}_{z \sim p(z)}[p(x \mid z, \theta)]$, что наводит на прямую оценку:

$$
p(x \mid \theta) \;\approx\; \frac{1}{K} \sum_{k=1}^K p(x \mid z_k, \theta), \qquad z_k \overset{\text{iid}}{\sim} p(z).
$$

Это безнадёжно, когда $p(x \mid z, \theta)$ остро пикован по $z$. Для конкретного $x$ значимый вклад дают только те $z$, что его объясняют; всё остальное практически ноль. Конкретный пример отказа: с $z \sim \mathcal{N}(0, 1)$ и $x \mid z \sim \mathcal{N}(z, \sigma^2)$ при малом $\sigma$ наблюдение $x = 10$ хорошо объясняется только $z \approx 10$, но $z \sim \mathcal{N}(0, 1)$ такие сэмплы практически не выдаёт. Требуемое $K$ растёт экспоненциально с расхождением prior и posterior.

Это и есть бутылочное горлышко, мотивирующее [[ml_concepts/variational-inference]]: вместо слепого сэмплирования $z$ из prior берём из распределения $q(z)$, сконцентрированного на значениях, объясняющих $x$. Цена смены меры — оценка [[ml_concepts/elbo|ELBO]] на log-evidence.

## Variations and related concepts

- [[ml_concepts/elbo]] — граница, делающая оптимизацию трактуемой.
- [[ml_concepts/variational-inference]] — фреймворк вокруг приближённых posterior.
- [[ml_concepts/amortized-variational-inference]] — общая сеть на все $x$.
- [[methods/vae]] — каноническая latent-variable модель с amortized inference.
- [[methods/variational-em]] — чередующая оптимизация модели и posterior.

## Open questions

- {нет}

## Sources

- [[sources/elbo-and-vae-lecture]] — постановка, мотивация и режим отказа наивного Monte Carlo.

## Up next

- [[ml_concepts/variational-inference]] — фреймворк, превращающий нерасчётный posterior inference в трактуемую оптимизацию.
- [[ml_concepts/elbo]] — нижняя граница на $\log p(x \mid \theta)$, на которой стоит maximum-likelihood обучение latent-variable моделей.
