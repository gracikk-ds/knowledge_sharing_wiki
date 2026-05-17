---
title: Linear Attention (and Gated Linear Attention)
type: ml_concept
tags: [attention, transformers, linear-attention, recurrent, ssm]
created: 2026-05-17
updated: 2026-05-17
sources: 1
status: draft
---

# Linear Attention (and Gated Linear Attention)

> Класс attention-схем, в которых softmax-нормировка убирается, и сумма по позициям пересобирается в рекуррентное накопление матричного состояния $S_t = \sum_j v_j k_j^\top$. Это даёт $O(1)$ памяти на шаг инференса вместо растущего [[ml_concepts/kv-cache|KV-кэша]], но взамен теряет точное retrieval softmax-attention. Gated Linear Attention (GLA) добавляет обучаемый forget-gate, контролирующий, сколько прошлого удерживать.

## Motivation

Стандартный [[ml_concepts/self-attention|self-attention]] на каждом шаге считает softmax-веса между текущим запросом и *всеми* прошлыми ключами, потом взвешенно суммирует values. Из-за softmax это «всё против всех», и стоимость растёт квадратично по длине; на инференсе [[ml_concepts/kv-cache|KV-кэш]] растёт линейно по длине, что для очень длинных контекстов становится тяжёлым.

Алгебраическая мысль: что если бы вместо softmax была просто билинейная форма $q^\top k$? Тогда сумму $\sum_j (q_t^\top k_j) v_j$ можно переставить так, чтобы вынести $q_t$ за скобки и собрать всё, что зависит только от прошлого, в одну матрицу:

$$
\mathbf{o}_t = \sum_{j=1}^{t} (\mathbf{q}_t^\top \mathbf{k}_j)\, \mathbf{v}_j = \left(\sum_{j=1}^{t} \mathbf{v}_j\, \mathbf{k}_j^\top\right) \mathbf{q}_t = S_t\, \mathbf{q}_t,
$$

где $S_t = \sum_{j=1}^{t} \mathbf{v}_j \mathbf{k}_j^\top$ — матрица $d_v \times d_k$, аккумулирующая outer products. $S_t$ обновляется рекуррентно: $S_t = S_{t-1} + \mathbf{v}_t \mathbf{k}_t^\top$. Это $O(1)$ работы и $O(d_v d_k)$ памяти на шаг — состояние фиксированного размера, не растущее с длиной. Авторегрессионная генерация становится дешёвой так же, как у RNN.

Проблема: без softmax-нормировки $S_t$ растёт неограниченно — старые $(v_j, k_j)$ накапливаются и в какой-то момент забивают сигнал. Нужен механизм затухания. Gated Linear Attention решает это обучаемым forget-гейтом $G_t$, который поэлементно умножает $S_{t-1}$ перед прибавлением нового outer product. Гейт зависит от текущего токена — модель сама учится решать, сколько прошлого помнить.

На практике линейные attention хуже softmax-attention по точному retrieval (например, найти конкретный токен далеко в контексте) — у $S_t$ ограниченная ёмкость, в отличие от полного KV-кэша. Поэтому современные модели не отказываются от softmax-attention полностью, а строят *гибридные стэки*: чередуют softmax-слои (для точного retrieval) с линейными/SSM-слоями (для дешёвого долгого микшинга).

## Formal description

**Линейная attention без гейта.** Состояние $S_t \in \mathbb{R}^{d_v \times d_k}$ обновляется:

$$
S_t = S_{t-1} + \mathbf{v}_t\, \mathbf{k}_t^\top, \qquad \mathbf{o}_t = S_t\, \mathbf{q}_t.
$$

Память на шаг — $O(d_v d_k)$ независимо от $t$. На обучении то же выражение допускает chunked-parallel реализацию: разбить последовательность на блоки, посчитать частичные суммы внутри блока параллельно, сшить блоки префиксной суммой.

**Gated Linear Attention.** Forget-gate $G_t \in \mathbb{R}^{d_v \times d_k}$ — функция текущего токена (например, sigmoid от линейной проекции $\mathbf{x}_t$):

$$
S_t = G_t \odot S_{t-1} + \mathbf{v}_t\, \mathbf{k}_t^\top, \qquad \mathbf{o}_t = S_t\, \mathbf{q}_t,
$$

где $\odot$ — поэлементное произведение. $G_t$ близко к единице — состояние удерживается; близко к нулю — забывается. Forget-gate структурно ровно тот же, что в LSTM, но работает не на скалярном/векторном hidden state, а на матричном $S_t$.

## Hybrid stacks

Современные модели не выкидывают softmax-attention целиком, а перемежают слои:

```
Layer 1:  [Softmax Attention]  ← полная квадратика, точное retrieval
Layer 2:  [GLA / Mamba-2    ]  ← линейная рекуррентность, дешёвый long-range mixing
Layer 3:  [Softmax Attention]
Layer 4:  [GLA / Mamba-2    ]
  ...
```

Конкретные сборки: Mamba-2 — в Nemotron-H и Falcon H1, DeltaNet — в Qwen3-Next. SSM-слои (Mamba и наследники) — это близкий родственник GLA: то же фиксированное состояние и линейная рекуррентность, но с более структурированной параметризацией перехода.

## Variations and related concepts

- [[ml_concepts/self-attention]] — операция, от которой линейная attention отказывается ради рекуррентности.
- [[ml_concepts/kv-cache]] — растущий кэш softmax-attention; линейная attention заменяет его на фиксированное состояние $S_t$.
- [[ml_concepts/gated-attention]] — другой gating-механизм: гейт на *выходе* softmax-attention, не на рекуррентном состоянии.
- [[ml_concepts/sliding-window-attention]] — параллельная стратегия удешевить long-range: ограничить окно, а не выкинуть softmax.

## Open questions

- Что именно теряется у GLA относительно softmax-attention по точному retrieval, и нельзя ли скомпенсировать это конструкцией forget-gate? Открытый вопрос на стыке экспериментов и теории.
- В гибридных стэках какое оптимальное соотношение softmax/линейных слоёв? И зависит ли оно от типа задачи (next-token vs reasoning vs длинный retrieval)?

## Sources

- [[sources/attention-mechanisms-lecture]] — алгебраическое выведение линейной attention из softmax-attention; рекуррентная форма $S_t = G_t \odot S_{t-1} + v_t k_t^\top$ с forget-gate; описание гибридных стэков с Mamba-2 и DeltaNet в Nemotron-H, Falcon H1, Qwen3-Next.

## Up next

- [[topics/attention-variants]] — место линейной attention в общем спектре современных attention-схем.
- [[ml_concepts/sliding-window-attention]] — альтернативная стратегия удешевить attention на длинных последовательностях.
