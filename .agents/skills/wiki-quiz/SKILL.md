---
name: wiki-quiz
description: 'Generate and grade quizzes grounded strictly in this wiki: multiple choice, open questions, derivations, and hand-calculation problems, including interview-prep and spaced-repetition modes. Use for “quiz me”, “test me”, “give me problems”, “interview prep”, «проверь меня», «дай задач», «квиз» and similar requests.'
---

# wiki-quiz

Use the wiki as the source of truth. Every question must be answerable from an existing page and anchored to at least one source note.

Follow `styleguide.md` for generated prose and math. Before creating or editing any note under `wiki/`, including `wiki/log.md`, read `styleguide.md` in full.

## Configure the quiz

Before generating questions, ask for:

1. format: multiple choice, open questions, paper-and-pen problems, or mixed;
2. scope: one page, a topic area, interview prep, or everything covered by the index;
3. difficulty: warmup, standard, or hard;
4. count and mode: batch or interactive.

Wait for the answers. If the user explicitly asks to proceed without clarification, announce sensible defaults: standard difficulty, five interactive questions, and a format inferred from the topic.

## Select sources

1. Read `wiki/index.md`.
2. For one page, read it in full.
3. For a topic, read the topic page and the relevant pages it links.
4. For interview prep, select every indexed page whose title, tags, or summary matches the topic.

Do not generate a question that lacks a wiki source.

## Generate questions

### Multiple choice

- Provide four options with exactly one correct answer.
- Use plausible distractors, preferably based on documented pitfalls.
- Do not use “all of the above” or “none of the above”.

### Open questions

Ask for explanations, mechanisms, comparisons, or derivations. Avoid yes/no questions.

### Paper-and-pen problems

- Give one concrete scenario with every input named.
- Prefer small values that can be checked by hand.
- Tell the user it is a paper-and-pen problem.
- Format all math as LaTeX.

Mix conceptual and technical questions. Remove duplicates that test the same idea. Hard questions must still be answerable from the wiki.

## Present and grade

In interactive mode, send one question per turn as `Qk / N`, without its answer or source link. Grade the answer before moving on.

In batch mode, send all numbered questions together and withhold the answer key until requested.

For every graded answer:

- state whether it is correct;
- identify what is right, missing, or wrong;
- for calculations, show the first divergent step and explain the error;
- finish with the source `[[wiki-link]]`.

If the same weakness appears twice, flag it as a candidate for follow-up study or `$wiki-ingest`.

## Log the completed session

Tell the user that completing a quiz includes updating `wiki/log.md`. After grading, append:

```markdown
## [YYYY-MM-DD] quiz | {short topic} ({N} questions, {format})

- **Scope:** [[a]], [[b]], [[c]]
- **Format:** {multiple choice / open / problems / mixed}
- **Difficulty:** {warmup / standard / hard}
- **Score:** {N correct / M total} or "ungraded" for open-answer-only sessions
- **Weak spots:** {topics where the user struggled}
- **Notes:** {anything useful for future study or ingest}
```

Use the current system date. Preserve existing log content. If `wiki/log.md` does not exist, create it during the first completed quiz session.

## Interview-prep mode

Use 8–15 source pages and usually 10–20 questions:

- definitions and intuition: about 30%;
- derivations and computations: about 30%;
- comparisons: about 20%;
- interviewer follow-ups and edge cases: about 20%.

Include at least two or three paper-and-pen problems. After grading, summarize readiness, strengths, and gaps.

## Spaced repetition

For a follow-up or spaced quiz, read recent quiz entries in `wiki/log.md`. Use roughly 30% variants of previously missed questions and 70% new questions.
