# Page Templates

Read this in `wiki-ingest` phase 5. Pick the template matching the page `type:`.

## ML concept page (`type: ml_concept`)

When to use: an ML idea that exists independently of any single algorithm — attention, dropout, residual connection. The page belongs in `wiki/ml_concepts/<slug>.md`.

```markdown
---
{frontmatter}
---

# {Title}

> {few-sentence definition — crisp, no hedging. This is the entry for refresh-mode reading.}

## Motivation

{2–4 paragraphs in motivated build-up voice: name what we want, name the naive
thing, name why it fails, name the workaround this concept introduces. Direct
prose, no Q&A markers, no metaphors. Math when it clarifies.}

## Formal description

{math, pseudocode, or precise prose. Use LaTeX-style $...$ and $$...$$. For
non-trivial math, link out to [[math_concepts/...]] instead of expanding it
inline.}

## Variations and related concepts

- [[ml_concepts/other-concept]] — {one-line relationship}
- [[methods/some-method]] — {how this method instantiates the concept}
- [[math_concepts/some-math]] — {the math underneath}

## Open questions

- [[questions/some-open-question]]
- {or inline if you haven't filed the question as its own page yet}

## Sources

- [[sources/source-page-a]] — {what this source contributed}
- [[sources/source-page-b]] — {what this source contributed}

## Up next

- [[wiki-link]] — {one-line "why this is the natural next step for a reader studying this area"}
```

## Math concept page (`type: math_concept`)

When to use: a math object used in ML — KL divergence, softmax, rotation matrix. Walk every step. The page belongs in `wiki/math_concepts/<slug>.md` (flat).

The math template differs from the ML template: more careful exposition, fewer shortcuts. The reader struggles with dense math, so unpack every step.

```markdown
---
{frontmatter}
---

# {Title}

> {few-sentence definition — what this math object computes, asserts, or measures}

## Plain-English statement

{What this is, in words. When the math object has a clean motivating story —
what we want, what naive approach fails, how this object solves it — open
with that build-up arc. For pure-math objects without such an arc, just unpack the definition.
Math notation OK, but introduce each symbol when it first appears. Don't drop into formulas
without naming the variables.}

## Step-by-step

{Walk through the math without compression. Show every intermediate step. If a
step uses another math object, link to it: [[math_concepts/x]]. Tell the
reader what each line does and why — not just what it equals.}

## Worked example

{One concrete numerical example with small numbers. Compute end-to-end so the
reader can verify by hand. For multi-dim objects, show the shapes at each step.}

## Where it shows up in ML

- [[ml_concepts/...]] — {how this math object is used in ML}
- [[methods/...]] — {methods that rely on it}

## Common pitfalls

- {index confusions, sign errors, off-by-one mistakes, dimension mismatches,
  base of log, etc.}

## Sources

- [[sources/...]]
```

## Method page (`type: method`)

When to use: a specific algorithm or technique — AdamW, FlashAttention, LoRA. The page belongs in `wiki/methods/<slug>.md`.

```markdown
---
{frontmatter}
---

# {Title}

> {few-sentence summary: what problem this method solves and how}

## Motivation

{2–4 paragraphs in motivated build-up voice: what we want this method to do,
what the naive or previous approach fails at, how this method's design
addresses that. Direct prose, no Q&A markers, no metaphors.}

## Problem setting

{when this method applies; what assumptions it makes}

## Algorithm

{pseudocode or explicit equations. Be precise about indices, shapes, and
hyperparameters.}

## Why it works

{the underlying concept(s) it leverages, with [[wiki-links]] to concept pages}

## Properties

- Complexity: {time / memory}
- Hyperparameters: {what to tune, sensible defaults}
- Failure modes: {when it breaks}

## Variants and successors

- [[related-method]] — {one-line delta}

## Sources

- [[sources/...]]

## Up next

- [[methods/successor-or-related-method]] — {what it adds over this one}
- [[topics/parent-topic]] — {how to see this method in the wider area}
```

## Topic page (`type: topic`)

When to use: a narrative primer for a whole area — Optimization, Regularization, Attention Variants. The page belongs in `wiki/topics/<slug>.md` (flat).

Topic pages are *primers*: narrative entry points that walk a reader through an area in motivated build-up voice, with inline links into the reference layer. They are not link maps — the story is in the prose, and reading order is woven into it. The numbered "Reading order (recap)" at the bottom is for scanability only.

```markdown
---
{frontmatter}
---

# {Title}

> {few-sentence framing of the area}

## The setting

{2–4 paragraphs in build-up voice: the problem this area addresses, what makes
it hard, what class of techniques shows up. This is the entry into the story,
not a "scope" disclaimer.}

## Core ideas

{Narrative through the concept pages of the area in reading order. Each
concept is introduced inline with `[[ml_concepts/foo]]` or
`[[math_concepts/foo]]`; the transitions between them explain why one leads to
the next. Build-up voice. Reading order is woven into prose, not stated as a
list here.}

## Methods that grow from these ideas

{Narrative through method pages in reading order, with `[[methods/...]]`
inline. Each method gets a one-paragraph sketch of what it does and what it
adds over the previous one.}

## Open threads

- {unresolved questions, what to ingest next; bullets are fine here}

## Reading order (recap)

1. [[ml_concepts/...]]
2. [[ml_concepts/...]]
3. [[methods/...]]
...

## Reading queue

- {sources to ingest next, even if not yet in raw/}
```

