---
name: wiki-query
description: Answer substantive ML, DL, CS, or system-design questions from this Obsidian vault by reading the wiki index and relevant notes, then synthesizing a precise answer with `[[wikilink]]` citations. Use for “what does the wiki say about X”, “synthesize X”, “answer from my notes”, and questions this vault could plausibly answer.
---

# wiki-query

Treat the wiki as the source of truth. Keep the candidate set small and stop expanding once the notes contain enough material to answer.

## Process

Track these steps in the task plan when a plan mechanism is available.

1. Restate the user's question in one precise sentence. Ask only if ambiguity materially changes the answer; otherwise choose the most charitable interpretation.
2. Read every line of `wiki/index.md`. Select direct hits and a small number of likely indirect hits.
3. Read each selected note in full.
4. Synthesize the answer and cite non-trivial claims with `[[wiki-link]]`.

## Answer quality

- Define the subject before making claims.
- Match the form to the question: a definition needs prose; a derivation needs equations.
- Follow `styleguide.md` conventions for language, voice, LaTeX, and intuition beside math.
- Distinguish note content from inference. Prefix claims that go beyond the notes with `Вывод за пределами wiki:` or `Inferring beyond the wiki:`, matching the response language.
- Never invent results or cite a page that does not exist.

If the answer turns into creating or editing a note under `wiki/`, read `styleguide.md` in full immediately before the edit.

## Sparse coverage

If the index contains no relevant material, say so directly, name only the closest pages and explain why they are tangential. Ask whether to answer from general knowledge instead. Do not imply that the wiki covers the topic.
