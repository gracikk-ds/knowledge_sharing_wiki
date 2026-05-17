# Language Policy

This rule auto-loads. It applies to all wiki content and skill output.

## Where which language

| Surface | Language |
|---|---|
| Prose body of pages under `wiki/{papers,lectures,clips,knowledge-sharings}` | Russian |
| Frontmatter `title:`, H1 of every wiki page | English |
| Filenames, slugs, tags, `[[wiki-links]]` | English (kebab-case) |
| Service files: `CLAUDE.md`, `AGENTS.md`, `wiki/index.md`, `wiki/log.md`, `.claude/skills/**`, `.claude/rules/**`, `.claude/role.md`, `ONBOARDING.md` | English |
| Section headings inside wiki pages | English |
| Commit messages, PR descriptions | English |

## Russian prose rules

ML and math terms stay English inside Russian prose: flow matching, attention, score matching, KL divergence, posterior, prior, embedding, latent, ELBO, autoencoder, gradient, softmax, dropout, EMA. Do **not** transliterate (`флоу-матчинг`, `постериор`) and do **not** over-translate (`нижняя граница доказательства` for ELBO).

Common words with stable Russian equivalents — «градиент», «вероятность», «распределение», «выборка» — pick whichever reads cleaner in context.

### Term glossing on first introduction

Load-bearing concepts that originate from English papers get **glossed**: the Russian translation is followed by the English original in parentheses **on first mention**. After that, use whichever reads cleaner.

Format:

> длина последовательности (sequence length), длина пути (max path length), остаточная связь (residual connection)

When to gloss:

- The reader would need the English form to look the concept up in papers, code, or other wiki breakdowns.
- The Russian translation alone is ambiguous («длина пути» — путь чего? между чем и чем?). The English form anchors it.
- The term will reappear on the page and you want the reader to recognise it in either form.

When **not** to gloss:

- Pure English terms with no Russian equivalent in use — keep them English: «attention», «softmax», «embedding», «KV-cache». Glossing them with a Russian transliteration is the calque ban below.
- Common words that everyone knows in both forms — «градиент / gradient», «выборка / sample». Pick one and use it.
- Mid-paragraph repetitions of an already-glossed term. Gloss once, then use plain.

Glossing is a **first-introduction tool**, not a verbose habit. If you've glossed three terms in the first paragraph, you're overusing it.

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
