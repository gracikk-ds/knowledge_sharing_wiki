---
title: Transformer
type: method
tags: [attention, transformers, seq2seq, encoder-decoder]
created: 2026-05-17
updated: 2026-05-17
sources: 1
status: draft
needs_rewrite: true
---

# Transformer

> Sequence-to-sequence архитектура (Vaswani et al., 2017), полностью построенная на attention: стек идентичных энкодеров (self-attention + feed-forward), стек идентичных декодеров (masked self-attention + cross-attention + feed-forward), residual-связки и LayerNorm вокруг каждого подслоя, sinusoidal positional encoding на входе. Никакой рекуррентности и конволюций; вся обработка последовательности параллелится по позициям.

## Motivation

До трансформера sequence-to-sequence модели строились на RNN и LSTM. У этой линии было два упрямых ограничения. Первое — последовательность шагов: скрытое состояние на позиции $t$ нельзя вычислить, не вычислив сначала $t-1$. Это делает обучение медленным и плохо масштабируется на GPU, где хочется параллелить всё, что можно. Второе — длинные зависимости: информация о токене на позиции $1$ должна пройти через $L$ перезаписей скрытого состояния, чтобы достичь позиции $L$, и за это путешествие её обычно сжимают так, что почти ничего не остаётся.

Конволюционные альтернативы (ByteNet, ConvS2S) частично решали первое, но имели ограниченное receptive field: чтобы соединить далёкие токены, нужно много слоёв.

Vaswani et al. предложили выкинуть и рекуррентность, и свёртку и строить модель только из [[ml_concepts/attention/self-attention|self-attention]] и feed-forward слоёв. Self-attention соединяет любые две позиции за одну операцию ($O(1)$ путь между ними) и параллелится по позициям внутри слоя ($O(L^2)$ работы, но всё это — две матричные операции). Feed-forward даёт нелинейную трансформацию каждой позиции независимо. Чтобы attention видел порядок, добавляется [[ml_concepts/attention/positional-encodings/index|positional encoding]]; чтобы стэк глубиной 6+ слоёв обучался — residual-связки и LayerNorm; чтобы один слой умел представлять разные типы отношений — [[ml_concepts/attention/multi-head-attention|multi-head attention]]; чтобы декодер был авторегрессионным — [[ml_concepts/attention/causal-masking|causal masking]]; чтобы декодер видел вход — [[ml_concepts/attention/variants/cross-attention|cross-attention]] между ним и энкодером.

В сумме получается архитектура, которая обучается заметно быстрее RNN-баз, выигрывает у Google NMT на WMT, и (что окажется важнее) служит фундаментом BERT, GPT, T5, ViT, Whisper, и почти всех современных LLM.

## Problem setting

Дано: входная последовательность токенов длины $L_{\text{src}}$, выходная — длины $L_{\text{tgt}}$, общий словарь или два разных словаря (например, английский и немецкий для перевода). Цель: научить модель распределению $p(\text{выход} \mid \text{вход})$ так, чтобы декодинг давал осмысленный перевод/ответ.

Обучение — teacher-forced cross-entropy: на шаге обучения декодеру подаётся правильная целевая последовательность со сдвигом на один токен, и модель предсказывает следующий токен на каждой позиции параллельно. Инференс — авторегрессионный: токен за токеном, обычно с greedy decoding или beam search.

## Architecture

**Вход.** Токенный эмбеддинг $E \in \mathbb{R}^{L \times d}$ ($d = 512$ в оригинале), к нему прибавляется [[methods/positional/sinusoidal-position-encoding|sinusoidal PE]] той же формы. Один и тот же эмбеддинг используется на входе энкодера и декодера (часто шарится с финальной проекцией в логиты).

**Encoder.** $N = 6$ идентичных по структуре блоков (веса не разделяются). Каждый блок — два подслоя:

1. Multi-head self-attention (8 heads, $d_k = d_v = 64$).
2. Position-wise feed-forward: $\mathrm{FFN}(x) = \max(0, x W_1 + b_1) W_2 + b_2$, скрытая размерность $d_{\text{ff}} = 2048$.

