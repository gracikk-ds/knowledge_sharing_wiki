---
title: Transformers
type: topic
tags: [attention, transformers, seq2seq, encoder-decoder]
created: 2026-05-17
updated: 2026-05-17
sources: 2
status: draft
---

# Transformers

> Архитектура, заменившая рекуррентные и свёрточные sequence-модели на стэк attention-блоков. От self-attention и multi-head до полной encoder-decoder сборки с positional encoding, residual-связками, masked self-attention и cross-attention.

## The setting

К 2017 году seq2seq задачи — машинный перевод, суммаризация, генерация — решались RNN/LSTM-моделями с attention поверх рекуррентного скрытого состояния (Bahdanau, Luong). У этой линии было два упрямых ограничения. Первое — последовательность шагов: скрытое состояние на позиции $t$ нельзя вычислить, не вычислив сначала $t-1$, и обучение плохо распараллеливается на GPU. Второе — путь от далёких токенов: чтобы информация с позиции $1$ дошла до позиции $L$, она должна пройти через $L$ перезаписей и обычно теряется по дороге.

Vaswani et al. (2017) предложили выкинуть рекуррентность и свёртку и построить модель целиком из self-attention. Self-attention соединяет любые две позиции за одну операцию и параллелится внутри слоя — оба ограничения снимаются разом. Архитектура получила название Transformer, выиграла у Google NMT на WMT-задачах и через несколько лет стала фундаментом всей современной языковой и мультимодальной NLP/CV: BERT, GPT, T5, ViT, Whisper, LLaMA — всё это варианты той же сборки.

Дальше — как Transformer устроен внутри и какие именно идеи делают его работающим.

## Core ideas

[[ml_concepts/self-attention]] — главный механизм. Каждый токен формирует три проекции эмбеддинга — query, key, value. Скор пары $(m, n)$ — скалярное произведение $q_m^\top k_n / \sqrt{d_k}$, softmax по строке даёт распределение веса, выход — взвешенная сумма value-векторов. Слой видит весь контекст за одну операцию, параллелится по позициям и имеет фиксированное число параметров независимо от длины. Без позиционного сигнала self-attention — функция от множества, а не от последовательности.

[[ml_concepts/positional-encoding]] — отдельный сигнал, который ломает permutation equivariance. В оригинальном трансформере используется [[methods/sinusoidal-position-encoding|sinusoidal PE]]: синусы и косинусы от позиции с геометрически разнесёнными частотами, прибавляются к токенному эмбеддингу до проекций. Современные модели чаще используют [[ml_concepts/rotary-position-embedding|RoPE]] — мультипликативную схему, в которой относительная зависимость встроена в геометрию attention; см. [[topics/positional-encoding]] для полной картины.

[[ml_concepts/multi-head-attention]] — параллельный запуск $h$ независимых self-attention блоков с уменьшенной внутренней размерностью $d_k = d / h$. Без него одно distribution attention'а часто доминируется самотокеном и не может одновременно представлять разные типы зависимостей (антецедент, модификатор, синтаксис). С multi-head heads специализируются и объединяются проекцией $W^O$.

[[ml_concepts/causal-masking]] — модификация self-attention, в которой скоры для будущих позиций обнуляются заменой на $-\infty$ до softmax. Нужна, чтобы при параллельном обучении декодер сохранял авторегрессионное свойство: позиция $m$ видит только $1, \ldots, m$.

[[ml_concepts/cross-attention]] — обобщение self-attention на два потока: $Q$ из одной последовательности, $K, V$ из другой. В трансформере — мост между декодером и энкодером: декодер на каждом блоке прямо «спрашивает» энкодер о входе.

## Methods that grow from these ideas

[[methods/transformer]] — оригинальная архитектура (Vaswani et al., 2017). Стэк из 6 идентичных энкодерных блоков (self-attention + FFN) и 6 идентичных декодерных блоков (masked self-attention + cross-attention + FFN), residual + LayerNorm вокруг каждого подслоя, sinusoidal PE на входе. Финальный линейный слой проецирует в логиты по словарю; softmax даёт распределение. Параллелизм по позициям внутри слоя — главное практическое преимущество.

С 2018 года из этой сборки вырастают три семейства:

