---
title: Attention Variants
type: topic
tags: [attention, transformers, kv-cache, long-context, inference]
created: 2026-05-17
updated: 2026-05-17
sources: 1
status: draft
---

# Attention Variants

> Современный landscape attention-схем в больших моделях: всё организовано вокруг одного inference-bottleneck'а — KV-кэша. Каждый вариант (MQA, GQA, MLA, gated, linear, SWA, document masking) — это разная точка на трёх осях: память кэша vs выразительность, локальное окно vs глобальный контекст, точное retrieval vs дешёвая рекуррентность.

## The setting

Оригинальный трансформер (Vaswani et al., 2017) определил attention один раз и навсегда: $h$ независимых heads, каждая со своими $W_Q, W_K, W_V$, softmax-нормировка скоров, полное квадратичное внимание $L \times L$. На моделях масштаба 2017 года это работало без оговорок: контексты до сотен токенов, heads исчисляются единицами, KV-кэш не главный потребитель GPU.

К 2024–2025 году картина другая. Frontier-модели имеют десятки слоёв и сотни heads, контексты — десятки и сотни тысяч токенов, и [[ml_concepts/attention/kv-cache|KV-кэш]] стал главным потребителем GPU-памяти на инференсе: его размер $2 \times n_{\text{heads}} \times n_{\text{layers}} \times d_{\text{head}} \times L$ — линеен по всем четырём множителям, и для типичной 70B-модели на 32k контексте легко превышает размер весов. Сколько одновременных запросов помещается в видеокарту — определяется кэшем, не FLOPS.

Параллельно растёт требование к длине контекста. Модели обучают на десятках тысяч токенов, экстраполируют до миллионов. Квадратичная стоимость attention становится практическим препятствием: даже если кэш помещается, $O(L^2)$ scoring при $L = 10^5$ — это $10^{10}$ операций на каждую head на каждом слое.

Эти два давления — KV-кэш и квадратика — породили целый класс модификаций attention. Они не отменяют идею Q/K/V и не заменяют softmax-attention целиком, но систематически режут одну из осей цены. Дальше — как организован этот landscape.

## Core ideas

[[ml_concepts/attention/kv-cache]] — организующий концепт. Размер кэша определяется четырьмя множителями: $2 \cdot n_{\text{heads}} \cdot n_{\text{layers}} \cdot d_{\text{head}} \cdot L$. Каждая модификация attention давит на один из них. На число heads — MQA/GQA/MLA. На длину $L$ — SWA, dual chunk, document masking. На число слоёв — cross-layer sharing (вне разбора этой лекции). Это формирует двумерную картину: «по какой оси режем — сколько режем — какую выразительность теряем».

[[ml_concepts/attention/multi-head-attention]] — точка отсчёта. Каждая head независимо проецирует вход в $Q, K, V$; ничего не шарится. Максимальная выразительность, максимальный кэш. Все остальные варианты — отклонения от этой точки в сторону компрессии.

[[ml_concepts/attention/efficiency/multi-query-attention]] — крайнее сжатие по оси heads: все heads делят одну пару $K, V$. Кэш делится на $n_{\text{heads}}$, но выразительность заметно проседает. Hugging Face ablation подтвердил: MHA побеждает MQA. С тех пор чистый MQA в новых моделях почти не используется.

[[ml_concepts/attention/efficiency/grouped-query-attention]] — промежуточная точка. Heads делятся на $g$ групп (обычно 2/4/8), каждая группа имеет свою пару $K, V$. Сюрприз: малые группы не только догоняют MHA, но и обгоняют его на HellaSwag/MMLU/ARC. Малое KV-шаринг работает как полезная регуляризация. Это переписало позицию GQA из «компромисса» в «новый default». Trinity Large, gpt-oss-120b, SmolLM3, OLMo 3 — все используют GQA.

[[ml_concepts/attention/efficiency/multi-latent-attention]] — другая стратегия сжатия. Вместо шаринга heads — спроецировать вход в низкоразмерный латент $c_t \in \mathbb{R}^{d_c}$, кэшировать его, восстанавливать $K, V$ на лету через обучаемые up-проекции. Даёт 4–8× сжатия с меньшей потерей выразительности, чем агрессивная GQA, ценой кастомных attention-ядер. Выбор DeepSeek и Kimi-K2.

[[ml_concepts/attention/variants/gated-attention]] — ортогональная модификация. Не про кэш и не про длину, а про *устойчивость*. Поэлементный sigmoid-гейт на выход attention учится подавлять [[ml_concepts/attention/attention-sink|attention sinks]] — позиции, аккумулирующие непропорциональный вес без семантической нагрузки. Стабилизирует большие обучения, помогает на длинных контекстах. Очень дешёвая прибавка.

[[ml_concepts/attention/efficiency/linear-attention]] — отказ от softmax ради алгебраического переноса. Сумма $\sum_j (q_t^\top k_j) v_j$ переcобирается в рекуррентное матричное состояние $S_t = \sum_j v_j k_j^\top$, и attention становится $O(1)$ на шаг. Gated Linear Attention (GLA) добавляет forget-gate $S_t = G_t \odot S_{t-1} + v_t k_t^\top$, контролирующий, сколько прошлого удерживать. Точное retrieval хуже, чем у softmax, поэтому реально применяется в *гибридных стэках*: чередовать GLA/Mamba-2-слои с softmax-слоями. Nemotron-H и Falcon H1 (Mamba-2), Qwen3-Next (DeltaNet).

