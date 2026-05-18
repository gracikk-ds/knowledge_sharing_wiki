---
name: skill-updater
description: Safely update agent instructions (.claude/role.md, .claude/rules/*.md, .claude/skills/*/SKILL.md) based on session insights. Three-phase flow with mandatory user review — Claude never edits its own instructions autonomously. **Runs only on two triggers:** (1) the user explicitly asks ("update skills", "refresh rules", "обнови скиллы", "перепиши правила", "учти инсайты"); (2) the autodoc backlog crosses a threshold — `.autodoc/insights.md` has ≥ 5 new entries since the last `chore(meta): apply skill updates` commit, AND the most recent skill-updater run was ≥ 14 days ago. Otherwise the skill stays dormant. The skill writes a diff to .claude/proposed-changes/<date>.diff; the user reviews; the skill applies only the accepted hunks.
---

## When this skill activates

Two triggers, no others:

1. **User asks.** Any of: "update skills", "refresh rules", "обнови скиллы", "перепиши правила", "учти инсайты", or a clear synonym.
2. **Backlog threshold.** Both conditions must hold:
   - `.autodoc/insights.md` has accumulated **≥ 5 new entries** since the most recent commit whose subject starts with `chore(meta): apply skill updates` (if no such commit exists, count from the start of history).
   - The most recent run of this skill (last `chore(meta): apply` commit) is **≥ 14 days old**.

   Check both with:
   ```bash
   last_apply=$(git log --grep "^chore(meta): apply skill updates" --format="%H %ci" -1)
   new_insights=$(git log "${last_apply%% *}"..HEAD --format="" -- .autodoc/insights.md | wc -l)
   ```

If neither trigger fires, do not start the flow — just say so and stop. Drift in `.claude/` is preferred over reflexive self-editing.

# skill-updater

LLM editing its own instructions is the highest-risk operation in this repo — a single bad rewrite can corrupt every future session. This skill enforces a three-phase safety contract: **predict → review → apply**. Claude never edits `.claude/role.md`, `.claude/rules/*.md`, or `.claude/skills/*/SKILL.md` outside this flow.

## Pre-flight

- [ ] Read `.claude/role.md`
- [ ] Read every file under `.claude/rules/`
- [ ] Read `.autodoc/index.md` and the last 10 entries of `.autodoc/insights.md`
- [ ] Read recent commits under `.claude/`: `git log --oneline -30 -- .claude/`

## Phase 1 — Predict

Goal: produce a unified diff file under `.claude/proposed-changes/<YYYY-MM-DD-HHmm>.diff`. **Do not modify the actual files.**

- [ ] **Step 1.** From `.autodoc/insights.md` (last 10 entries), extract patterns:
  - Recurring **gotchas** that future sessions keep hitting → candidate for a new rule or a tightened existing rule.
  - **Skill/tool issues** that came up more than once → candidate for skill SKILL.md update.
  - **Wiki structure observations** (e.g., "this section overflows", "tag X is overloaded") → candidate for `_shared/page-templates.md` or `_shared/illustration-policy.md`.
  - **Discoveries** about voice, style, or terminology → candidate for `rules/01-language-policy.md` or `_shared/russian-style.md`.
- [ ] **Step 2.** Cross-check against `git log` on `.claude/` — if a rule was just changed, don't re-propose the same change.
- [ ] **Step 3.** Draft the proposed edits as a single diff file. Use unified diff format so the user can read it like a patch:

  ```diff
  --- a/.claude/rules/01-language-policy.md
  +++ b/.claude/rules/01-language-policy.md
  @@ -42,6 +42,9 @@ Stable anglicisms — kept English in body text:
   - sequence length
   - residual connection
   - max path length
  +- positional encoding (PE)
  +- feed-forward network (FFN)
  +- multi-head attention

   Reason: these terms are used as-is in Russian ML discourse.
  ```

  Each hunk must be **self-contained and independently applicable** — the user may accept some and reject others.

- [ ] **Step 4.** Write the file:

  ```bash
  printf '%s\n' "$DIFF_CONTENT" > .claude/proposed-changes/$(date +%Y-%m-%d-%H%M).diff
  ```

- [ ] **Step 5.** Add a top-of-file header **inside the diff file** (before the first `--- a/`) summarising what is being proposed and why:

  ```
  # Proposed skill/rule updates — YYYY-MM-DD HH:MM

  Rationale: <2-4 sentences citing specific .autodoc insights or recurring patterns>

  Hunks: N total
   1. <one-line summary>
   2. <one-line summary>
   ...

  To accept all: tell me "apply all from <date>.diff"
  To accept a subset: tell me "apply hunks 1, 3, 4 from <date>.diff"
  To reject: tell me "discard <date>.diff"
  ```

- [ ] **Step 6.** Report to the user: file path + the header text. **Stop and wait.** Do not proceed to Phase 3 without explicit user instruction.

## Phase 2 — Review (user-driven)

