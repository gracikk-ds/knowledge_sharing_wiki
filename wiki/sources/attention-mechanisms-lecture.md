---
title: "Attention Mechanisms (lecture)"
type: source
source_path: raw/lectures/Attention Mechanisms.md
source_kind: lecture
source_date: 2026-02-22
ingested: 2026-05-17
tags: [attention, transformers, kv-cache, mqa, gqa, mla, gated-attention, linear-attention, long-context, sliding-window, document-masking]
sources: 1
status: draft
---

# Attention Mechanisms (lecture)

> Лекция, организующая весь современный landscape attention-вариантов вокруг одного inference-bottleneck'а — KV-кэша. Систематически разбирает спектр MHA → MQA → GQA → MLA с формулой кэша и ablation'ами; добавляет gated attention (против attention sinks), GLA и гибридные стэки (Mamba-2 / DeltaNet в Nemotron-H, Falcon H1, Qwen3-Next); long-context-паттерны (sliding window, dual chunk, local/global interleaving, document masking) с конкретными моделями (Gemma 3, Qwen-2.5, SmolLM3). Сильная сторона — конкретные frontier-сборки (Kimi-K2, Trinity Large, gpt-oss-120b, OLMo 3, DeepSeek) на каждой странице.

## Key takeaways

- **KV-кэш как организующий концепт.** Формула $2 \cdot n_{\text{heads}} \cdot n_{\text{layers}} \cdot d_{\text{head}} \cdot L$ — единственный bottleneck, через который удобно объяснять весь зоопарк вариантов. Каждый variant давит на один из множителей.
- **MHA → MQA → GQA — спектр шаринга KV.** MHA — один KV на head (всё). MQA — один KV на все heads (минимум). GQA — KV на группу heads (компромисс). Hugging Face ablation: MHA побеждает MQA, *но* GQA с группами 2/4/8 *обгоняет* MHA на HellaSwag/MMLU/ARC — KV-шаринг малой группы работает как полезная регуляризация. Поменяло позицию GQA из «компромисса» в «стандарт по умолчанию».
- **MLA — другая стратегия сжатия.** Спроецировать вход в латент $c_t \in \mathbb{R}^{d_c}$, кэшировать его, восстанавливать $K, V$ через обучаемые up-проекции. 4–8× сжатия с меньшей потерей выразительности, чем агрессивная GQA. Реалистично только при наличии команды на кастомные kernel'ы. Выбор DeepSeek и Kimi-K2.
- **Gated attention против attention sinks.** Поэлементный sigmoid-гейт $\sigma(W^G x_t)$ на выход attention учится подавлять стоковые позиции. Дешёвая прибавка для стабилизации больших обучений и long-context-обобщения.
- **Linear attention — алгебраический рефакторинг.** Дроп softmax → сумма пересобирается в рекуррентное состояние $S_t = \sum_j v_j k_j^\top$. $O(1)$ память на шаг. Без normalization $S_t$ растёт неограниченно; GLA фиксирует это forget-гейтом $G_t \odot S_{t-1}$. На практике используется только в гибридных стэках, чередующих softmax и линейные слои (Mamba-2 → Nemotron-H, Falcon H1; DeltaNet → Qwen3-Next).
- **Long-context patterns.** Sliding window attention (Gemma 3) — ограничение окна, $O(L \cdot p)$ вместо $O(L^2)$. Dual chunk attention (Qwen-2.5) — иерархическая маска, контексты до 1M. Local/global interleaving — чередование ограниченных и полных слоёв. Document masking — блочно-диагональная маска для pack'нутых последовательностей; некритично на 4k, обязательно на 64k+ (SmolLM3).
- **Default-сборка.** GQA с 4–8 группами + RoPE/RNoPE. Если нужна максимальная экономия памяти — MLA. Если long context — добавить document masking, RNoPE/YaRN, interleaving local/global. Gated attention — дешёвая прибавка для стабильности. Не брать linear/hybrid без своих ablation'ов на масштабе.

## Concepts touched

