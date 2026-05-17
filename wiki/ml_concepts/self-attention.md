---
title: Self-Attention
type: ml_concept
tags: [attention, transformers, sequence-models]
created: 2026-05-17
updated: 2026-05-17
sources: 1
status: stub
---

# Self-Attention

> Слой трансформера, в котором каждый токен формирует свой query, key и value-вектор из общего входного эмбеддинга, а выход — это взвешенная сумма value-векторов всех токенов, где веса определяются softmax от скалярных произведений $QK^\top / \sqrt{d_k}$.

## Key property: permutation equivariance

Без позиционного сигнала self-attention — функция от *множества* токенов, а не от их *последовательности*. Если переставить токены на входе, выход переставится так же, но содержательно не изменится. Скалярное произведение $q_m^\top k_n$ зависит от содержимого $q_m, k_n$, а не от их позиций $m, n$. Чтобы трансформер видел порядок, нужно явно добавить позиционную информацию — это и решает [[ml_concepts/positional-encoding]].

## Sources

- [[sources/rope-lecture]] — упоминает permutation equivariance как стартовую мотивацию для RoPE.
