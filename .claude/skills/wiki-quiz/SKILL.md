---
name: wiki-quiz
description: Generate a quiz from the wiki — multiple choice tests, open questions, or solve-on-paper problems (derivations, hand calculations, worked examples). Always asks first about format, scope, difficulty, and count before generating anything. Has a special interview-prep mode for broader coverage of a topic area. Triggers on "quiz me", "test me", "give me problems", "drill X", "interview prep", "проверь меня", "дай задач", "квиз", "тест", and similar.
---

# wiki-quiz

Workflow for generating quizzes from wiki content. The user uses these to check their understanding — sometimes for fun, sometimes for interview prep, sometimes to find weak spots in a specific topic.

The wiki is the source of truth. Every question must be answerable from a page that exists in the wiki. If you cannot anchor a question to a wiki page, drop it.

---

## Checklist (mirror as TodoWrite tasks)

1. **Clarify the request.** Format, scope, difficulty, count, interaction mode. Always ask — do not skip this step.
2. **Pick source pages.** Read `wiki/index.md`, then read the relevant pages in full.
3. **Generate questions.** Match the requested type and difficulty. Anchor every question to a specific wiki page.
4. **Present the quiz.** One question at a time (interactive) or as a batch (offline solving).
5. **Grade and explain.** Compare the user's answer to the wiki. Link to the source page in every explanation.
6. **Log the session.** Append a `quiz` entry to `wiki/log.md` capturing scope, format, score, and weak spots.

---

## Step 1 — Clarify the request

Before generating any question, ask the user four things. Use the `AskUserQuestion` tool if available; otherwise list them inline. Wait for the answers.

- **Format:**
  - Multiple choice (quick recall — pick one of four)
  - Open questions (explain, describe, compare — written answer)
  - Problems (math / derivations / hand-calculated examples — paper and pen)
  - Mixed
- **Scope:**
  - One specific page (e.g. `[[ml_concepts/attention]]`)
  - A topic area (e.g. everything under `[[topics/optimization]]`)
  - Interview prep on X — broader, mixes concepts + math + methods
  - Whatever the index covers (random across `mature` pages)
- **Difficulty:**
  - Warmup — definitions, identification, "what is X"
  - Standard — explain, apply, work through a mechanism
  - Hard — derive, compare, edge cases, "why does X fail when Y"
- **Count and mode:**
  - N questions, batch (user solves offline, returns with answers later)
  - N questions, interactive (one at a time, instant feedback)

If the user has asked you to work without stopping for clarifying questions, pick sensible defaults and announce them: standard difficulty, 5 questions, interactive, format inferred from the scope (math-heavy topic → problems; ML mechanism → mixed open + multiple choice).

---

## Step 2 — Pick source pages

- Read `wiki/index.md` first.
- For one specific page: read that page in full, plus pages it directly links to (one hop out).
- For a topic area: read the topic page and every page it lists.
- For interview prep on X: pull every page whose tags or summary mention X, plus the `[[ml_concepts/...]]`, `[[math_concepts/...]]`, and `[[methods/...]]` pages linked from them. Read each in full.
- For "whatever the index covers": pick 3–5 random `mature` pages. Bias toward pages the user hasn't quizzed recently (skim recent `quiz` log entries to avoid repetition).

Do not generate questions from pages you have not read in full. If a topic is thin in the wiki, say so before generating — suggest a `wiki-ingest` first.

---

## Step 3 — Generate questions

Anchor every question to at least one wiki page. List the anchor pages with the question (or hold them for the answer key, depending on mode).

### Multiple choice

- Four options. Exactly one is correct.
- Distractors must be plausible. Pull common misconceptions from "Common pitfalls" sections on `math_concept` pages when they exist.
- Avoid "all of the above" / "none of the above".
- The stem is one sentence ending in `?` or a fill-in-the-blank.

### Open question

- Phrased to require an explanation, not yes/no.
- Good shapes:
  - "Explain why X."
  - "Describe what happens to Y when Z changes."
  - "Compare A and B — when would you reach for each?"
  - "Walk through the derivation of Z."

### Problem (paper and pen)

