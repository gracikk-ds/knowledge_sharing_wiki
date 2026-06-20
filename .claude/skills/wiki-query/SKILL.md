---
name: wiki-query
description: Answer a question against the wiki — read the index, drill into relevant pages, synthesize a precise answer with citations. Use whenever the user asks an ML question against this vault, says "what does the wiki say about X", "synthesize X", or asks any substantive question that the wiki could plausibly answer.
---

# wiki-query

Workflow for answering a question against the wiki.

---

## Checklist (mirror as TodoWrite tasks)

1. **Restate the question.** One sentence, in your own words, so any ambiguity surfaces before you go searching.
2. **Read `wiki/index.md`.** Pick candidate pages by skimming the one-line summaries.
3. **Drill into candidate pages.** Read the relevant pages in full.
4. **Synthesize the answer.** Cite by `[[wiki-link]]`. Distinguish what's in the wiki from what you're inferring.

---

## Step 1 — Restate the question

Rewrite the user's question in one precise sentence. Examples:

- User: "what's the deal with attention scaling?" → Restate: "Why is the dot-product attention score divided by √d_k in the Transformer formulation?"
- User: "how does Adam differ from SGD?" → Restate: "What does Adam compute differently from vanilla SGD, and what failure modes does that change introduce or remove?"

If the restated question is ambiguous in a load-bearing way, ask clarifying questions. Otherwise pick the most charitable interpretation and proceed.

---

## Step 2 — Read the index

Open `wiki/index.md`. Read every line. Mentally tag candidates:

- Direct hits: pages whose one-line summary matches the question.
- Indirect hits: pages that are likely to be linked from the direct hits.

Keep the candidate list short. If the candidate list explodes, the question is probably too broad — narrow it before drilling.

---

## Step 3 — Drill in

Read each candidate page in full. Stop expanding once you have enough material to answer.

---

## Step 4 — Synthesize

Write the answer for the user. Follow the same quality bar as wiki pages:

- **Definitions before claims.** State what the question is about, then the answer.
- **Cite specifically.** Every non-trivial claim ends in a `[[wiki-link]]` to the page it came from. If the claim came from multiple pages, list both.
- **Distinguish wiki content from inference.** If you're going beyond what the wiki says (e.g., synthesising a comparison the wiki doesn't make explicitly), say so with a brief "Inferring beyond the wiki:" tag. Don't invent results.
- **Match the form to the question.** A definition deserves a paragraph. A derivation deserves equations. Don't bullet-point everything reflexively.
## When the wiki is too small to help

In the early days the wiki will be sparse. If a question lands and there's nothing relevant in the index, say so plainly:

```
The wiki doesn't cover this yet. Closest pages:
- [[a]] (tangentially related: ...)

Want me to answer from general knowledge anyway, or hold until we've fed in
relevant sources?
```

Do not pretend the wiki said something it didn't. Citing absent pages is worse than citing none.
