---
name: write-russian
description: Rules for writing clear human Russian prose on the ML wiki. Covers tone, sentence rhythm, anti-AI patterns, anglicism replacement, term introduction with analogies, formatting, and an editing checklist. Apply when writing or rewriting any Russian wiki page — concept, method, topic, source, question. Trigger phrases — "write russian", "напиши на русском", "перепиши на русском", "проверь стиль".
---

# write-russian — How to write clear Russian prose on the wiki

This is a self-contained style guide. Apply every time you produce Russian text for a wiki page (under `wiki/{ml_concepts,math_concepts,methods,topics,sources,questions}/`). It does **not** apply to code, identifiers, commit messages, headings, slugs, or frontmatter — those stay English per `.claude/rules/01-language-policy.md`.

The rules are written for AI assistants and human authors. Each rule states the principle, gives a banned example, and shows the replacement.

---

## 1. Audience assumption

Write for an **adult reader (20-45 years old)** who:

- Reads in chunks of 15-30 seconds, scans before reading
- Has university-level Russian but no special tolerance for academic, bureaucratic, or corporate phrasing
- Spots AI-generated prose instantly and stops reading
- May or may not have technical background — never assume jargon is shared

Tone is **"a knowledgeable friend explaining a thing"**, not "a lecturer", not "a copywriter", not "a textbook". Use **"вы"** (not "ты") — formal-friendly distance.

---

## 2. Sentence-level rules

### 2.1 Short paragraphs

- **2-4 sentences per paragraph.** One idea = one paragraph.
- Empty line between paragraphs.
- If you wrote a 6-sentence paragraph, split it — you have two ideas, not one.

### 2.2 No trailing period on the last sentence of a paragraph

The last sentence of any paragraph does **not** end with a period. Periods only between sentences inside the same paragraph. Bullet-list items also have no trailing period.

```
❌ Линейная регрессия — простейшая модель. Её используют как baseline.
✅ Линейная регрессия — простейшая модель. Её используют как baseline
```

This is a stylistic convention that improves visual flow when paragraphs are short. If your target medium requires standard punctuation (formal documents, books), drop this rule.

### 2.3 Em-dash budget — use sparingly

Russian uses `—` (em-dash) as legitimate punctuation, but AI generators overuse it. Limit to **≤ 3 em-dashes per ~700 words**.

Before writing an em-dash, ask: would a **comma**, **"и"/"а"/"но"/"поэтому"**, or **sentence split** work? Use em-dash only when those alternatives genuinely hurt clarity (parenthetical that would be clumsy with commas, sharp clause break that a period would flatten).

**Em-dashes in list-item definitions, blockquote pull-outs, and inline code don't count against the budget.** Hyphens in compound words (`какой-то`, `веб-сервис`) are always fine.

### 2.4 Avoid the «X, — Y» parsing trap

Russian em-dash separates subject from predicate: «Главная проблема — отсутствие данных». But when the **subject already has its own verb**, sticking «, — » before another verb produces parsing ambiguity that reads as garbled:

```
❌ Главная причина, по которой машина не заводится зимой, — садится аккумулятор
✅ Чаще всего машина не заводится зимой не из-за бензина, а потому что садится аккумулятор
```

Rule: if the subject clause already contains a verb, restructure instead of forcing an em-dash pivot.

### 2.5 Mix sentence lengths

If three sentences in a row are all 18-22 words, that's AI rhythm. **Vary**: a 5-word fragment + a 30-word period + a 12-word statement.

Not every sentence needs a subordinate clause. **Subject + verb + object** without a `который`-clause is fine and often better. Simple sentences are normal Russian — they're not "primitive".

### 2.6 No `который`-cascades

Two `который / которая / которое` in one sentence → rewrite. The same goes for participial cascades (`занимающийся X, использующий Y, и...`) and 4+ deep genitive chains («процесс улучшения качества подготовки специалистов»).

```
❌ Процесс улучшения качества подготовки специалистов, занимающихся обработкой данных
✅ Учим аналитиков данных лучше
```

Restructure as **verbs**.

### 2.7 No empty hedge words

