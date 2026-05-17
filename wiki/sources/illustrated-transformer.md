---
title: "The Illustrated Transformer (Jay Alammar)"
type: source
source_path: raw/clips/The Illustrated Transformer.md
source_kind: clip
source_date: 2018-06-27
ingested: 2026-05-17
tags: [attention, transformers, multi-head, encoder-decoder, position-encoding, seq2seq]
sources: 1
status: draft
---

# The Illustrated Transformer (Jay Alammar)

> Визуальное введение в архитектуру Transformer (Vaswani et al., 2017): стэки энкодеров и декодеров, поток тензоров между ними, пошаговый разбор self-attention (Q/K/V, scaled dot-product, softmax, взвешенная сумма) и матричной формы, multi-head attention, sinusoidal positional encoding, residual + LayerNorm, masked self-attention и cross-attention в декодере, финальный linear + softmax, training-loss и beam search. Один из самых цитируемых учебных материалов по трансформерам.

## Key takeaways

- **Архитектура — два стэка по 6.** Encoder — стэк из $N = 6$ идентичных по структуре блоков (веса не разделяются), каждый из self-attention + position-wise FFN. Decoder — то же плюс cross-attention между ними. Шесть — гиперпараметр, не магическая константа.
- **Self-attention пошагово.** Из каждого эмбеддинга $x \in \mathbb{R}^{512}$ через $W_Q, W_K, W_V$ получают $q, k, v \in \mathbb{R}^{64}$. Скор $q_m^\top k_n / \sqrt{d_k}$ (делитель $\sqrt{64} = 8$ для стабильных градиентов), softmax по строке, взвешенная сумма $v$. Матрично — $\mathrm{softmax}(Q K^\top / \sqrt{d_k}) V$.
- **Multi-head — восемь параллельных каналов.** Восемь независимых наборов $W_Q^{(h)}, W_K^{(h)}, W_V^{(h)}$ дают восемь $Z^{(h)}$. Уменьшенная размерность head'а ($d_k = d/h$) держит общую стоимость примерно постоянной. Конкатенация и проекция $W^O$ возвращают результат в $\mathbb{R}^d$. Снимает доминирование самотокена; даёт «representation subspaces».
- **Sinusoidal PE прибавляется к эмбеддингу.** Преимущество — модель в принципе может обрабатывать последовательности длиннее обученных. Реализация в Tensor2Tensor интерливит sin/cos иначе, чем формула в статье: статья concat'ит две половины, T2T интерливит покоординатно.
- **Residual + LayerNorm вокруг каждого подслоя.** В обоих стэках: $\mathrm{LayerNorm}(x + \mathrm{Sublayer}(x))$. Без этих обвязок стэк глубиной 6 слоёв не сходится; в посте они упомянуты как «деталь, которую важно отметить».
- **Декодер — три подслоя на блок.** (1) Masked self-attention — будущие позиции зануляются $-\infty$ перед softmax. (2) Encoder-decoder attention — $Q$ из предыдущего подслоя декодера, $K, V$ из выхода *верхнего* слоя энкодера (один и тот же $K, V$ переиспользуется во всех блоках декодера). (3) FFN.
- **Финал — линейный + softmax.** Выход декодера $\in \mathbb{R}^d$ проецируется в $\mathbb{R}^{|V|}$ (логиты по словарю), softmax даёт распределение. Cell с максимальной вероятностью — следующий токен.
- **Обучение — cross-entropy/KL.** На каждом шаге целевое распределение — one-hot на правильном токене, предсказанное — softmax по словарю. Декодинг — greedy или beam search (хранить top-$k$ частичных гипотез, выбирать по совокупной оценке).

## Concepts touched

