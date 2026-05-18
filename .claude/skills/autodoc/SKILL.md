---
name: autodoc
description: Capture session insights into .autodoc/. Run at the end of a session, after a meaningful /wiki-ingest, or when something non-obvious was learned. The pre-push hook reminds you to run it on any branch when ≥ 2 substantive commits have accumulated since the last `chore(autodoc):` commit (see rules/02-commit-policy.md). Triggers when user says "autodoc", "save session insights", "collect insights", "что узнали", "сохрани insights".
---

# autodoc

Persistent session memory: write down what was learned this session so future sessions can pick it up.

## Pre-flight

- [ ] Read `.autodoc/index.md`
- [ ] Read the last 5 entries of `.autodoc/insights.md` for context — avoid duplicates.

## What to save

| Category | What it captures |
|---|---|
| **Discovery** | Domain knowledge surfaced this session that wasn't in `wiki/` yet (and may belong there) |
| **Wiki structure** | Observations about the wiki itself — "this subfolder is overflowing, split it"; "this concept needs a topic primer"; etc. |
| **Skill/tool issue** | Something broke or behaved unexpectedly — mermaid rendering issue, Quartz build edge case, sed quirk, etc. |
| **Gotcha** | Non-obvious trap that should be documented to save the next visitor an hour. |

## What NOT to save

- Wiki content. That goes in `wiki/`.
- Information already in git log. Commit messages are the history of what changed.
- Current-session TODOs. Those belong in TodoWrite, not in autodoc.
- Routine progress updates ("finished task 5"). Only non-obvious findings.

## Procedure

- [ ] Step 1 — **Reflect on the session.** Ask: what did I learn that future-me would want? What unexpected thing happened? What would I want to know if I opened this repo cold tomorrow?
- [ ] Step 2 — **Draft 3-7 candidate insights** as bullets, each with a category. Skip categories that have no honest content.
- [ ] Step 3 — **Show candidates to the user** in this format:
  ```
  Draft insights for .autodoc/insights.md:

  1. [Category] <title>
     <1-3 sentences>

  2. [Category] <title>
     ...

  OK to append?
  ```
- [ ] Step 4 — **Wait for user OK.** If user edits or removes some, apply the edits.
- [ ] Step 5 — **Append to `.autodoc/insights.md`** in the format defined at the top of that file. Date the entries with today's date.
- [ ] Step 6 — **Update `.autodoc/index.md`** with one line per new entry: `- YYYY-MM-DD — [<title>](insights.md#<anchor>) — <one-line hook>`.
- [ ] Step 7 — **Propose a commit:**
  ```
  chore(autodoc): session insights — YYYY-MM-DD
  ```

## What you do not do

- Do not invent insights to look productive. If the session was routine, write nothing and say so.
- Do not edit past entries. Append corrections as new entries.