Target length: ~500–1200 words; expand when justified by content. No hard cap.

## Source page (`type: source`)

When to use: every ingested raw source gets one. The page belongs in `wiki/sources/<slug>.md` (flat).

```markdown
---
{frontmatter with source_path, source_kind, source_date, ingested}
---

# {Title}

> {few-sentence "what this source is and why it mattered"}

## Key takeaways

- {3–7 bullets, in your own words. Not a transcription of the source.}

## Concepts touched

- [[ml_concepts/concept-a]] — {how the source addressed it: new info, confirmation, contradiction, refinement}
- [[math_concepts/concept-b]] — {…}

## Contradictions and revisions

{Did this source disagree with anything already in the wiki? Note it. This
section can be empty.}

## Questions raised

- [[questions/...]]

## Pointer back to raw

`{source_path}`
```

## Question page (`type: question`)

When to use: an open question that hasn't been resolved. The page belongs in `wiki/questions/<slug>.md` (flat).

```markdown
---
{frontmatter; status starts as `stub`, flips to `mature` when resolved}
---

# {The question, phrased clearly}

## Why it matters

{1–3 sentences}

## What we know so far

- {bullets summarising current state — link to concepts/sources}

## What would resolve it

- {experiment, paper to find, derivation to attempt}

## Related

- [[ml_concepts/...]] or [[math_concepts/...]]
- [[sources/...]]
```

## Common conventions across all templates

- All frontmatter follows `rules/04-frontmatter-schema.md`.
- Prose body is Russian; headings, slugs, frontmatter values are English (`rules/01-language-policy.md`).
- Math in LaTeX, never in backticks (this carries over from existing CLAUDE.md guidance).
- `[[wiki-link]]` syntax for internal references.
- Page length: as long as needed, no longer. Soft target 200-1000 lines body; hard split at ~750 if a natural sub-concept emerges.

---

## Term introduction (every page)

Every technical term gets a **one-line definition + everyday analogy** on its first mention. After that, use the term plainly.

**Format:**

> **`<термин>`** (`<English original>`, if relevant) — это `<plain Russian definition>`. Можно представить как `<everyday-life analogy>`: `<one or two strokes of concrete detail>`.

**Rules:**

- **Bold** on the term at first mention.
- One short sentence of plain-Russian definition right after the bold.
- One analogy from everyday adult life (post office, library, customs, train timetable, lab notebook, electric kettle, restaurant ticket). Avoid analogies that themselves need analogies ("это как middleware" — fails if reader doesn't know middleware).
- After first mention, use plain. No re-definition further down the page.
- Applies to: ML terms, math objects, dataset names (Telco Churn, MNIST), magic numbers in code (`random_state=42`, `test_size=0.2`) on first appearance.

**Example:**

> **Attention sink** — это феномен, когда несколько позиций (обычно первый токен или знаки препинания) собирают на себя непропорционально большой attention-вес почти во всех headах. Можно представить как **общая корзина «прочее»** в магазинной выкладке: товары, которые никуда не подошли, скапливаются в одном месте — но не потому что они особенно важны, а потому что больше некуда положить.

---

## Formula symbol annotation (math pages and any prose with math)

Every formula is followed by a **`где: …` list** explaining each symbol. No exceptions.

**Format:**

> $\hat{y} = w_1 x_1 + w_2 x_2 + \ldots + w_n x_n + b$
>
> где:
> - $\hat{y}$ — предсказание модели
> - $x_1, x_2, \ldots, x_n$ — значения признаков объекта
> - $w_1, w_2, \ldots, w_n$ — веса модели, которые подбираются при обучении
> - $b$ — свободный член (intercept), смещение по вертикали
> - $n$ — количество признаков

**Rules:**

- Applies to LaTeX block formulas (`$$…$$`) and to inline formulas with non-trivial symbols (Σ, ∫, σ, α, β, ∇, indexed sums).
- Naked arithmetic (`x = 5 + 3`) — no `где` needed.
- If a Greek letter is used, name it once on first appearance: «$\alpha$ — альфа, темп обучения».
- For indexed sums, state the index range: «$i$ пробегает от $1$ до $n$».

---

## Code-formula bridge (non-trivial math gets a snippet)

Any non-trivial math concept gets a short Python or pseudocode snippet (3-6 lines) that turns the formula into runnable code. Applies to loss functions, gradient computation, sigmoid / softmax, entropy / Gini, metric definitions.

**Example:**

```python
# MSE — средний квадрат ошибки
def mse(y_true, y_pred):
    return ((y_true - y_pred) ** 2).mean()

# Sigmoid
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
```

**Rules:**

- One concept = one snippet. Don't stuff loss + gradient + update into one block.
- Pseudocode is allowed when full Python distracts from the idea.
- Variable names in English, comments in Russian (`rules/01` and `write-russian` §9.3).
- Code blocks ≤ 10 lines by default. Longer only when the structure itself is the point.