- [[ml_concepts/attention/self-attention]] — апгрейд stub → draft: полный механизм Q/K/V, scaled dot-product, матричная форма, мотивация через альтернативы RNN. **Главный вклад источника.**
- [[ml_concepts/attention/multi-head-attention]] — новая страница. Мотивация (доминирование самотокена, разные типы отношений), формальное описание ($h$ heads, конкатенация, $W^O$), стоимость.
- [[ml_concepts/attention/variants/cross-attention]] — новая страница. Encoder-decoder attention: $Q$ из декодера, $K, V$ из энкодера; матрица скоров $L_{\text{tgt}} \times L_{\text{src}}$.
- [[ml_concepts/attention/causal-masking]] — новая страница. Маскирование будущих позиций для авторегрессионного декодера; параллельное обучение vs последовательный инференс.
- [[ml_concepts/attention/positional-encodings/index]] — добавлена как второй источник: контекст оригинального трансформера, аддитивная схема, интуиция про осмысленные расстояния после проекции.
- [[methods/architectures/transformer]] — новая страница. Полная архитектура: encoder/decoder стэки, residual + LayerNorm, sinusoidal PE, финальный linear+softmax, варианты (BERT/GPT/T5/ViT).
- [[methods/positional/sinusoidal-position-encoding]] — добавлена как второй источник: расхождение между формулой в статье и реализацией в Tensor2Tensor.
- [[topics/transformers]] — новая страница. Narrative-вход в область: мотивация, core ideas, methods, потомки и направления оптимизации.

## Contradictions and revisions

Нет. Источник первым открывает область трансформеров в вики; существующие соседние страницы ([[ml_concepts/attention/positional-encodings/index]], [[methods/positional/sinusoidal-position-encoding]], [[ml_concepts/attention/positional-encodings/rotary-position-embedding]]) согласуются с его изложением. Stub [[ml_concepts/attention/self-attention]] существовал до ингеста как заглушка из RoPE-лекции; этот источник заполняет его — рост сложности страницы корректен.

## Questions raised

- **Pre-LN vs Post-LN.** Пост использует Post-LN ($\mathrm{LayerNorm}(x + \mathrm{Sublayer}(x))$), современные модели — Pre-LN. Что именно ломается в Post-LN при больших глубинах? Записано в [[methods/architectures/transformer]] и [[topics/transformers]], отдельной `questions/` страницы не создано — нужен сфокусированный источник.
- **Многоголовость и интерпретируемость.** Каждая head специализируется на своём (антецедент, синтаксис) — это наблюдение из ранних разборов BERT/GPT-2. Сохраняется ли оно для современных крупных моделей? Записано в [[ml_concepts/attention/multi-head-attention]].
- **$O(L^2)$ узкое место.** Записано в [[ml_concepts/attention/self-attention]] и [[topics/transformers]] как направление оптимизации (FlashAttention, linear attention, Mamba) — кандидат на отдельную тему при будущем ингесте.

## Notes

- Источник популярный, не академический. Уровень — мотивирующий разбор с диаграммами; точность достаточная для понимания механизма, но детали (точные размеры, расписание learning rate, label smoothing, dropout) не разбираются — это нужно брать из оригинальной статьи Vaswani 2017 (в reading queue на [[topics/transformers]]).
- В посте 2025 года автор обновил его и сослался на свою книгу LLM-book.com (Chapter 3), где разобраны Multi-Query Attention и RoPE. Эти расширения уже частично покрыты в вики: [[methods/positional/rope]], reading queue на [[topics/transformers]] и [[topics/positional-encoding]].
- Изображения. Все диаграммы в источнике — внешние URL'ы на jalammar.github.io. По политике вики (self-contained, без рисков ротации внешних ссылок) embed'ы не делал; описания фигур уходят в прозу концептуальных страниц. Оригинал доступен по URL источника, указанному в frontmatter clip'а.
- Beam search и greedy decoding упомянуты в источнике, но в вики не вынесены в отдельные методы — мотивация выходит за рамки именно трансформера. Оставлены как будущие стабы при ингесте сфокусированного источника по декодингу.
- Residual connection, LayerNorm и position-wise FFN упомянуты в источнике как «детали», но без характеризации. Оставлены как stub-кандидаты в [[methods/architectures/transformer]] и [[topics/transformers]]; самостоятельные страницы создавать на этом источнике преждевременно.

## Pointer back to raw

`raw/clips/The Illustrated Transformer.md`
