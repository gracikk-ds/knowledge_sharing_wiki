# Session Insights

Append-only log of insights captured by the `autodoc` skill. One entry per session that produced something worth keeping.

Format of each entry:

```
## [YYYY-MM-DD] <one-line title>

**Category:** <Discovery | Wiki structure | Skill/tool issue | Gotcha>

<body — 1-5 paragraphs>
```

---

## [2026-05-17] Wiki overhaul scope locked

**Category:** Wiki structure

Spec `docs/superpowers/specs/2026-05-17-wiki-overhaul-design.md` defines the
fundament: role, hierarchical structure, rewritten CLAUDE.md, ingest v2,
autodoc, ONBOARDING. Hooks and skill-updater are explicitly out of scope —
they are in the "Next iteration" section of the spec and ship as separate
cycles.

---

## [2026-05-18] Next-iteration debts closed

**Category:** Wiki structure

The "Next iteration" backlog from the wiki-overhaul spec (section 10) is now
mostly closed:

- **skill-updater** — new 3-phase skill (`predict → review → apply`) for
  meta-edits of `.claude/`. Triggers narrowly: explicit user ask, or ≥ 5
  new entries in `.autodoc/insights.md` since the last apply commit (and
  that apply ≥ 14 days old). Otherwise dormant. Drafts land in
  `.claude/proposed-changes/` (gitignored), so unaccepted proposals never
  enter history.
- **Git hooks** in `.githooks/`, installed via `bash .githooks/install.sh`:
  - `pre-commit` checks frontmatter on staged wiki pages + soft-warns when
    a commit exceeds 300 lines.
  - `pre-push` (only on push to `main`) counts substantive commits since
    the last `chore(autodoc):` — if ≥ 2, prompts to run `/autodoc` before
    publishing. Hook can't invoke Claude; it nudges, you run the skill.
- **`/wiki-push` wrapper** was on the backlog; obsoleted because the push
  policy was lifted (Claude can push directly). The autodoc-trigger part
  of `/wiki-push` survived as the `pre-push` hook above.
- **`/wiki-illustrate` and `/wiki-russian`** were considered and rejected.
  Figure work belongs inside `/wiki-ingest`; voice cleanup belongs to the
  existing `write-russian` skill applied ad-hoc — no need for page-target
  wrappers.

**Gotcha:** `mapfile` is bash 4+; macOS ships bash 3.2 by default. Hook
scripts must use plain `while read` + heredoc, not `mapfile` + `read -d`.
Also avoid `set -u` if iterating over a possibly-empty array — use `[ -n
"$var" ]` checks instead.

## [2026-05-18] /onboard collapsed into the skill, ONBOARDING.md removed

**Category:** Wiki structure

The shadow text file `ONBOARDING.md` duplicated `/onboard` content and
went stale fast — layout was hardcoded in two places. Removed the file;
rewrote the skill to discover the repo state at runtime (`ls`, `find`,
read `description:` line from each `.claude/skills/*/SKILL.md`). The
walkthrough now reflects whatever is actually on disk, not a frozen
snapshot.

**Rule for future onboarding-style work:** never hardcode the repo's
folder structure or skill set into long-lived guides. Either link to the
live source, or have the guide enumerate at read-time. ASCII-tree blocks
in `.md` files rot.

## [2026-05-18] Push policy lifted

**Category:** Skill/tool issue

Original rule: "Claude never runs `git push`." That made push a manual
ritual after every session. New rule: push is allowed without per-action
approval. Force-push and pushing `main` from a feature branch still need
an explicit user OK. The pre-push hook gates publish-to-`main` on a
recent `/autodoc` so the policy doesn't bypass insight capture.

**Why preserve force-push and main-from-feature gates:** both can destroy
upstream state. Everything else is recoverable from origin.

## [2026-05-18] Pre-push autodoc nudge on every branch

**Category:** Skill/tool issue

First version of the pre-push hook only checked pushes to `main`. Real
work also lives on feature branches (wiki-overhaul, migrate-*,
experimental-*) — losing session insights there costs the same. The hook
now fires on every push, prints the branch name in the warning, and
counts substantive commits relative to HEAD (so the count makes sense
on each branch independently).

This bit when first tested: the hook caught two real substantive commits
on `wiki-overhaul` (the hook-generalization commit itself, and a later
onboard restoration). Confirmed the gate works on feature branches.

## [2026-05-18] /onboard restored from hardcoded version + sync contract

**Category:** Wiki structure

Earlier in this session: rewrote /onboard to be discovery-driven (no
hardcoded layout, ls/find at runtime). User reverted: the hardcoded
version is clearer to read; the runtime-discovery approach felt vague.

To make the trade-off explicit: added a **Maintenance contract** table
to `/skill-updater` listing every file that hardcodes structure (layout,
skill set, push policy, hooks, source kinds) and what else must travel
with each kind of change. Phase 1 of /skill-updater self-checks the
diff against this table before writing to .claude/proposed-changes/.

**Rule:** when accepting "hardcoded is clearer", commit to the sync work.
Don't pretend the cost isn't there.

## [2026-05-18] Commit-staging discipline with active external edits

**Category:** Gotcha

When the user is editing files externally (in their IDE) while Claude
runs `git add` + `git commit` sequentially, files modified between the
two commands can land in Claude's commit. Saw this happen: explicit
`git add .claude/...` showed 3 files in `git diff --cached --stat`,
but `git commit` shipped 6 (qwen page + log + new figure ended up
inside a skill-refactor commit).

Fix: `git reset --mixed HEAD~1`, re-add only the intended files,
recommit. Easy to recover before push.

**Prevention rule:** when the user is actively editing wiki/ files in
parallel, run `git add <paths> && git diff --cached --stat` and
`git commit -m ...` in a SINGLE compound Bash call so nothing slips
in between. Or: stage with `git add -- <paths>` and pass `--only`
to commit (`git commit --only -- <paths>`).