Delete on sight unless they serve a real purpose:

- «очевидно», «как известно», «безусловно», «несомненно», «конечно же»
- «в целом», «в принципе», «как правило»
- «практически» (as fake hedge — keep when it means «почти 100%»)
- «следует отметить», «стоит отметить», «нельзя не отметить»

If a claim is true, prove it with a specific number or example — don't insist with «безусловно».

### 2.8 Specifics over vague quantifiers

Replace «различные», «некоторые», «достаточно», «несколько», «многие» with concrete numbers, names, or examples.

```
❌ Несколько крупных городов перешли на эту систему
✅ Москва, Берлин и Сингапур перешли на эту систему
✅ Около 30% городов с населением больше миллиона перешли на эту систему
```

### 2.9 Simple words instead of bureaucratic

| Don't write | Write |
|---|---|
| является / являются | это / [delete the verb] |
| осуществлять / осуществляется | делать / происходит / работает |
| реализовать / реализация | внедрить / делаем |
| представляет собой | это / вот что такое |
| обладает / характеризуется | имеет / показывает |
| демонстрировать | показывать |
| функционировать | работать |
| модифицировать | менять |
| определённый | [specify or delete] |
| способствует | помогает / даёт |
| обеспечивает | даёт / гарантирует |

«Линейная регрессия — модель» beats «Линейная регрессия является моделью». Calque from English «to be» is the most common AI tell.

---

## 3. Anti-AI patterns (synthesise this list during editing)

### 3.1 Banned openers

Instant AI tells. Rewrite or skip.

| Banned | Replacement |
|---|---|
| В современном динамично развивающемся мире | Сейчас / Сегодня / [Skip — open with the actual problem] |
| В условиях глобализации / цифровизации | [Skip — name the actual situation] |
| С развитием технологий | [Skip — what specifically changed] |
| Стоит отметить / Нельзя не отметить / Важно понимать | Запомните / Вот что важно / [State the thing] |
| Безусловно / Несомненно / Конечно же | [Delete] |
| В последнее время наблюдается | Недавно выяснили / Теперь известно |
| Знаете ли вы, что / Задумывались ли вы | [Direct claim with specific number] |

### 3.2 Banned constructions

- **«Не X, а Y» rhetorical pivot.** Reads as cheap motivational rhetoric. State the positive directly.
  - ❌ «Не "прочитал главу", а "разобрался в теме"»
  - ✅ «После каждой главы остаётся понимание темы»
  - A single bare negation without the «а Y» pivot is fine («Книга не заканчивается на последней странице»). The banned form is the explicit two-clause «не X, а Y» pivot, especially with quoted phrases.
- **«Не только X, но и Y».** Same problem, different shell. Drop «не только»: «Ускоряет и трансформирует» beats «не только ускоряет, но и трансформирует».
- **«С одной стороны… с другой стороны».** False symmetric balance. Pick the answer; mention the other side as exception.
- **«Прежде всего, во-первых, во-вторых…» as inline enumeration.** For lists of 3+, use a bullet list. Inline numbering is for 2 items max.
- **Tricolon addiction.** Not every list is exactly 3 items. If you have 2 real reasons, write 2. If 5, write 5. Symmetric threes in every paragraph = AI formula.
- **Smooth-transition addiction.** Every paragraph starting with «Дополнительно», «Кроме того», «Более того», «Тем не менее» = AI glue. Sometimes the topic just changes — start the new paragraph directly.

### 3.3 Banned faux-warmth (strongest AI tell)

Never use:

- «Отлично!», «Прекрасный вопрос!», «Замечательно!» — instructional text doesn't react with delight
- «Надеюсь, это помогло» / «Надеюсь, было полезно» — ChatGPT-answer outro
- «С удовольствием расскажу» / «Приглашаю вас» — fake engagement
- «Великолепно работает», «потрясающе быстро» — superlatives without numbers. Replace with specifics («в 15 раз быстрее») or delete.
- «Давайте разберёмся вместе» more than once per topic — AI formula
- «Как видим / как видите» 2+ times in a piece — narrator-assistant voice. Use «Заметьте» or just show without commenting.

