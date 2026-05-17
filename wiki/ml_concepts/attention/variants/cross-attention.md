---
title: Cross-Attention
type: ml_concept
tags: [attention, transformers, encoder-decoder, seq2seq]
created: 2026-05-17
updated: 2026-05-17
sources: 1
status: draft
needs_rewrite: true
---

# Cross-Attention

> Тот же механизм, что [[ml_concepts/self-attention|self-attention]], но queries и keys/values считаются из *разных* последовательностей. В энкодер-декодер трансформере $Q$ берётся из предыдущего слоя декодера, а $K, V$ — из выхода всего энкодерного стека. Так декодер для каждого генерируемого токена фокусируется на релевантных позициях входной последовательности.

## Motivation

В seq2seq задаче (перевод, суммаризация, image captioning) есть две последовательности: входная — её надо понять — и выходная — её надо породить. [[ml_concepts/self-attention|Self-attention]] работает внутри одной последовательности: позиции смотрят друг на друга, формируя контекстуализированное представление. Этого достаточно для энкодера, который только читает вход, и для декодера, который смотрит на уже сгенерированные токены.

Но как декодер должен заглядывать в энкодер? Конкретно: на шаге генерации $t$ нужно решить, какие токены входной последовательности сейчас важны. В классическом seq2seq с RNN это делал отдельный attention-слой между декодером и энкодером (Bahdanau, Luong). Трансформер сохраняет ту же идею, переиспользуя механизм attention, но «расщепляет» источники Q и K/V:

- Query приходит из текущего слоя декодера — это «что я ищу прямо сейчас, чтобы предсказать следующее слово».
- Keys и values приходят из выхода энкодера — это «вот что есть во входной последовательности и под каким адресом».

Декодер в результате получает прямой доступ ко всем позициям входа за одну операцию, без рекуррентности и без слияния входной информации в одно сжатое состояние. Каждый слой декодера независимо «спрашивает» энкодер о своём.

## Formal description

Пусть $H^{\text{enc}} \in \mathbb{R}^{L_{\text{src}} \times d}$ — выход верхнего слоя энкодера, $H^{\text{dec}} \in \mathbb{R}^{L_{\text{tgt}} \times d}$ — выход предыдущего подслоя текущего слоя декодера. Cross-attention использует три проекции, как и обычный self-attention, но запускает $W_Q$ на $H^{\text{dec}}$, а $W_K, W_V$ — на $H^{\text{enc}}$:

$$
Q = H^{\text{dec}} W_Q, \qquad K = H^{\text{enc}} W_K, \qquad V = H^{\text{enc}} W_V.
$$

Дальше — стандартный scaled dot-product:

$$
\mathrm{CrossAttention}(H^{\text{dec}}, H^{\text{enc}}) = \mathrm{softmax}\!\left(\frac{Q K^\top}{\sqrt{d_k}}\right) V.
$$

Матрица скоров теперь прямоугольная: $L_{\text{tgt}} \times L_{\text{src}}$. Строка $m$ — распределение веса позиции $m$ выходной последовательности по всем позициям входной. Выход — $L_{\text{tgt}} \times d_k$, та же форма, что и у входа $H^{\text{dec}}$.

В энкодер-декодер трансформере cross-attention применяется multi-head (см. [[ml_concepts/multi-head-attention]]) и стоит как *второй* подслой в каждом блоке декодера: после masked self-attention и до feed-forward.

## Variations and related concepts

- [[ml_concepts/self-attention]] — частный случай, когда оба потока — это один и тот же $H$. Cross-attention обобщает на два разных источника.
- [[ml_concepts/multi-head-attention]] — cross-attention в трансформере всегда multi-head.
- [[ml_concepts/causal-masking]] — на cross-attention не применяется: декодер имеет право смотреть на весь вход целиком.
- [[methods/transformer]] — cross-attention — это второй подслой каждого блока декодера, мост между двумя стэками.

## Open questions

- В decoder-only моделях (GPT-style) cross-attention отсутствует — мультимодальный вход кодируется в общую последовательность и обрабатывается self-attention'ом. Как соотносятся выразительность и стоимость двух подходов?

## Sources

- [[sources/illustrated-transformer]] — описывает encoder-decoder attention как «такой же multi-head, но Q из нижнего слоя декодера, K/V из выхода энкодерного стека»; объясняет роль в seq2seq генерации.

## Up next

- [[ml_concepts/causal-masking]] — другая модификация attention, нужная для авторегрессионной генерации в декодере.
- [[methods/transformer]] — как cross-attention встроен в каждый блок декодера между masked self-attention и feed-forward.