- **Encoder-only (BERT, RoBERTa, DeBERTa).** Только энкодерный стек, без cross-attention и причинной маски. Обучается на masked language modelling. Сильно в классификации, retrieval, эмбеддинг-задачах.
- **Decoder-only (GPT, LLaMA, Mistral, Claude, Gemini).** Только декодерный стек, без cross-attention. Все слои с causal masking, обучение — next-token prediction. Стандарт для современных LLM.
- **Encoder-decoder с улучшениями (T5, BART, mT5).** Та же структура, что у оригинала, но другие задачи претренинга и часто шаринг параметров.

Параллельно идут две линии оптимизаций. Первая — масштабирование контекста через позиционные схемы: [[topics/positional-encoding]] описывает переход от sinusoidal PE к RoPE и его расширениям (PI, NTK-Aware, YaRN, DyPE). Вторая — атака на $O(L^2)$ узкое место self-attention и на [[ml_concepts/kv-cache|KV-кэш]]: целое семейство attention-вариантов разбирается в отдельном primer'е [[topics/attention-variants]]. Коротко: MQA/GQA/MLA жмут множитель «heads» в кэше, [[ml_concepts/sliding-window-attention|SWA]] и dual chunk attention режут квадратику по длине, [[ml_concepts/linear-attention|linear attention]] и SSM (Mamba-2, DeltaNet) меняют softmax на рекуррентное состояние, FlashAttention переписывает scoring через IO-aware tile-кернел, [[ml_concepts/gated-attention|gated attention]] подавляет attention sinks, [[ml_concepts/document-masking|document masking]] чистит границы между документами на длинных контекстах.

## Open threads

- Pre-LN vs Post-LN: оригинал использует Post-LN ($\mathrm{LayerNorm}(x + \mathrm{Sublayer}(x))$); современные модели переходят на Pre-LN ради стабильности на больших глубинах. Что именно ломается в Post-LN при $N \gg 6$?
- Почему [[ml_concepts/grouped-query-attention|GQA]] с малыми группами не только догоняет MHA, но *обгоняет* её на HellaSwag/MMLU/ARC? Это эмпирическое наблюдение без механистического объяснения. (Сама поверхностная формулировка «MQA/GQA теряют немного качества» оказалась неточной — GQA выигрывает.)
- Линейные attention-приближения теоретически решают $O(L^2)$, но плохо догоняют softmax-attention по точному retrieval. Что именно теряется в выразительности при замене softmax на ядро, и какое соотношение softmax/линейных слоёв в гибридных стэках (Nemotron-H, Falcon H1, Qwen3-Next) оптимально?

## Reading order (recap)

1. [[ml_concepts/self-attention]]
2. [[ml_concepts/positional-encoding]]
3. [[ml_concepts/multi-head-attention]]
4. [[ml_concepts/causal-masking]] → [[ml_concepts/cross-attention]]
5. [[methods/transformer]]
6. Далее — варианты (BERT/GPT/T5; стабы пока не созданы), современные attention-схемы ([[topics/attention-variants]]) и позиционные ([[topics/positional-encoding]]).

## Reading queue

- Vaswani et al., «Attention Is All You Need» (2017) — оригинал архитектуры; пока ингестирован только через [[sources/illustrated-transformer]].
- Harvard NLP, «The Annotated Transformer» (2018) — PyTorch-реализация оригинала с пояснениями.
- Devlin et al., «BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding» (2018).
- Radford et al., «Improving Language Understanding by Generative Pre-Training» (2018) — GPT-1.
- Raffel et al., «Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer» (2019) — T5.
- Dosovitskiy et al., «An Image is Worth 16x16 Words» (2020) — ViT.
- Dao et al., «FlashAttention» (2022) — IO-aware реализация attention.

## Sources

- [[sources/illustrated-transformer]] — визуальный разбор Vaswani 2017 архитектуры: энкодер/декодер стэки, поток тензоров, self-attention пошагово, multi-head, positional encoding, residual+LayerNorm, masked + cross-attention в декодере, финальный linear+softmax.
- [[sources/attention-mechanisms-lecture]] — современные attention-варианты (MQA, GQA, MLA, gated, GLA/hybrid) и long-context-паттерны (SWA, dual chunk, doc masking); KV-кэш как организующий bottleneck. Использован для обновления open threads и ссылки на primer [[topics/attention-variants]].