### 3.4 Banned phantom citations

«Эксперты считают», «специалисты утверждают», «согласно исследованиям», «как отмечают аналитики» **without a concrete source** = AI hallucination tell. Either name the source («исследование MIT 2024 показало») or drop the framing and state the fact directly.

«Доказано наукой» / «подтверждено многочисленными исследованиями» — never.

### 3.5 Banned vocabulary (corporate / AI bloat)

Already covered partially in §2.9, plus:

| AI word | Human alternative |
|---|---|
| участвует в процессе | работает / делает |
| демонстрирует эффективность | работает / показывает результат |
| множество / большое количество | много / десятки / [concrete number] |
| на протяжении (без даты) | за / в течение |
| в полной мере | полностью / совсем |

### 3.6 Hedge cascade

«В целом, можно сказать, что в большинстве случаев, как правило, это улучшает результаты, хотя есть исключения» — three or more hedges in one sentence = delete all but one. **Max one hedge per claim.**

### 3.7 Header phrasing — descriptive, not metaphoric

Banned in H3/H4 and as paragraph-opening lines:

- «Один ключевой нюанс», «Главный секрет», «Самое интересное»
- «Теперь второй сюжет —», «Перейдём к следующему акту», «А вот и поворот»
- «На самом деле…», «Хитрость в том, что…»

Headers describe content in nominative form:

- ❌ «Один ключевой нюанс — масштаб»  → ✅ «Чувствительность к масштабу признаков»
- ❌ «Теперь второй сюжет — регуляризация» → ✅ «Регуляризация: L1 и L2»

### 3.8 Math-textbook phrasing — rewrite in plain Russian

Constructions like «выход функции, число из интервала $(0,1)$, интерпретируется как вероятность» read as a math textbook, not as an explanation. Triggers to rewrite:

- «из интервала $(a, b)$» → «от $a$ до $b$»
- «принадлежит множеству $\{0, 1\}$» → «равно 0 или 1»
- «интерпретируется как» → «мы трактуем как» / «это»
- «при условии что» (in normal prose, not a formal theorem) → «если» / «когда»
- «функция, отображающая X в Y» → «функция, которая берёт X и возвращает Y»

This rule applies to **explanatory prose** — leave it intact inside formal mathematical statements.

---

## 4. Tone register: «друг, который объясняет»

### 4.1 Conversational connectives

- «давайте разберёмся», «обратите внимание», «мы с вами»
- «не пугайтесь, это проще, чем кажется»
- «представьте», «допустим», «вот пример»

Use questions before revealing answers: «Что произойдёт, если...?» — then explain.

### 4.2 Slow and patient

Walk through complex ideas step by step. Never say «как вы уже знаете» about something introduced a paragraph ago — the reader may have skimmed.

### 4.3 Allowed informalisms — sparingly

A **single colloquial particle per major section**: «же», «ведь», «всё-таки», «короче», «в общем». One per section is texture; two is a tonal slip.

Domain slang in moderation — if your text targets a specific community (developers, gamers, designers, drivers, cyclists), one or two community-specific terms per section add texture. **One such word per major section.** Three in one paragraph = rewrite.

### 4.4 Banned juvenile slang and memes

Never: «АУФ», «база», «кринж», «реально», «прикольно», «топчик». Friendly ≠ teen. The audience is 20-45 adults.

### 4.5 No emoji in prose

Emoji only as `❌` / `✅` markers when contrasting wrong vs right. No 😊, 🚀, 💡, 🎉 in body text — it reads as corporate-cheerful or chatbot.

### 4.6 Humanisation moves on the wiki

Apply 1-2 humanisation moves per major section. Concrete options for wiki context:

