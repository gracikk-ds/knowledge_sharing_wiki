---
title: Multi-Head Attention
type: ml_concept
tags: [attention, transformers, multi-head]
created: 2026-05-17
updated: 2026-05-17
sources: 2
status: draft
needs_rewrite: true
---

# Multi-Head Attention

> Параллельный запуск $h$ независимых [[ml_concepts/self-attention|self-attention]] блоков с собственными $W_Q^{(i)}, W_K^{(i)}, W_V^{(i)}$; выходы $h$ heads конкатенируются по последней оси и проецируются обучаемой матрицей $W^O$. Каждая head работает в своём $d_k$-мерном подпространстве и может специализироваться на своём типе зависимостей.

## Motivation

Одноголовый self-attention выдаёт одно распределение веса $\alpha_{m, \cdot}$ на каждую позицию. На практике это приводит к двум проблемам.

Во-первых, единственное распределение часто оказывается «съедено» самим токеном: $q_m^\top k_m$ обычно велико, и $\alpha_{m, m}$ доминирует над всеми остальными $\alpha_{m, n}$. Полезная информация о соседях задавливается.

Во-вторых, одно распределение не может одновременно представлять разные типы отношений. Слово «it» в предложении «The animal didn't cross the street because it was too tired» одновременно зависит от «animal» (антецедент местоимения) и от «tired» (причина). Если усреднить эти две зависимости в одно распределение, теряется и то, и другое.

Решение: запустить $h$ self-attention блоков параллельно. Каждый имеет свой набор проекций $W_Q^{(i)}, W_K^{(i)}, W_V^{(i)}$, инициализированных независимо. При обучении head'ы расходятся: один может научиться следить за антецедентами, другой — за модификаторами, третий — за синтаксической зависимостью. После их выходы конкатенируются и проецируются обратно в исходную размерность, чтобы интерфейс слоя оставался $\mathbb{R}^d \to \mathbb{R}^d$ и блок можно было стэкать.

Стоимость держится примерно постоянной за счёт того, что внутренняя размерность $d_k$ каждой head уменьшена в $h$ раз: при $d = 512$ и $h = 8$ берут $d_k = 64$. Суммарное число параметров $h \cdot d \cdot 3 \cdot d_k = 3 d^2$ совпадает с одноголовой версией с $d_k = d$, и матричные умножения упаковываются в один батч-вызов.

## KV-cache cost

На инференсе MHA требует хранить $K$ и $V$ для каждой позиции *и каждой head*. Размер [[ml_concepts/kv-cache|KV-кэша]] на одну последовательность:

$$
\text{KV-cache} = 2 \times n_{\text{heads}} \times n_{\text{layers}} \times d_{\text{head}} \times L.
$$

Множитель «$n_{\text{heads}}$» здесь — главный практический недостаток MHA в больших моделях с длинными контекстами: на 70B-модели с $L = 32\text{k}$ кэш легко превышает размер весов. Именно ради сжатия этого множителя появилась целая ветвь вариантов: [[ml_concepts/multi-query-attention|MQA]] делит на $h$, [[ml_concepts/grouped-query-attention|GQA]] — на $h / g$, [[ml_concepts/multi-latent-attention|MLA]] заменяет «$2 \cdot n_{\text{heads}} \cdot d_{\text{head}}$» на одну узкую латентную ширину $d_c$. На современных frontier-моделях чистый MHA в attention-подслое почти не встречается — стандартом стала GQA с 2–8 группами.

## Formal description

Пусть $X \in \mathbb{R}^{L \times d}$ — входная матрица эмбеддингов, $h$ — число heads, $d_k = d / h$ — размерность каждой head (обычно). Для каждой head $i \in \{1, \ldots, h\}$ есть свои проекции $W_Q^{(i)}, W_K^{(i)}, W_V^{(i)} \in \mathbb{R}^{d \times d_k}$. Выход head'а:

$$
Z_i = \mathrm{Attention}(X W_Q^{(i)},\, X W_K^{(i)},\, X W_V^{(i)}) \in \mathbb{R}^{L \times d_k},
$$

где $\mathrm{Attention}$ — стандартный scaled dot-product attention (см. [[ml_concepts/self-attention|self-attention]]).

Конкатенация по последней оси:

$$
Z = [Z_1; Z_2; \ldots; Z_h] \in \mathbb{R}^{L \times (h \cdot d_k)} = \mathbb{R}^{L \times d}.
$$

Финальная обучаемая матрица $W^O \in \mathbb{R}^{d \times d}$ смешивает результаты heads и возвращает выход в исходное пространство:

$$
\mathrm{MultiHead}(X) = Z\, W^O.
$$

Без $W^O$ слой был бы просто склейкой $h$ независимых каналов; $W^O$ даёт обучаемую линейную комбинацию между ними.

## Variations and related concepts

- [[ml_concepts/self-attention]] — базовый механизм; multi-head — это $h$ его параллельных копий с уменьшенной $d_k$.
- [[ml_concepts/cross-attention]] — multi-head применим и к cross-attention, где $Q$ и $K, V$ из разных последовательностей.
- [[ml_concepts/causal-masking]] — маска накладывается одинаково на все heads; параллелизм heads сохраняется.
- [[ml_concepts/multi-query-attention]] — крайний случай: все heads делят одну пару $K, V$; кэш делится на $h$ ценой выразительности.
- [[ml_concepts/grouped-query-attention]] — компромисс: heads делятся на группы, каждая группа делит свой $K, V$. Современный default — обгоняет MHA в ablation'ах при $g = 2$–$8$.
- [[ml_concepts/multi-latent-attention]] — другой путь сжатия кэша: спроецировать вход в латент $c_t$, восстанавливать $K, V$ на лету.
- [[ml_concepts/kv-cache]] — bottleneck, ради которого появилась вся ветвь MQA/GQA/MLA.
- [[methods/transformer]] — multi-head — основной строительный блок и в энкодере, и в декодере.

## Open questions

- Какие конкретно отношения учат разные heads в больших современных моделях? Сохраняется ли наблюдение из ранних разборов (один head — кореференция, другой — синтаксис), или у крупных моделей роли размываются?
- Почему [[ml_concepts/grouped-query-attention|GQA]] с малыми группами не только догоняет MHA, но *обгоняет* её на HellaSwag/MMLU/ARC? Что именно работает как полезная регуляризация при шаринге KV внутри группы? Эмпирически подтверждено, механистически — нет.

## Sources

- [[sources/illustrated-transformer]] — описывает multi-head как способ дать модели «representation subspaces» и снять доминирование самотокена; объясняет роль $W^O$ как проектора конкатенированного результата.
- [[sources/attention-mechanisms-lecture]] — фиксирует MHA как «highest capacity, highest cache» точку спектра MHA → GQA → MQA → MLA; формула KV-кэша; ablation Hugging Face, где GQA-малой-группы обогнала MHA.

## Up next

- [[ml_concepts/grouped-query-attention]] — почему чистый MHA уступил место GQA в современных моделях.
- [[topics/attention-variants]] — общая картина attention-схем вокруг KV-bottleneck'а.