Каждый подслой обёрнут в residual + LayerNorm: $\mathrm{LayerNorm}(x + \mathrm{Sublayer}(x))$.

**Decoder.** $N = 6$ идентичных блоков. Каждый — три подслоя:

1. Masked multi-head self-attention (нижне-треугольная маска — см. [[ml_concepts/attention/causal-masking]]).
2. Multi-head [[ml_concepts/attention/variants/cross-attention|cross-attention]]: $Q$ из предыдущего подслоя декодера, $K, V$ из выхода *верхнего* слоя энкодера (один и тот же $K, V$ для всех блоков декодера).
3. Position-wise feed-forward.

Каждый подслой обёрнут в residual + LayerNorm.

**Выход.** Линейный слой $W^{\text{out}} \in \mathbb{R}^{d \times |V|}$ проецирует выход верхнего декодера в логиты по словарю; softmax даёт распределение $p(\text{токен})$ на каждой позиции. На обучении считается cross-entropy относительно one-hot целевого распределения; на инференсе токен выбирается greedy или через beam search.

## Why it works

Каждый компонент решает свою задачу, и вместе они закрывают слабости предшественников:

- **Self-attention** даёт $O(1)$ путь между любыми двумя позициями — длинные зависимости больше не размываются по цепочке.
- **Multi-head** позволяет одному слою параллельно представлять разные типы отношений.
- **Positional encoding** ломает permutation equivariance — без него self-attention видит множество, а не последовательность.
- **Residual-связки** дают градиентам прямой путь через стэк глубиной 6+ слоёв; без них трансформер не сходится.
- **LayerNorm** нормализует активации по последней оси, удерживая их в зоне, где softmax и нелинейности дают приличные градиенты.
- **Cross-attention** — мост между энкодером и декодером, заменяющий сжатие всего входа в одно состояние (как у seq2seq RNN с attention или без).
- **Causal masking** в декодере делает обучение параллельным, сохраняя авторегрессионное свойство на инференсе.

Параллелизм — главное практическое следствие: вся последовательность обрабатывается в один forward pass на GPU, и обучение масштабируется на крупные модели и большие батчи.

## Properties

- **Complexity:** self-attention — $O(L^2 \cdot d)$ времени и памяти на скор-матрицу, $O(L \cdot d^2)$ — на проекции. Доминирует $L^2$ на длинных контекстах.
- **Hyperparameters:** глубина $N$, размерность $d$, число heads $h$, скрытая размерность FFN $d_{\text{ff}}$, dropout, warmup-расписание learning rate, регуляризация label smoothing.
- **Failure modes:** без warmup'а и Adam с правильным расписанием обучается плохо; глубокие стэки чувствительны к Pre-LN vs Post-LN порядку (оригинал — Post-LN, современные обычно Pre-LN ради стабильности); квадратичная стоимость attention ограничивает длину контекста.

## Variants and successors

- **Encoder-only (BERT, RoBERTa, DeBERTa).** Только энкодерный стек, без cross-attention и без causal masking. Обучается на masked language modelling. Используется для классификации, retrieval, представлений.
- **Decoder-only (GPT, LLaMA, Mistral).** Только декодерный стек, без cross-attention. Все слои с causal masking, обучение — next-token prediction. Текущий стандарт для LLM.
- **Encoder-decoder с улучшениями (T5, BART).** Та же структура, что у оригинала, но другие задачи претренинга и часто шаринг параметров.
- **Vision Transformer (ViT).** Тот же encoder, токены — патчи изображения; [[methods/positional/rope|RoPE]]-варианты для 2D позиций.
- **Современные attention-замены.** Linear attention, FlashAttention, Mamba (selective state-space) — атакуют именно $O(L^2)$ узкое место.

## Sources

- [[sources/illustrated-transformer]] — пошаговая визуальная сборка архитектуры: стэк энкодеров и декодеров, поток тензоров между ними, residual+LayerNorm, финальный линейный + softmax.

## Up next

- [[topics/transformers]] — narrative-вход в область: от мотивации до архитектуры и её современных потомков.
- [[ml_concepts/attention/self-attention]] — главный механизм, без которого трансформер не работает.