1. **Specific numbers instead of vague.** «За 3 эпохи» beats «через несколько эпох». «50 000 строк» beats «много данных». «mAP +3.2 над предыдущим SOTA» beats «значительное улучшение».
2. **Concrete numerical example mid-explanation.** Replace abstract algebra with a worked example using small concrete values: «возьмём $d_k = 4$, $q = (1, 0, 0, 0)$, посмотрим что получится в softmax».
3. **Cite the source explicitly, not vaguely.** Instead of «эксперты утверждают» or «известно, что» — link to `[[sources/<page>]]` or name the paper inline: «Su et al. (2021) показали…».
4. **Rhetorical question with deferred answer.** «Что произойдёт, если убрать $\sqrt{d_k}$ из формулы? Получим взрыв softmax — рассмотрим ниже». Then answer in the next paragraph.
5. **One colloquial particle per section** (see 4.3) — sparingly, only where the prose feels too dry.

Wiki note — author voice. The wiki is not a blog; «по моему опыту» / «у меня в проекте» constructions don't fit. Voice comes from selection of which source to trust, what to flag as contested, what to skip — not from inserting first-person experience claims.

---

## 5. Term introduction (define on first mention)

### 5.1 The format

Any term that isn't general-language Russian — programming jargon, web/network terms, tooling concepts, data-format names — gets a **one-line definition + analogy** on first mention:

> **`<термин>`** (`<English original>`, if relevant) — это `<когда применяется>`. Можно представить как `<аналогия из обычной жизни>`: `<один-два штриха конкретики>`.

Example for `API`:

> **API** (Application Programming Interface) — это правила, по которым одна программа просит у другой данные или действия. Можно представить как **окошко в МФЦ**: вы подаёте заявление по форме, окошко в ответ выдаёт справку. Внутри здания работают сотрудники с базами и принтерами, но вам это не видно — вы видите только окошко и форму.

### 5.2 Rules for analogies

- **One analogy per term.** Pick the closest fit and stop. Don't pile three.
- **Analogy from everyday adult experience**, not engineering: post office, library, customs, lab notebook, train timetable, restaurant ticket, contract, electric kettle.
- **Avoid analogies that need their own analogy.** «Это как middleware в веб-фреймворке» — if the analogy needs explaining, it failed. Pick a non-technical one.
- **After first mention, use the term plainly.** No need to re-analogize. The rule is about onboarding, not running glossary.

### 5.3 Once-only discipline across a piece

Each technical term / library / anglicism is explained **once** per piece. After the first mention, use it plainly. Don't re-define `pandas` in chapter 3 if you defined it in chapter 1.

---

## 6. Anglicism replacement

If an English term has a settled Russian equivalent, **write the Russian one**. English is allowed only in parentheses after the first Russian mention.

| Anglicism | Russian equivalent |
|---|---|
| benchmark (in plain prose) | эталон / эталонный замер |
| warm-up | разминка |
| mental-model | шпаргалка / схема мышления |
| seductive details | избыточные подробности |
| highlight (как глагол) | выделить / подчеркнуть |
| feedback (в смысле «отзыв») | обратная связь / отзыв |
| deadline | срок |
| meeting / митинг | встреча / совещание |
| issue (про неисправность) | проблема / неполадка |
| update (как существительное в обычной прозе) | обновление / новость |
| flow (UX/process sense) | флоу — «пользовательский флоу», «флоу регистрации» |
| thread (OS sense) | поток — keep "поток" for OS threads only, never for UX flow |

### When English is allowed

- In parentheses after first Russian mention: «обратная связь (feedback)». After that — only Russian.
- In code: variable names, method names, library names always stay English.
- URLs, library names, commit messages: English.
- **Terms with no good Russian equivalent stay as-is.** Examples from your own domain: any technical term that's entered Russian lexicon firmly enough that translating it creates more confusion than it solves — `email`, `браузер`, `смартфон`, `сериал`, `подкаст`, `стартап`, `бренд`, `тренд`. Keep your domain's settled borrowings; replace only the ones where a clean Russian equivalent already exists in everyday speech.

### Why this matters

Non-technical Russian readers parse anglicisms-without-Russian-equivalent as **noise**. Native Russian phrasing lowers cognitive load. Authors writing AI-translated texts overuse calques; this rule reverses it.

---

## 7. Punctuation specifics

### 7.1 Russian quotes — «ёлочки» as default

