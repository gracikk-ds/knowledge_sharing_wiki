---
title: Multi-Query Attention (MQA)
type: ml_concept
tags: [attention, transformers, kv-cache, inference]
created: 2026-05-17
updated: 2026-05-17
sources: 1
status: draft
needs_rewrite: true
---

# Multi-Query Attention (MQA)

> Вариант [[ml_concepts/attention/multi-head-attention|multi-head attention]], в котором все $h$ heads делят одну общую пару $K, V$, но каждая имеет свою $Q$. Сокращает [[ml_concepts/attention/kv-cache|KV-кэш]] в $h$ раз ценой потери выразительности: heads вынуждены работать в одном и том же KV-подпространстве.

## Motivation

В стандартном multi-head attention каждая head независимо проецирует вход в свои $Q^{(i)}, K^{(i)}, V^{(i)}$. На инференсе это означает, что KV-кэш хранит $h$ копий ключей и значений на каждый токен. Для моделей с десятками heads и длинными контекстами это становится главным потребителем GPU-памяти.

Заметим, что в одну attention-операцию входит только один $Q$, а $K$ и $V$ потребляются *симметрично* всеми позициями: каждая позиция совпадает с одним и тем же $K, V$ независимо от того, какая head задаёт запрос. Если согласиться, что разные heads будут специализироваться только через свои *запросы*, а сравниваться со всеми позициями через единый набор ключей и единый набор значений, можно выкинуть лишние $h-1$ копий KV и оставить одну. Это и делает MQA: один $W_K, W_V$ на весь слой, $h$ независимых $W_Q^{(i)}$.

Цена очевидна: heads теряют возможность смотреть на разные «измерения» одного и того же контекста по-разному — у них на руках одно и то же KV-разложение входа. Ablation'ы (Hugging Face) подтверждают, что MQA проигрывает MHA по качеству на HellaSwag/MMLU/ARC; именно эта потеря заставила появиться [[ml_concepts/attention/efficiency/grouped-query-attention|GQA]] как компромисс.

## Formal description

Стандартный MHA: $h$ независимых $W_Q^{(i)}, W_K^{(i)}, W_V^{(i)} \in \mathbb{R}^{d \times d_k}$. MQA оставляет независимыми только $W_Q$:

$$
W_Q^{(1)}, \ldots, W_Q^{(h)} \in \mathbb{R}^{d \times d_k}, \qquad W_K, W_V \in \mathbb{R}^{d \times d_k}.
$$

Для каждой head $i$:

$$
Q^{(i)} = X W_Q^{(i)}, \qquad K = X W_K, \qquad V = X W_V,
$$

и выход head'а считается стандартным scaled dot-product attention'ом:

$$
Z_i = \mathrm{softmax}\!\left(\frac{Q^{(i)} K^\top}{\sqrt{d_k}}\right) V.
$$

Конкатенация и проекция $W^O$ — как в MHA.

KV-кэш на одну позицию:

$$
\text{KV-cache}_{\text{MQA}} = 2 \times 1 \times n_{\text{layers}} \times d_{\text{head}} \times L,
$$

то есть в $h$ раз меньше, чем у MHA. Это и есть весь выигрыш и весь компромисс.

## Variations and related concepts

- [[ml_concepts/attention/multi-head-attention]] — исходная схема, относительно которой MQA — крайний случай шаринга.
- [[ml_concepts/attention/efficiency/grouped-query-attention]] — промежуточная точка: heads делятся на группы, каждая группа имеет свой $K, V$. Снимает значительную часть потери качества MQA.
- [[ml_concepts/attention/efficiency/multi-latent-attention]] — альтернативный подход к сжатию KV (через латентное представление, а не через шаринг).
- [[ml_concepts/attention/kv-cache]] — bottleneck, ради которого MQA вообще появился.

## Open questions

- Почему MQA так сильно проигрывает MHA, а GQA с малыми группами — нет? Что именно ломается, когда heads вынуждены делить ровно один KV вместо нескольких?

## Sources

- [[sources/attention-mechanisms-lecture]] — MQA как крайний случай шаринга KV; ссылка на ablation Hugging Face, подтверждающий заметный проигрыш MHA.

## Up next

- [[ml_concepts/attention/efficiency/grouped-query-attention]] — компромисс, который снимает потерю выразительности MQA, не отказываясь от выигрыша по памяти.
- [[ml_concepts/attention/efficiency/multi-latent-attention]] — альтернативная стратегия: сжимать кэш, не шаря heads.
