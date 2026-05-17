---
title: Grouped Query Attention (GQA)
type: ml_concept
tags: [attention, transformers, kv-cache, inference]
created: 2026-05-17
updated: 2026-05-17
sources: 1
status: draft
---

# Grouped Query Attention (GQA)

> Промежуточный вариант между [[ml_concepts/multi-head-attention|MHA]] и [[ml_concepts/multi-query-attention|MQA]]: $h$ heads делятся на $g$ групп, каждая группа делит свою пару $K, V$. Сокращает [[ml_concepts/kv-cache|KV-кэш]] в $h / g$ раз и в ablations с малыми группами (2–8) даже *обгоняет* full MHA по качеству.

## Motivation

MQA жёстко режет KV-кэш, но платит за это потерей выразительности — heads не могут смотреть на контекст под разными углами, у них одно и то же KV-разложение. MHA сохраняет всю выразительность, но кэш на инференсе становится главным потребителем памяти. Хочется промежуточную точку, в которой одну часть памяти отдаётся, но не всю.

Решение — шарить KV не *одним пулом на все heads* (MQA) и не *по одному пулу на head* (MHA), а *по одному пулу на группу heads*. Группы малы (обычно 2, 4 или 8 групп на слой), и каждая группа имеет собственную пару $K, V$. Heads внутри группы делят KV, между группами — нет.

Сюрприз: в Hugging Face ablations GQA с малыми группами не только догнала MHA, но *обогнала* её на HellaSwag, MMLU и ARC. То есть некоторая степень шаринга KV работает как полезный inductive bias — что-то вроде регуляризации, заставляющей heads внутри группы выучить согласованное KV-пространство. Это резко поменяло позицию GQA: из «компромисса между памятью и качеством» она стала *новым стандартом по умолчанию* для современных моделей (Trinity Large, gpt-oss-120b, SmolLM3, OLMo 3).

## Formal description

Пусть $h$ — число heads, $g$ — число групп KV, $h$ делится на $g$. Каждая группа $G_j \subset \{1, \ldots, h\}$ размера $h / g$ имеет собственные $W_K^{(j)}, W_V^{(j)} \in \mathbb{R}^{d \times d_k}$. Каждая head внутри группы имеет собственную $W_Q^{(i)} \in \mathbb{R}^{d \times d_k}$.

Для head $i$, принадлежащей группе $j(i)$:

$$
Q^{(i)} = X W_Q^{(i)}, \qquad K^{(j(i))} = X W_K^{(j(i))}, \qquad V^{(j(i))} = X W_V^{(j(i))},
$$

$$
Z_i = \mathrm{softmax}\!\left(\frac{Q^{(i)} (K^{(j(i))})^\top}{\sqrt{d_k}}\right) V^{(j(i))}.
$$

Конкатенация и $W^O$ — как в MHA.

KV-кэш на одну позицию:

$$
\text{KV-cache}_{\text{GQA}} = 2 \times g \times n_{\text{layers}} \times d_{\text{head}} \times L,
$$

то есть в $h / g$ раз меньше, чем у MHA, и в $g$ раз больше, чем у MQA. Граничные случаи: $g = h$ даёт MHA, $g = 1$ даёт MQA.

## Spectrum: MHA — GQA — MQA

Все три схемы — точки одного спектра «сколько KV-пар приходится на head»:

```
MHA (h=8, no sharing)         GQA (h=8, g=4 groups)        MQA (h=8, 1 shared KV)
┌──┬──┬──┬──┬──┬──┬──┬──┐    ┌──┬──┬──┬──┬──┬──┬──┬──┐    ┌──┬──┬──┬──┬──┬──┬──┬──┐
│Q₁│Q₂│Q₃│Q₄│Q₅│Q₆│Q₇│Q₈│    │Q₁│Q₂│Q₃│Q₄│Q₅│Q₆│Q₇│Q₈│    │Q₁│Q₂│Q₃│Q₄│Q₅│Q₆│Q₇│Q₈│
├──┼──┼──┼──┼──┼──┼──┼──┤    ├──┴──┼──┴──┼──┴──┼──┴──┤    ├──┴──┴──┴──┴──┴──┴──┴──┤
│K₁│K₂│K₃│K₄│K₅│K₆│K₇│K₈│    │ K₁  │ K₂  │ K₃  │ K₄  │    │         K₁            │
├──┼──┼──┼──┼──┼──┼──┼──┤    ├─────┼─────┼─────┼─────┤    ├────────────────────────┤
│V₁│V₂│V₃│V₄│V₅│V₆│V₇│V₈│    │ V₁  │ V₂  │ V₃  │ V₄  │    │         V₁            │
└──┴──┴──┴──┴──┴──┴──┴──┘    └─────┴─────┴─────┴─────┘    └────────────────────────┘
  8 KV pairs (full cache)       4 KV pairs (cache / 2)        1 KV pair (cache / 8)
```

*Спектр шаринга KV: количество $Q$ сохраняется, число KV-пар на слой меняется.*

## Variations and related concepts

- [[ml_concepts/multi-head-attention]] — крайний случай $g = h$ (полное отсутствие шаринга).
- [[ml_concepts/multi-query-attention]] — крайний случай $g = 1$ (максимальное шаринг).
- [[ml_concepts/multi-latent-attention]] — альтернативный путь сжатия KV: не шарить heads, а сжимать $K, V$ в латентное представление.
- [[ml_concepts/kv-cache]] — bottleneck, ради которого GQA вообще применяется.
- [[methods/transformer]] — современные транcформеры используют GQA вместо MHA в attention-подслоях.

## Open questions

- Почему GQA с малыми группами *обгоняет* MHA, а не просто догоняет? Какая именно регуляризация возникает из шаринга KV внутри группы? Без подробного механистического объяснения это пока эмпирическое наблюдение.
- Существует ли оптимальное соотношение $g$ к $h$ как функция глубины модели, длины контекста или задачи? В практике берут 2, 4 или 8 без явного обоснования.

## Sources

- [[sources/attention-mechanisms-lecture]] — описание спектра MHA → GQA → MQA с диаграммой и формулой кэша; ablation Hugging Face с GQA, превзошедшей MHA на HellaSwag/MMLU/ARC; список frontier-моделей (Trinity Large, gpt-oss-120b, SmolLM3, OLMo 3), использующих GQA по умолчанию.

## Up next

- [[ml_concepts/multi-latent-attention]] — параллельная стратегия сжатия KV, дающая 4–8× компрессии другими средствами.
- [[topics/attention-variants]] — общий narrative по KV-bottleneck'у и его вариантам.