- One concrete scenario with every input named.
- Pick small numbers so the answer can be checked by hand.
- Tell the user this is a paper-and-pen problem so they know to grab a sheet.
- Use LaTeX (`$...$`, `$$...$$`) for math.
- Good shapes:
  - "Compute $\text{softmax}([2, 1, -1])$ (use natural log)."
  - "Given $A \in \mathbb{R}^{3 \times 2}$ and $B \in \mathbb{R}^{2 \times 4}$, what is the shape of $AB$? With the specific values below, compute $AB_{0,2}$ by hand."
  - "Derive $\partial \mathcal{L} / \partial z_i$ for the cross-entropy loss on a single example with $K$ classes, where $z$ are the pre-softmax logits."

### Quality bar for questions

- Mix conceptual and technical. Do not ask only definitions.
- For interview prep mode, include at least 2–3 derivation/computation problems alongside the conceptual ones.
- If two of your generated questions test the same thing, drop one.
- Hard questions should still be answerable from the wiki — not from outside knowledge.

---

## Step 4 — Present the quiz

### Interactive mode (one at a time)

Send one question per turn. Do not reveal the answer or the source page until the user answers.

```
**Q1 / N — [format, difficulty]**

{question text}

{options A–D, if multiple choice}
```

Wait for the user. Move to the next question after grading the current one.

### Batch mode (all at once)

Send all N questions in a single message, numbered. Tell the user to solve and return when ready. Hold the answer key until they ask for it.

```
N questions on {topic}. Solve them on paper, then come back with your answers.

**Q1 — [format, difficulty]**
{question}

**Q2 — [format, difficulty]**
{question}
...
```

---

## Step 5 — Grade and explain

For each user answer:

- **Multiple choice.** State correct or incorrect. Quote the right option and explain in one sentence why the others fail.
- **Open question.** Compare the user's answer against the wiki page in full. Call out what is correct, what is missing, what is wrong. Cite the page inline with `[[wiki-link]]`.
- **Problem.** Check the computation step by step. Where the user diverged from the expected solution, show the right step and explain what went wrong (sign error, dimension mismatch, wrong base of log, etc.).

Always end the explanation with a link back to the source page: "See `[[ml_concepts/...]]` for the full derivation." If the user got the same kind of question wrong twice in one session, note it — that is a candidate for a follow-up `wiki-ingest` (the wiki may be thin there) or a new `[[questions/...]]` page.

---

## Step 6 — Log the session

Append one entry to `wiki/log.md`:

```markdown
## [YYYY-MM-DD] quiz | {short topic} ({N} questions, {format})

- **Scope:** [[a]], [[b]], [[c]]
- **Format:** {multiple choice / open / problems / mixed}
- **Difficulty:** {warmup / standard / hard}
- **Score:** {N correct / M total} or "ungraded" for open-answer-only sessions
- **Weak spots:** {topics where the user got things wrong — useful as ingest signals}
- **Notes:** {anything noteworthy — e.g. user asked a question the wiki cannot
  answer yet; flag for next ingest}
```

The log becomes a record of what has been drilled. `wiki-lint` can read this later to spot under-drilled areas.

---

## Interview prep mode

When the user asks for "interview prep on X" the workflow shifts:

- Pull a broader page set: 8–15 pages instead of the usual 3–5.
- Generate 10–20 questions, weighted across:
  - Definitions and intuition (~30%)
  - Math derivations and step-by-step problems (~30%)
  - Comparisons with alternative methods or approaches (~20%)
  - Common interviewer follow-ups: "what would change if we removed X?", "what fails when the input is degenerate?", "how does this scale?" (~20%)
- Include at least 2–3 paper-and-pen problems if any `math_concept` or `method` pages are in scope.
- After grading, give a short readiness summary: what is solid, what needs more work, where a confident "I don't know — but here is how I would reason about it" is the right answer.

---

## Spaced repetition / follow-up quizzes

If the user asks for a "follow-up" or "spaced" quiz, read recent `quiz` log entries to find what they got wrong before. Re-ask those questions (or close variants) alongside new ones. Target a 30/70 mix of revisit / new.

---

## What this skill is NOT

- Not a chat. Quizzes drill specific knowledge. Stay on topic; do not drift into open conversation between questions.
- Not a wiki edit workflow. If a quiz surfaces a missing page or a contradiction, note it in the log entry and suggest a follow-up `wiki-ingest` or `wiki-lint`. Do not edit pages mid-quiz.
- Not a substitute for ingesting sources. If the wiki is thin on a topic the user wants to drill, say so plainly — suggest ingesting more before quizzing.
