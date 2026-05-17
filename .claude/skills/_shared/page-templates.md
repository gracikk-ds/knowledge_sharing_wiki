# Page Templates

Read this in `wiki-ingest` phase 5. The wiki has **one canonical template** — Template A (Motivation-first) — used for every paper, lecture, and clip breakdown. Knowledge sharings use a variant with extra frontmatter fields and one optional section. All cross-cutting writing rules (term introduction, formula annotation, code-formula bridge) at the end apply to every template.

---

## Template A — Source breakdown (paper / lecture / clip)

The page belongs in `wiki/{papers,lectures,clips}/<slug>.md` per the slug rules in `rules/04-frontmatter-schema.md`.

```markdown
---
title: <Plain title in English>
source_kind: paper | lecture | clip
source_path: raw/<kind>/<file>
source_date: YYYY-MM-DD
ingested: YYYY-MM-DD
authors: [<First Last>, ...]
tags: [<tag1>, <tag2>, ...]
status: stub | draft | mature
---

# {Plain title}

> {TL;DR — 4-7 sentences in Russian. Five things, in this order:
> 1. Задача, которую решает источник, в одной фразе.
> 2. Что предлагает источник как ответ.
> 3. Один-два конкретных численных результата (BLEU, FID, скорость, FLOPs).
> 4. Контекст: почему до сих пор актуально, или чем уже заменено.
> 5. Что найдёшь в этом разборе (одна короткая фраза).
> Пишется плотно, без воды: за 20-30 секунд читатель решает, нужен ему весь разбор или нет.}

## Мотивация

{2-4 paragraphs of motivated build-up:
1. What we want (from positional encoding, attention, training, etc.).
2. The naive or previous approach.
3. Why it fails — concretely, what's the failure mode.
4. What this source proposes, in one sentence (no details yet).}

## Идея в одной картинке

{The single most important visualisation — mermaid diagram or matplotlib PNG.
Under it: caption + one paragraph explaining what the figure shows and why
it is the key. This is the **first** figure on the page, not the only one —
see `rules/03-illustration-policy.md` for the minimum count per source kind
(paper ≥ 3, lecture ≥ 2, clip ≥ 1, KS ≥ 1). Additional figures live inside
«Как это работает» subsections, attached to the concepts they illustrate.}

## Как это работает

{Details. Subsections are dictated by content. Typical subsections below.}

### Математика

{Formulas in LaTeX (`$...$`, `$$...$$`). Each non-trivial formula is followed
by a `где: ...` list explaining every symbol.}

### Pseudocode / Python

{3-6 lines per snippet. Variable names in English, comments in Russian.}

### Иллюстрация второго порядка

{Optional — if there are detail diagrams beyond the «Идея в одной картинке».}

## Вывод

{1-3 sentences. What the reader takes away after reading «Как это работает».
Not a repeat of TL;DR — by now the reader understands *why*.}

## Источник

- **`{source_path}`** ({source_kind}, {source_date})
- URL: {arxiv / DOI / blog link}
- Authors: {First Last et al.}
```

### Optional sections (insert between «Как это работает» and «Вывод»)

```markdown
## Результаты

{Papers with empirics only. 3-7 bullets with concrete numbers and benchmark
names. No vague «significant improvement» — specifics mandatory.}

## Сравнение с альтернативами

{2-4 bullets. Each: «X differs from <related method> in that …».}

## Ограничения

{Critical view: what the source omits, where it breaks, what it was not
tested on. This is the author-of-breakdown's section, not a retelling.}

## Открытые вопросы

- {Unresolved threads after reading.}
- {Experiments worth running.}

## Связанные разборы

- [[papers/<other-slug>]] — {one-line: why related}
- [[lectures/<other-slug>]] — {one-line}
```

**If an optional section has no content — it is absent**, not left as an empty header.

---

## Template B — Knowledge sharing variant

Same shape as Template A, with these deltas:

**Frontmatter:** replace `authors:` with `presenter:`, add optional `audience:` and `slides:`.

```yaml
---
title: <KS topic>
source_kind: knowledge-sharing
source_path: raw/knowledge-sharings/<file>
source_date: YYYY-MM-DD                      # date of the meeting
ingested: YYYY-MM-DD
presenter: <First Last>
audience: <team | internal | public>         # optional
slides: <URL or relative path>               # optional
tags: [<tag1>, ...]
status: stub | draft | mature
---
```

**Additional optional section** (insert before «Открытые вопросы»):

```markdown
## Q&A и обсуждение

- {Notable question + the answer / discussion that followed}
- {...}
```

