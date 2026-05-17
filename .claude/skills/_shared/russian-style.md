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

### What stays English inside Russian prose

ML/math terms with stable English form, no good Russian equivalent:
- flow matching, score matching, attention, KL divergence
- posterior, prior, embedding, latent, ELBO, autoencoder
- gradient, softmax, dropout, EMA, RoPE, FlashAttention

Do **not** transliterate (`флоу-матчинг`, `постериор`). Do **not** over-translate (`нижняя граница доказательства` for ELBO).

### Term glossing: when to show English in parens

Russian translations of English-origin concepts can be ambiguous on their own. «Длина последовательности» — длина в чём, в токенах, в символах, в секундах звука? «Длина пути» — путь чего, между чем и чем? The fix is to gloss the term with its English original on first mention.

| First mention | After |
|---|---|
| длина последовательности (sequence length) | длина последовательности |
| длина пути (max path length) | длина пути |
| остаточная связь (residual connection) | остаточная связь, либо просто residual |
| коэффициент масштабирования (scaling factor) | коэффициент масштабирования |
| свёрточный слой с ядром $k$ (convolutional layer, kernel $k$) | свёртка с ядром $k$ |

When **to** gloss:

- Reader will need the English form to grep papers, code, or other wiki breakdowns.
- The Russian translation is load-bearing for the explanation and could be misread.
- The term reappears further down — glossing once locks the mapping.

When **not** to gloss:

- Term has no stable Russian translation in use — keep it pure English: «attention», «softmax», «embedding», «KV-cache». Glossing «внимание (attention)» reads like Wikipedia.
- Term is shared everyday math vocabulary — «градиент», «вероятность», «производная». Both forms are equally readable; pick one.
- Mid-paragraph repetitions of an already-glossed term. Once is enough.
- Pure mathematical objects defined right under a formula. The `где: ...` list does the job.

Glossing is a **first-introduction tool**. If three consecutive sentences each carry a gloss, you are mistranslating English in Cyrillic — switch to the pure English form for some of them.

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
