# Russian Style Guide

Read this in `wiki-ingest` phase 7. Short regulation: `.claude/rules/01-language-policy.md`. This file is the deep guide with examples.

## Voice rules

### Direct, calm, no hype

Bad: «Attention — это революционный механизм, который изменил всё в NLP.»
Good: «Attention оценивает каждый key относительно query и взвешенно агрегирует values.»

### Motivated build-up arc

For every non-trivial concept, the prose follows: what we want → naive approach → why it fails → what the concept introduces.

Bad: «Rotary position embedding кодирует позицию через вращение.»
Good: «От позиционного кодирования хочется одного: чтобы dot-product между Q и K зависел только от относительной позиции m − n, а не от абсолютных m и n. Sinusoidal positional encoding этого свойства не даёт — оно складывает позицию с эмбеддингом аддитивно, и dot-product получает абсолютную позицию через произведение синусов. RoPE решает это, вращая Q и K в каждой парной плоскости на угол, пропорциональный позиции.»

## Banned constructions

### Bureaucratic fillers — never write

- «является» → use direct verb: «X — это Y» or «X делает Z».
  - Bad: «Softmax является функцией, которая нормирует логиты.»
  - Good: «Softmax нормирует логиты в распределение.»

- «представляет собой» → same fix.
  - Bad: «Attention представляет собой взвешенное усреднение.»
  - Good: «Attention — это взвешенное усреднение.»

- «осуществляется» → use active verb.
  - Bad: «Обновление весов осуществляется через backprop.»
  - Good: «Веса обновляются через backprop.»

- «в данной работе / статье / заметке» → drop entirely.
  - Bad: «В данной заметке мы рассмотрим RoPE.»
  - Good: <delete the sentence; the page title carries this info>

- «следует отметить, что» → drop or use «заметим».
  - Bad: «Следует отметить, что dot-product зависит от размерности.»
  - Good: «Dot-product зависит от размерности — отсюда множитель √d_k.»

### AI-speak openings — never write

- «давайте разберёмся» / «погрузимся в» → start directly.
- «как мы знаем» / «как известно» → drop. If the reader does not know, explain; if they do, no need to say it.
- «итак» / «в заключение» / «подводя итог» → drop. Structure carries this.
- «важно понимать, что» → drop. If it matters, just say it.

### Marketing epithets — never write

- «мощный», «впечатляющий», «революционный», «передовой», «прорывной», «инновационный»
- Replace with a specific claim: «mAP +3.2 над предыдущим SOTA», «в 4 раза быстрее на batch=32 H100».

### Calque anglicisms — replace

| Calque | Standard Russian |
|---|---|
| бэкпропагейтить | обратное распространение |
| энкодить | кодировать |
| декодить | декодировать |
| лосс падает | функция потерь убывает |
| зафайнтюнить | дообучить |
| прелёрненный | предобученный |
| инференс на проде | инференс в проде, либо «inference в продакшене» (выбрать одно и придерживаться) |

### How to render an ML term: 3-tier hierarchy

Short version of the rule, full text in `rules/01-language-policy.md`. Every technical term goes through this decision tree.

**Bucket 1 — stable anglicism. Keep pure English, no translation, no gloss.**

If Russian ML discourse already uses the English form (papers, courses, Telegram/Slack ML-чаты), keep it that way. The reader has met the term in that form and will continue to do so. Translation would be a regression. **Bold** the English form on first mention, give a one-line Russian definition + analogy — but never wrap the term itself in Russian.

| Pure English (default) | Don't write |
|---|---|
| sequence length | длина последовательности (sequence length) |
| max path length | длина пути (max path length) |
| residual connection | остаточная связь (residual connection) |
| positional encoding (PE) | позиционное кодирование (positional encoding) |
| feed-forward network (FFN) | сеть прямого распространения |
| multi-head attention | многоголовое внимание (multi-head attention) |
| masked self-attention | маскированный self-attention |
| layer norm | слой нормализации |
| learning rate, batch size | темп обучения, размер батча |

Starter list of bucket-1 terms (extend as needed):

```
attention, softmax, embedding, layer norm, batch norm, dropout, gradient,
residual connection, positional encoding (PE), sequence length, path length,
max path length, scaled dot-product, multi-head attention, encoder, decoder,
cross-attention, masked self-attention, KV-cache, feed-forward network (FFN),
MLP, tokenization, fine-tuning, scaling laws, learning rate, batch size,
warmup, gradient clipping, label smoothing, weight decay,
flow matching, score matching, diffusion, KL divergence, ELBO,
posterior, prior, latent, autoencoder, EMA, RoPE, ALiBi, FlashAttention
```

**Bucket 2 — translatable but with traceability. Russian + English in parens on first mention only.**

For terms where Russian is the dominant form in discourse **и** показать английский исходник имеет смысл для сверки с папером или кодом. Gloss once, then drop the gloss.

| First mention | After |
|---|---|
| матрица смежности (`adjacency matrix`) | матрица смежности |
| доверительный интервал (`confidence interval`) | доверительный интервал |

If you find yourself in bucket 2 more than 2-3 times per page, you are probably mistranslating bucket-1 terms.

**Bucket 3 — everyday math/ML vocab. Pick one form and stay there.**

Examples: градиент / gradient, выборка / sample, вероятность / probability, нейросеть / neural network, обучение / training, функция потерь / loss function.

**Default to bucket 1 for ML paper breakdowns.**

### Calque anglicisms still banned

Bucket 1 keeps the term in **Latin script form**: `attention`, `residual connection`, `multi-head attention`. A Cyrillic transliteration of an English word («бэкпропагейтить», «энкодить», «зафайнтюнить») — это calque, оно остаётся в баннах ниже. Difference: bucket 1 — `fine-tuning`. Calque — `зафайнтюнить`. Same root, different fate.

## Phase 7 checklist (per page)

```
For each page produced in phase 5:
  [ ] No bureaucratic fillers (grep for: является, представляет собой, осуществляется, в данной, следует отметить, стоит отметить, производится, имеет место)
  [ ] No AI-speak openings (grep for: давайте, погрузимся, итак, в заключение, подводя итог, как мы знаем, как известно, важно понимать, не случайно)
  [ ] No marketing epithets (grep for: мощный, впечатляющий, революционный, передовой, прорывной, инновационный)
  [ ] No calque anglicisms (grep for: бэкпропагейтить, энкодить, декодить, лосс падает, зафайнтюнить, прелёрненный, инференс на проде)
  [ ] Load-bearing English-origin terms glossed on first mention (см. «Term glossing» выше)
  [ ] Every non-trivial claim has motivated build-up or links to source
  [ ] Math goes in LaTeX, not backticks
  [ ] Illustrations attached to text, not floating ("вот картинка, разбирайся" — fix)
```

If a check fails, fix in place. Do not commit a page with a known violation.