Everything else (required sections, cross-cutting rules) is identical to Template A.

---

## Cross-cutting rules (apply to every template)

### Term introduction (first mention)

Every technical term gets a **one-line definition + everyday analogy** on its first mention. The term itself is rendered per the 3-tier hierarchy in `rules/01-language-policy.md`:

- **Bucket 1 — stable anglicism** (default for ML). Term stays English. Bold the English form, follow with Russian definition + analogy. Don't dress it in Russian and don't gloss with English in parens — it already is English.
- **Bucket 2 — translatable with traceability gloss.** Bold the Russian form, English in parens, then definition + analogy.
- **Bucket 3 — everyday math/ML vocab.** Bold either form, definition + analogy.

Format (bucket 1, default):

> **`<English term>`** — это <plain Russian definition>. Можно представить как <everyday-life analogy>: <one or two strokes of concrete detail>.

Format (bucket 2):

> **<Russian term>** (`<English original>`) — это <plain Russian definition>. <analogy>

Rules:

- **Bold** the term at first mention regardless of bucket.
- One short sentence of plain-Russian definition right after the bold.
- One analogy from everyday adult life (post office, library, customs, train timetable, electric kettle). Avoid analogies that themselves need analogies (don't say «это как middleware» if the reader doesn't know middleware).
- After first mention, use plain. No re-definition further down the page.
- Applies to ML terms, math objects, dataset names (Telco Churn, MNIST), magic numbers in code (`random_state=42`, `test_size=0.2`) on first appearance.

Examples:

> **`max path length`** — это сколько последовательных операций нужно градиенту, чтобы дойти от выхода до самого дальнего входного токена. Можно представить как **число пересадок** между двумя станциями метро: чем больше пересадок, тем больше шансов потеряться и тем дольше едет сигнал. Для self-attention оно равно 1: любой токен виден из любого за один шаг.

> **`attention sink`** — это феномен, когда несколько позиций (обычно первый токен или знаки препинания) собирают на себя непропорционально большой attention-вес почти во всех heads. Можно представить как **общая корзина «прочее»** в магазинной выкладке: товары, которые никуда не подошли, скапливаются в одном месте — но не потому что они особенно важны, а потому что больше некуда положить.

### Formula symbol annotation (`где: ...`)

Every non-trivial formula is followed by a `где: ...` list explaining each symbol. No exceptions.

Format:

> $\hat{y} = w_1 x_1 + w_2 x_2 + \ldots + w_n x_n + b$
>
> где:
> - $\hat{y}$ — предсказание модели
> - $x_1, x_2, \ldots, x_n$ — значения признаков объекта
> - $w_1, w_2, \ldots, w_n$ — веса модели, которые подбираются при обучении
> - $b$ — свободный член (intercept), смещение по вертикали
> - $n$ — количество признаков

Rules:

- Applies to LaTeX block formulas (`$$…$$`) and to inline formulas with non-trivial symbols (Σ, ∫, σ, α, β, ∇, indexed sums).
- Naked arithmetic (`x = 5 + 3`) — no `где` needed.
- If a Greek letter is used, name it once: «$\alpha$ — альфа, темп обучения».
- For indexed sums, state the index range.

### Code-formula bridge

Non-trivial math gets a short Python or pseudocode snippet (3-6 lines) that turns the formula into runnable code. Applies to loss functions, gradient computation, sigmoid / softmax, entropy / Gini, metric definitions.

Example:

```python
# MSE — средний квадрат ошибки
def mse(y_true, y_pred):
    return ((y_true - y_pred) ** 2).mean()

# Sigmoid
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
```

Rules:

- One concept = one snippet. No stuffing loss + gradient + update into one block.
- Pseudocode is fine when full Python distracts from the idea.
- Variable names in English, comments in Russian (`rules/01` and `write-russian` §9.3).
- Code blocks ≤ 10 lines by default.

### Other conventions

- All frontmatter follows `rules/04-frontmatter-schema.md`.
- Prose body is Russian; headings, slugs, frontmatter values are English (`rules/01-language-policy.md`).
- `[[wiki-link]]` syntax for internal references; the link path is `<kind>/<slug>` (e.g., `[[papers/su-2021-roformer]]`).
- No marketing voice, no AI-speak, no faux-warmth. Run the `write-russian` editing checklist before commit (`rules/01-language-policy.md` lists the banned phrases inline).
- Page length: dictated by content, no hard target. Long lectures may need 1500+ words; a short clip may fit in 400.
