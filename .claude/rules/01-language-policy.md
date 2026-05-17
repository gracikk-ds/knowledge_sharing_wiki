# Language Policy

This rule auto-loads. It applies to all wiki content and skill output.

## Where which language

| Surface | Language |
|---|---|
| Prose body of pages under `wiki/{ml_concepts,math_concepts,methods,topics,sources,questions}` | Russian |
| Frontmatter `title:`, H1 of every wiki page | English |
| Filenames, slugs, tags, `[[wiki-links]]` | English (kebab-case) |
| Service files: `CLAUDE.md`, `AGENTS.md`, `wiki/index.md`, `wiki/log.md`, `.claude/skills/**`, `.claude/rules/**`, `.claude/role.md`, `ONBOARDING.md` | English |
| Section headings inside wiki pages | English |
| Commit messages, PR descriptions | English |

## Russian prose rules

ML and math terms stay English inside Russian prose: flow matching, attention, score matching, KL divergence, posterior, prior, embedding, latent, ELBO, autoencoder, gradient, softmax, dropout, EMA. Do **not** transliterate (`флоу-матчинг`, `постериор`) and do **not** over-translate (`нижняя граница доказательства` for ELBO).

Common words with stable Russian equivalents — «градиент», «вероятность», «распределение», «выборка» — pick whichever reads cleaner in context.

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