[[ml_concepts/attention/efficiency/sliding-window-attention]] — атака на длину $L$ через ограничение окна. Каждая позиция видит только последние $p$ токенов, маска становится диагональной полосой шириной $p$. Стоимость $O(L \cdot p)$ вместо $O(L^2)$. Без full-attention-слоёв полностью теряет дальний контекст, поэтому обычно перемежается: full через каждые $k$ SWA-слоёв (Gemma 3). Дополнительные варианты — dual chunk attention (Qwen-2.5, контексты до 1M), interleaving local/global.

[[ml_concepts/attention/document-masking]] — другая модификация маски для длинных контекстов. Когда несколько документов pack'нуты в одну обучающую последовательность, document masking запрещает attention пересекать их границы. На коротких контекстах эффект мал; при переходе с 4k на 64k становится обязательным — без него модель учится плохим cross-document шорткатам. SmolLM3 эмпирически подтвердил необходимость для перехода в long context.

## Methods that grow from these ideas

Различные frontier-сборки выбирают разные комбинации:

- **GQA + RoPE/RNoPE.** Default современных dense-моделей. Хорошее KV-сжатие, хорошая совместимость с FlashAttention и стандартным FSDP-шардингом. SmolLM3 (g=4), gpt-oss-120b (g=8), Trinity Large (g=8), OLMo 3.
- **MLA-based.** Когда инференс-память — главный constraint, и команда готова поддерживать кастомные ядра. DeepSeek-V2/V3, Kimi-K2 (384 MoE-экспертов поверх MLA).
- **Hybrid stacks (softmax + linear).** Перемежение softmax-слоёв с GLA/Mamba-2/DeltaNet ради линейной по $L$ части compute. Nemotron-H, Falcon H1, Qwen3-Next.
- **Long-context dense.** Document masking + RNoPE/YaRN + interleaving local/global. SmolLM3 (4k → 64k), Qwen-2.5 (через dual chunk attention до 1M).

С точки зрения «что брать по умолчанию»:

- **Если ничего особенного не нужно** — GQA с 4 или 8 группами + [[methods/positional/rope|RoPE]]. Известный, протестированный, совместим с инструментами.
- **Если инференс-память критична** — MLA. Но реалистично только если есть кадры поддерживать кастомные kernel'ы.
- **Если нужны длинные контексты (64k+)** — document masking обязателен, плюс RNoPE/[[methods/positional/yarn|YaRN]] и interleaving local/global.
- **Gated attention** — добавлять, если беспокоит стабильность обучения. Дёшево.
- **Linear/hybrid** — *не брать* без своих ablation'ов на твоём масштабе и задачах. Сложнее кernel'ы, больше багов.

## Open threads

- **Почему GQA-малой-группы > MHA?** Лекция фиксирует эмпирическое наблюдение, но не даёт механистического объяснения. Это самый интересный открытый вопрос в области.
- **MLA vs GQA в TFLOPS.** В чистой памяти MLA выигрывает, в compute — нет (декомпрессия). Как сравнивать честно — открыто, зависит от профиля инференса.
- **Гибридные стэки.** Какое соотношение softmax/линейных слоёв оптимально? Зависит от задачи (next-token, reasoning, long retrieval)? Сейчас выбирается эмпирически.
- **Длинный контекст и cross-document'ные границы.** Почему document masking резко обязателен именно при переходе 4k → 64k? Плавная зависимость или критическая длина?
- **Attention sinks и gated attention.** Какие именно позиции отключает гейт у обученных моделей? Совпадают ли они с известными sink-токенами?

## Reading order (recap)

1. [[ml_concepts/attention/kv-cache]]
2. [[ml_concepts/attention/multi-head-attention]] → [[ml_concepts/attention/efficiency/multi-query-attention]] → [[ml_concepts/attention/efficiency/grouped-query-attention]] → [[ml_concepts/attention/efficiency/multi-latent-attention]]
3. [[ml_concepts/attention/attention-sink]] → [[ml_concepts/attention/variants/gated-attention]]
4. [[ml_concepts/attention/efficiency/linear-attention]] (с GLA и гибридными стэками)
5. [[ml_concepts/attention/efficiency/sliding-window-attention]] → [[ml_concepts/attention/document-masking]]
6. Назад к [[topics/transformers]] — где attention-варианты живут в общей картине архитектур.

## Reading queue

- Shazeer, «Fast Transformer Decoding: One Write-Head is All You Need» (2019) — оригинал MQA.
- Ainslie et al., «GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints» (2023) — GQA.
- DeepSeek-V2 / DeepSeek-V3 техотчёты — MLA и её обоснование.
- «Mamba-2» (Dao et al., 2024) и «Mamba» (Gu & Dao, 2023) — структурированные SSM, родственники GLA.
- «Gated Linear Attention» (Yang et al., 2024) — GLA как класс.
- «StreamingLLM» / «Sink Token» — практическое использование attention-sinks для эффективного инференса.
- SmolLM3 техотчёт — document masking, long-context-сетап, RNoPE.
- Gemma 3 техотчёт — SWA-interleaving.
