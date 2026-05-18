# Language Policy

This rule auto-loads. It applies to all wiki content and skill output.

## Where which language

| Surface | Language |
|---|---|
| Prose body of pages under `wiki/{papers,lectures,clips,knowledge-sharings}` | Russian |
| Frontmatter `title:`, H1 of every wiki page | English |
| Filenames, slugs, tags, `[[wiki-links]]` | English (kebab-case) |
| Service files: `CLAUDE.md`, `AGENTS.md`, `wiki/index.md`, `wiki/log.md`, `.claude/skills/**`, `.claude/rules/**`, `.claude/role.md` | English |
| Section headings inside wiki pages | English |
| Commit messages, PR descriptions | English |

## Russian prose rules

ML and math terms stay English inside Russian prose: flow matching, attention, score matching, KL divergence, posterior, prior, embedding, latent, ELBO, autoencoder, gradient, softmax, dropout, EMA. Do **not** transliterate (`флоу-матчинг`, `постериор`) and do **not** over-translate (`нижняя граница доказательства` for ELBO).

Common words with stable Russian equivalents — «градиент», «вероятность», «распределение», «выборка» — pick whichever reads cleaner in context.

### How to render an ML term: 3-tier hierarchy

For every technical term decide which of these three buckets it belongs to. This is the practical version of the rule — when in doubt, default to bucket 1 (pure English).

**Bucket 1 — stable anglicism. Pure English, no translation, no gloss.**

The term is the form Russian ML discourse already uses. Russian-language papers, courses, и Telegram/Slack ML-чаты используют именно английский вариант. Перевод выглядел бы натянуто. На первое упоминание делается **bold** + Russian one-line definition + analogy, но сам термин остаётся английским.

Starter list (extend as needed, не предписывающе):

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

**Bucket 2 — translatable but traceability matters. Russian + English in parens on first mention.**

Term has a clean Russian translation that is genuinely used in discourse, **и** ты хочешь, чтобы читатель смог нагуглить английскую форму при сверке с исходником. Gloss один раз, потом используй ту форму, которая в данном предложении читается лучше.

Examples: матрица смежности (`adjacency matrix`), доверительный интервал (`confidence interval`), нижняя оценка правдоподобия (`evidence lower bound`, ELBO — though ELBO is usually pure English).

**Bucket 3 — everyday math/ML vocab. Pick one form, stick to it.**

Both forms fully natural in Russian and there's no traceability win from showing both. Choose whichever reads cleaner in context.

Examples: градиент / gradient, выборка / sample, вероятность / probability, нейросеть / neural network, обучение / training, функция потерь / loss function.

**Default to bucket 1 for ML papers.** If you find yourself in bucket 2 more than 2-3 times per page, you are probably mistranslating bucket 1 terms.

**This is distinct from calque anglicisms** (banned below). A calque is a Cyrillic transliteration of an English verb («бэкпропагейтить», «энкодить»). Bucket 1 keeps the term in its own Latin script form.

### Banned constructions

**Bureaucratic fillers** — never write:
- «является», «осуществляется», «представляет собой»
- «в данной работе», «в данной статье», «в данной заметке»
- «следует отметить, что», «стоит отметить»
- «производится», «имеет место»

**AI-speak openings** — never write:
- «давайте разберёмся», «погрузимся в»
- «как мы знаем», «как известно», «не случайно»
- «итак», «в заключение», «подводя итог»
- «важно понимать, что»

**Marketing epithets** — never write:
- «мощный», «впечатляющий», «революционный»
- «передовой», «прорывной», «инновационный»

**Calque anglicisms** — replace with standard Russian ML terms:
- «бэкпропагейтить» → обратное распространение
- «энкодить», «декодить» → кодировать, декодировать
- «лосс падает» → функция потерь убывает
- «зафайнтюнить» → дообучить

## Verification (during `wiki-lint`)

Grep prose for any banned construction. Each match is a finding to surface.