- [[ml_concepts/attention/kv-cache]] — **новая страница, главный вклад источника.** Формула размера кэша, четыре множителя, спектр вариантов как способы давить на каждый.
- [[ml_concepts/attention/multi-head-attention]] — добавлен раздел про KV-cache cost; обновлены variations (ссылки на MQA/GQA/MLA/KV-cache); зачищен open question про MQA/GQA (источник его *закрывает*) — теперь там вопрос «почему GQA обгоняет MHA».
- [[ml_concepts/attention/efficiency/multi-query-attention]] — новая страница. Формулы, точка крайнего сжатия, ablation Hugging Face.
- [[ml_concepts/attention/efficiency/grouped-query-attention]] — новая страница. Спектр MHA ↔ MQA, диаграмма, формула кэша, ablation'ы, список frontier-моделей.
- [[ml_concepts/attention/efficiency/multi-latent-attention]] — новая страница. Down/up-проекции, формула кэша $d_c \cdot n_{\text{layers}} \cdot L$, trade-off памяти и compute, DeepSeek и Kimi-K2.
- [[ml_concepts/attention/variants/gated-attention]] — новая страница. Формула $\tilde{o} = o \odot \sigma(W^G x)$, мотивация через attention sinks.
- [[ml_concepts/attention/efficiency/linear-attention]] — новая страница. Алгебраическое выведение, рекуррентная форма, GLA с forget-гейтом, гибридные стэки.
- [[ml_concepts/attention/efficiency/sliding-window-attention]] — новая страница. Маска SWA, формула $O(L \cdot p)$, interleaving с full-attention, Gemma 3.
- [[ml_concepts/attention/document-masking]] — новая страница. Блочно-диагональная маска, эффект на 4k vs 64k, необходимость для long-context-сетапа.
- [[ml_concepts/attention/attention-sink]] — новый стаб. Феномен, на который реагирует gated attention.
- [[topics/attention-variants]] — **новая страница, narrative-вход в всю картину.** KV-кэш как организующий концепт, разбор core ideas в reading order, рекомендации по умолчанию, reading queue с primary sources.
- [[topics/transformers]] — обновлены «Methods that grow from these ideas» (ссылка на новый primer и краткий обзор семейств вариантов), open threads (MQA/GQA-вопрос *закрыт* с поворотом «GQA обгоняет MHA»; добавлены гибридные стэки), reading order и sources.

## Contradictions and revisions

- **Resolved (не контрадикция, но смена позиции).** Open thread в [[topics/transformers]] до этого источника был сформулирован как «MQA/GQA урезают KV и теряют немного качества — почему так мало?». Лекция показывает, что в случае GQA с малыми группами модель *выигрывает* у MHA, а не теряет. Open thread переписан с учётом этого.
- **Resolved open question в [[ml_concepts/attention/multi-head-attention]].** Тот же вопрос про MQA/GQA на странице MHA — заменён на «почему GQA обгоняет MHA». Прежняя формулировка снята.
- Прямых контрадикций с другими страницами вики (positional-encoding, RoPE, transformer и т.п.) нет — лекция расширяет, не пересматривает.

## Questions raised

Лекция не формулирует исследовательских открытых вопросов явно, но рождает несколько естественных, размещённых на соответствующих страницах:

- Почему GQA-малой-группы обгоняет MHA? ([[ml_concepts/attention/multi-head-attention]], [[ml_concepts/attention/efficiency/grouped-query-attention]], [[topics/transformers]], [[topics/attention-variants]]) — самый интересный.
- Как корректно сравнивать MLA и GQA с учётом цены декомпрессии? ([[ml_concepts/attention/efficiency/multi-latent-attention]], [[topics/attention-variants]]).
- Что именно теряется у GLA относительно softmax-attention по retrieval, и какое соотношение softmax/линейных слоёв оптимально в гибридах? ([[ml_concepts/attention/efficiency/linear-attention]], [[topics/transformers]], [[topics/attention-variants]]).
- Почему document masking резко важен при переходе 4k → 64k? ([[ml_concepts/attention/document-masking]], [[topics/attention-variants]]).
- Какие позиции отключает гейт у обученных моделей — совпадают ли они с attention sinks? ([[ml_concepts/attention/variants/gated-attention]], [[topics/attention-variants]]).

Решено не заводить отдельных `questions/` страниц — вопросы естественно живут в Open questions соответствующих концепт-страниц. Могут быть промоутированы при появлении сфокусированного источника.

## Notes

- Лекция содержит ASCII-диаграммы внутри fenced-блоков (KV-spectrum для MHA/GQA/MQA, sliding-window vs causal full, document mask vs causal). Все три скопированы дословно в [[ml_concepts/attention/efficiency/grouped-query-attention]], [[ml_concepts/attention/efficiency/sliding-window-attention]] и [[ml_concepts/attention/document-masking]] соответственно — это лучший способ донести структуру масок/шаринга, и они полностью внутри markdown'а (внешних изображений нет).
- Список конкретных frontier-моделей (Kimi-K2, Trinity Large, gpt-oss-120b, SmolLM3, OLMo 3, DeepSeek, Gemma 3, Qwen-2.5, Nemotron-H, Falcon H1, Qwen3-Next) — сильная сторона источника; перенесены на соответствующие страницы вики для возможности обратного поиска «какие модели используют X».
- В оригинале одна опечатка в LaTeX (`$mathbf{q}_t$` вместо `$\mathbf{q}_t$` в формуле MHA и в формуле размерности латента MLA) — на вики переписано корректно.
- Реальная глубина каждой темы в лекции — обзорная: на каждом варианте достаточно для понимания и сравнения, но без полной деривации и без ablation-чисел. Primary sources перечислены в reading queue [[topics/attention-variants]] для углубления.

## Pointer back to raw

`raw/lectures/Attention Mechanisms.md`