Use **« »** for outer quotes and **„ "** for nested. Reserve straight ASCII `"..."` for code blocks and tokens that must stay machine-parseable.

```
✅ Он сказал: «Мы запустили проект „Альфа"»
❌ Он сказал: "Мы запустили проект 'Альфа'"
```

### 7.2 No period after closing quote with `?` or `!`

A closing quote with `?` or `!` already terminates the sentence. A trailing period is grammatically redundant.

```
❌ «вопрос?».
✅ «вопрос?»

❌ «крик!».
✅ «крик!»
```

A comma after `?»` is fine when the sentence continues: «„Вопрос?", спросил он» — keep the comma.

### 7.3 «не» before nouns — separate word, not hyphenated

Russian writes «не» as a separate word before a noun. The hyphenated form reads as a calque from English.

```
❌ не-технарю / не-разработчику
✅ не технарю / не разработчику
```

Hyphens in proper compound words (`какой-то`, `интернет-провайдер`) are fine.

### 7.4 «На пальцах» — only with speech verbs

The idiom «на пальцах» means «in simple terms». It combines with speech verbs only: «опиши на пальцах», «объясни на пальцах», «расскажи на пальцах», «разбери на пальцах». **Never with «напиши»** — «напиши на пальцах» is a calque from English `write it out simply` and grates on a Russian ear.

```
❌ Напиши на пальцах, как работает X
✅ Опиши на пальцах, как работает X
✅ Объясни на пальцах, как работает X
```

---

## 8. Lists and enumeration

### 8.1 Bullet lists for 3+ items

When the text says «there are N reasons» or «N benefits», render them as a bullet list. Inline «во-первых, во-вторых, в-третьих» works for 2 items max — three is already harder to scan.

Format: each item opens with `**Термин:**` followed by a one-sentence explanation.

```markdown
- **Скорость:** запросы выполняются за миллисекунды
- **Стоимость:** не нужно держать собственный сервер
- **Гибкость:** легко переключиться на другого провайдера
```

### 8.2 ≤ 7 items per list

Miller's 7±2. Bigger lists → split into sub-groups, or move content into a separate section.

### 8.3 No trailing periods on bullet items

Bullet list reads as a list of labels, not sentences. Terminal dots look pedantic and visually break the column.

### 8.4 No checkbox syntax (`- [ ]`)

Most rendering systems show `[ ]` literally. For self-check lists use plain bullet items.

---

## 9. Code and prose interaction (when writing technical content)

This section applies only when the text contains code blocks. Skip if you're writing non-technical prose.

### 9.1 Prose-first

- **Code without surrounding prose is noise.** Default mode is **prose explaining ideas**, not a code dump.
- **Before every code block:** 2-3 sentences setting up *why* this code is about to appear.
- **After every code block:** 1-2 sentences walking through what happened.
- **Banned pattern:** «Вот пример:» + code. Always write a real motivating paragraph first.

### 9.2 Transitional connectors are fine

After a real 2-3 sentence motivation, finish with a clear handoff: «Рассмотрим на примере:», «Вот как это выглядит:», «Проверим на коде:», «Разберём пошагово:».

### 9.3 Variable names: English. Comments: Russian.

Russian variable names look childish in code and break tooling:

```python
❌ имя = "Алиса"
❌ список_покупок = ["хлеб", "молоко"]

✅ name = "Алиса"               # имя пользователя
✅ shopping_list = ["хлеб", "молоко"]
```

Strings inside `print` and string literals **can** be in Russian — that's user-facing output.

### 9.4 Code block size — 3-10 lines by default

Longer blocks allowed when the structure itself is the point. Prefer staging into smaller pieces with explanations between them.

### 9.5 Inline comments inside long code blocks beat trailing dumps

When a long code block needs per-line explanation, put it as `# comment` next to the line, not in a 6-paragraph «разберём построчно» after the block.

---

## 10. Editing checklist (run before declaring text done)

Apply this checklist as a final pass. Each item maps to a rule above.

**Sentence-level**

