---
title: Progressive Distillation
type: method
tags: [distillation, diffusion, few-step-generation]
created: 2026-05-15
updated: 2026-05-15
sources: 1
status: stub
needs_rewrite: true
---

# Progressive Distillation

> Итеративно distill diffusion-учителя в student'а, делающего один шаг там, где учитель делал два; число шагов делится пополам в каждом раунде.

Это канонический multi-step рецепт [[ml_concepts/generative/step-distillation]]. Каждый раунд обучает свежего student'а на loss'е

$$
\mathcal{L}_{\text{KD}_m}(\theta) \;=\; \mathbb{E}_{t, x_0, x_t}\big\lVert x_\theta(x_t, t) - \hat{x}_\phi(x_t, t) \big\rVert_2^2,
$$

где $\hat{x}_\phi(x_t, t)$ — выход учителя после **двух** ODE-шагов из $(x_t, t)$. После сходимости student становится учителем следующего раунда, и число шагов сэмплирования делится пополам каждый раз.

Лекция упоминает его только как предшественника, мотивировавшего CMs и flow-map методы; подробности (расписание, warm-start, параметризация) идут из оригинальной статьи Salimans & Ho (2022), не из этого источника.

## Sources

- [[sources/flow-map-models-lecture]] — упомянут как «multi-step KD, progressive distillation».