Out of band. The user reads the diff file (in their editor or via `cat`), decides which hunks to accept, and tells you. There is no Claude work in this phase.

Acceptable user instructions:
- `apply all from <date>.diff`
- `apply hunks 1, 3, 4 from <date>.diff` (1-based indexing, matching the header summary)
- `discard <date>.diff`
- `apply all from <date>.diff except hunk 2`

If the user wants to edit the diff before applying, they may — re-read the file in Phase 3.

## Phase 3 — Apply

Triggered by the user's `apply` instruction. Idempotent — re-running on the same diff with the same accepted set is a no-op.

- [ ] **Step 1.** Re-read the diff file. If it has been deleted or modified since Phase 1, stop and report.
- [ ] **Step 2.** For each accepted hunk, apply the change to the target file. Use the `Edit` tool with `old_string` / `new_string` derived from the hunk's `-` / `+` lines — patch fuzziness is not allowed; the surrounding context must match exactly. If `Edit` fails because the file changed since Phase 1, stop and report; do not retry with looser matching.
- [ ] **Step 3.** Delete the diff file: `rm .claude/proposed-changes/<date>.diff`.
- [ ] **Step 4.** Stage all touched files plus the deletion. Propose this commit:

  ```
  chore(meta): apply skill updates from <date>.diff

  Accepted hunks: <list — file:line summary per hunk>
  Skipped: <list, if any>

  Rationale: <copy from diff header>
  ```

- [ ] **Step 5.** **Stop and wait for the user to approve the commit message before running `git commit`.**

## What this skill is NOT

- Not a license to refactor `.claude/` at will. If you didn't see the pattern in `.autodoc/insights.md` or recent git history, don't propose changing it.
- Not for one-off fixes. Typo in a rule? Use a regular edit. This flow is for **systematic updates driven by accumulated session evidence**.
- Not a content-page editor. It only touches `.claude/role.md`, `.claude/rules/*.md`, and `.claude/skills/*/SKILL.md` (+ `_shared/`). `wiki/` is out of scope.
- Not autonomous. If the user has not yet said "apply", you wait — indefinitely if needed.

## Safety invariants

1. **Phase 1 produces a file. It must not modify the originals.** Any tool call in Phase 1 that targets `.claude/role.md`, `.claude/rules/`, or `.claude/skills/*/SKILL.md` with `Edit` or `Write` is a bug.
2. **Phase 3 applies only what the user listed.** If the user said "hunks 1, 3", hunk 2 is not applied.
3. **The diff file lives under `.claude/proposed-changes/`** — that directory is gitignored, so unaccepted proposals never enter the repo's history.
4. **If anything is unclear**, stop and ask. A skipped update is recoverable; a wrong update to the rules costs every future session.

## Maintenance contract

Several files hardcode the repo's structure or skill set and **must travel together** with structural changes. When a proposed diff touches any of the items in the left column, the diff **must also propose synchronized edits** to every file in the right column. The Phase 1 self-check verifies this before writing the diff to `.claude/proposed-changes/`; if a synchronized edit is missing, add it (or downgrade the change so it doesn't break the contract).

| If you're changing… | Then also update… |
|---|---|
| Repo layout (new top-level dir, renamed subfolder under `raw/` / `wiki/` / `.claude/`) | `.claude/skills/onboard/SKILL.md` (Phase 2 layout block), `.claude/CLAUDE.md` (Layout section), `AGENTS.md` (Layout block), `README.md` (Что внутри) |
| Skill set (added / removed / renamed a skill, changed a command surface) | `.claude/skills/onboard/SKILL.md` (Phase 4 command table), `.claude/CLAUDE.md` (Commands table), `AGENTS.md` (Skills table), `README.md` (Основные команды) |
| Push / commit policy | `.claude/skills/onboard/SKILL.md` (Phase 6), `.claude/rules/02-commit-policy.md`, `.claude/CLAUDE.md` (Principles section), `AGENTS.md` (Commit and push section) |
| Git hooks (`.githooks/`) | `.claude/skills/onboard/SKILL.md` (Phase 6), `.claude/CLAUDE.md` (Principles 7), `AGENTS.md` (Git hooks section), `.claude/rules/02-commit-policy.md` |
| Source kinds (`papers`, `lectures`, `clips`, `knowledge-sharings`) — added or removed | `.claude/skills/onboard/SKILL.md` (Phases 2-3), `.claude/role.md` (Where new pages live), `.claude/rules/04-frontmatter-schema.md`, every `_shared/*.md` that lists kinds, `.githooks/pre-commit` (frontmatter check regex) |

**Why `onboard/SKILL.md` is on every row:** the skill hardcodes layout, commands, push policy, and the source-kind taxonomy on purpose — a discovery-driven gid was tried and found less clear. The cost of "hardcoded" is exactly this contract: when something moves, the gid must move too. If a proposed change touches structure but the diff has no corresponding `onboard` hunk, the diff is incomplete.