- [ ] Paragraphs are 2-4 sentences (§2.1)
- [ ] No trailing period on last sentence of each paragraph (§2.2)
- [ ] Em-dash density ≤ 3 per ~700 words (§2.3)
- [ ] No «X, — Y» parsing traps (§2.4)
- [ ] Sentence lengths vary inside each paragraph (§2.5)
- [ ] No `который`-cascades, no 4+ genitive chains, no participial pileups (§2.6)
- [ ] No empty hedges («очевидно», «безусловно», …) (§2.7)
- [ ] No vague quantifiers without specifics (§2.8)
- [ ] No bureaucratic verbs («является», «осуществляется», …) (§2.9)

**Anti-AI scan**

- [ ] No banned openers (§3.1)
- [ ] No «Не X, а Y» pivots, no «Не только… но и», no tricolon addiction (§3.2)
- [ ] No faux-warmth («Отлично!», «Надеюсь, это помогло») (§3.3)
- [ ] No phantom citations («эксперты считают» without source) (§3.4)
- [ ] No corporate vocabulary (§3.5)
- [ ] No hedge cascades (§3.6)
- [ ] Headers describe content, not promise drama (§3.7)
- [ ] No math-textbook phrasing in plain prose (§3.8)

**Tone**

- [ ] «Вы», not «ты» (§4)
- [ ] At most one informal particle per section (§4.3)
- [ ] No juvenile slang (§4.4)
- [ ] No emoji in body prose (§4.5)
- [ ] 1-2 humanisation moves per section (§4.6)

**Terms**

- [ ] Every new term is bolded + defined + given an everyday analogy on first mention (§5.1, §5.2)
- [ ] After first mention, terms are used plainly (§5.3)

**Anglicisms**

- [ ] Settled Russian equivalent used where available (§6)
- [ ] English in parentheses on first mention only

**Punctuation**

- [ ] Russian quotes (« ») for outer, („ ") for nested (§7.1)
- [ ] No period after `?»` / `!»` (§7.2)
- [ ] «не» separate from following noun (§7.3)
- [ ] «На пальцах» only with speech verbs (§7.4)

**Lists**

- [ ] 3+ items → bullet list (§8.1)
- [ ] ≤ 7 items per list (§8.2)
- [ ] No trailing periods on items (§8.3)

**Code (if applicable)**

- [ ] Every code block has 2-3 sentences of setup before and 1-2 sentences of walkthrough after (§9.1)
- [ ] Variable names English, comments Russian (§9.3)
- [ ] Code blocks ≤ 10 lines by default (§9.4)

---

## 11. Fast grep for self-audit

After writing, run this regex against the text to catch the most common AI tells in one pass:

```bash
grep -i -E "следует отметить|стоит отметить|нельзя не отметить|безусловно|несомненно|давайте разберёмся вместе|надеюсь, это помогло|является|осуществляется|представляет собой|во-первых.*во-вторых.*в-третьих|с одной стороны.*с другой стороны|таким образом|следовательно|эксперты считают|согласно исследованиям|в современном мире|в условиях глобализации" <file>
```

Each match → manual review. Sometimes a banned phrase has legitimate context; the default action is **rewrite**.

---

## 12. Wiki-specific notes and when to deviate

These rules optimise for **explanatory Russian prose meant to be read once and understood** on the wiki. A few wiki-specific carve-outs:

- **Math derivations** in `math_concepts/` may use slightly more formal phrasing — «при условии», «пусть $x \in \mathbb{R}^d$» — to keep precision. Even so, prefer plain Russian where it preserves meaning.
- **Source pages** (under `wiki/sources/`) summarise findings, not opinions — drop §4.6 humanisation moves entirely on source pages; stay strictly objective.
- **Question pages** (under `wiki/questions/`) can ask open questions directly without setup — that's their entire purpose.
- **Quoting from a source** — verbatim quote stays as written, even if the source uses banned constructions. Wrap in blockquote and attribute. Don't rewrite the source's words.

§2.2 (no trailing period at paragraph end) is **advisory** for wiki — existing pages use standard punctuation with periods. Apply §2.2 to new content if you want a consistent stylistic choice across a page; otherwise standard punctuation is acceptable.
