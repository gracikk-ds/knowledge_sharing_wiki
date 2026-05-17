---
name: wiki-lint
description: Health-check the wiki — scan for orphan pages, broken links, frontmatter errors, stale claims, and tag-index inconsistencies. Report findings and let the user pick what to act on. Use when the user says "lint the wiki", "audit the wiki", "health check", or asks for a wiki cleanup. Run periodically (every 10–20 ingests is a reasonable cadence).
---

## Pre-flight

- [ ] Read `.claude/role.md`
- [ ] Read `.claude/rules/04-frontmatter-schema.md`
- [ ] Read `wiki/tags.md` — the live tag registry; used to validate page tags

# wiki-lint

Workflow for auditing the wiki's health. The goal is to **surface problems clearly, propose concrete fixes, and let the user decide what to act on**. Don't silently fix structural problems; report them first.

A lint pass is not the same as an ingest. It uses no new sources — it only analyses what's already there.

---

## Checklist (mirror as TodoWrite tasks)

1. **Take inventory.** Count pages by source kind; spot-check the index for completeness.
2. **Run the lint checks** (see Lint checks section below). Each check produces zero or more findings.
3. **Group findings** by severity: blockers (broken links, frontmatter errors), structural (orphans, tag-index drift), editorial (stale claims, contradictions, voice drift).
4. **Report.** Present findings in a single structured report. Suggest a concrete fix for each.
5. **Wait for user steering.** Don't auto-fix anything beyond trivial frontmatter or index hygiene. The user picks what to act on.
6. **Apply approved fixes.** Edit pages, update index, append a single lint log entry summarising the run.

---

## Inventory

Scan all pages under:

- `wiki/papers/**/*.md`
- `wiki/lectures/**/*.md`
- `wiki/clips/**/*.md`
- `wiki/knowledge-sharings/**/*.md`

(`wiki/index.md` and `wiki/log.md` follow their own minimal schema and are not lint targets in this version.)

Use the Bash tool to count and list:

```bash
find wiki/papers/ wiki/lectures/ wiki/clips/ wiki/knowledge-sharings/ -name "*.md" 2>/dev/null | sort
wc -l wiki/index.md wiki/log.md
grep -c "^## \[" wiki/log.md   # number of log entries
```

Cross-reference:

- Does every page found on the filesystem appear in `wiki/index.md`?
- Does every entry in `wiki/index.md` correspond to a real file?

This catches drift between index and filesystem early.

---

## Lint checks

Frontmatter rules are in `.claude/rules/04-frontmatter-schema.md`. Enforce all 9 validation rules from that file. Run these checks in order. Each section specifies *how* to detect the problem, *why* it matters, and *what to propose* as a fix.

1. **Frontmatter present** — file starts with `---` on line 1; ends with `---` before body.
2. **All base fields present** — `title`, `source_kind`, `source_path`, `source_date`, `ingested`, `authors` (or `presenter` for KS), `tags`, `status`.
3. **`source_kind` matches directory** — `wiki/papers/*.md` has `source_kind: paper`, etc.
4. **`source_path` exists** — referenced file under `raw/` resolves.
5. **`source_date` ≤ `ingested`** — chronological sanity.
6. **`tags` non-empty and all registered** — every page tag has a matching H2 entry in `wiki/tags.md` (the `**Slug:**` line value). Flag unknown tags with a proposed fix: either add the tag to `wiki/tags.md` with a definition, or change it to an existing tag.
7. **`status` is one of: `stub`, `draft`, `mature`**.
8. **For KS pages: `presenter` is present**, `authors` is absent.
9. **Slug pattern matches `source_kind`** — see `rules/04` slug table.
10. **No broken `[[wiki-links]]`** — link target file exists under `wiki/`.
11. **No orphan pages** — every page is reachable from `wiki/index.md`.
12. **Tag-index consistency** — every page's tags appear in the `By tag` section of `wiki/index.md`.
13. **Tag-registry consistency** — every H2 in `wiki/tags.md` has a `**Slug:**` line and a `[Все разборы →](/tags/<slug>)` link. No orphan registry entries (tag defined but never used on any page) older than one ingest cycle — flag them so the user can either drop the entry or schedule an ingest that uses the tag.

### Check 10 detail: broken `[[wiki-links]]`

**How:** for every `[[link]]` in every wiki page, confirm a target page exists. A link `[[papers/foo]]` should match `wiki/papers/foo.md`. Use a grep-and-check loop.

**Why:** broken links are silent rot.

**Propose:** for each broken link, classify as:

- **Stub-worth:** the concept genuinely deserves a page — propose a stub ingest target.
- **Renamed:** the target was renamed; fix the link to point to the new slug.
- **Spurious:** the link doesn't make sense as a wiki page — remove it.

### Check 11 detail: orphan pages

**How:** a page is an orphan if no other wiki page links to it AND it's not linked from `wiki/index.md`. Walk every page's outgoing links and build the inbound set per target.

**Why:** orphans are pages the wiki has forgotten.

**Propose:**

- **Orphan stub:** suggest related breakdowns to link from.
- **Orphan mature page:** suggest 2–3 specific pages whose `Связанные разборы` section should reference it.

### Check 12 detail: tag-index consistency

**How:** for each page, read its `tags:` list. Open `wiki/index.md` → «By tag» section. Each tag must have an entry listing the page. Flag any page whose tag doesn't appear there, or any index tag entry pointing to a non-existent page.

**Why:** the «By tag» section is the primary concept-navigation path for `wiki-query`.

**Propose:** rebuild the missing tag-group entries. Safe to auto-apply with user opt-in.

### Additional checks

**Stale claims:**

- Claims of "state-of-the-art" or "current best" with no date.
- Numerical results without a source link.
- Mentions of named models/methods superseded by a newer thing in another wiki page.

**Propose:** flag the page and section, suggest specific edits (add date, add citation, mark as historical).

**Contradictions:**

- Two breakdowns cite the same paper but report different numbers.
- A breakdown says "X is required" but another describes a method without X.

**Propose:** for each contradiction, either (a) reconcile inline by adding context, (b) note it as an open question on the relevant page, or (c) flag for the next ingest of a tie-breaking source.

**Voice drift:** sample 5–10 random pages and check for banned filler per `rules/01`:

- "in conclusion", "in summary", "it is important to note", "let's dive in"
- "powerful", "fascinating", "revolutionised" (applied to the concept itself)
- Meta-commentary ("this page covers…", "this section discusses…")

**Propose:** quote the offending sentences with their file paths for user review.

**Page size:** flag any page over 750 lines. Propose a natural split point.

**Index drift:** compare `wiki/index.md` entries against the actual filesystem. Safe to auto-rebuild with user opt-in.

---

## Step 3 — Group findings

Bucket findings by severity:

| Severity | Bucket | Example |
|---|---|---|
| **Blocker** | Breaks the wiki's read path | Broken links, malformed frontmatter, missing required fields, index/filesystem drift |
| **Structural** | Affects discoverability or compounding | Orphans, tag-index inconsistency, contradictions |
| **Editorial** | Affects quality / trust | Stale claims, voice drift, oversized pages |

---

## Step 4 — Report

Single structured report, in this order. Be concise. Don't pad sections with "no findings" if there's nothing to report — drop the empty sections instead.

```markdown
# Wiki Lint — YYYY-MM-DD

Inventory: {P papers, L lectures, C clips, K knowledge-sharings}
Log entries: N

## Blockers

### Frontmatter issues (N)
- `papers/su-2021-roformer.md` — missing `source_date` field.
- `lectures/karpathy-makemore-3.md` — unknown tag `rnn` (no entry in wiki/tags.md).

### Broken links (N)
- [[papers/foo]] in `lectures/bar.md` → target missing. Propose: stub ingest.

### Index drift (N)
- `wiki/index.md` lists [[papers/x]] but file is gone. Propose: remove entry.

## Structural

### Orphans (N)
- [[clips/illustrated-transformer-alammar]] — no inbound links from any page.
  Propose: add to `Связанные разборы` in [[papers/vaswani-2017-attention]].

### Tag-index inconsistency (N)
- `papers/su-2021-roformer.md` has tag `positional-encoding` but no entry
  under that tag group in `wiki/index.md`. Propose: add the link.

### Contradictions (N)
- [[papers/a]] reports metric X = 0.82; [[papers/b]] cites the same paper
  as X = 0.80. Propose: reconcile or flag as different eval settings.

## Editorial

### Stale claims (N)
- `papers/scaling-laws.md` references "current SOTA" without a date.
  Propose: add citation date.

### Voice drift (N)
- `lectures/karpathy-makemore-3.md`: "This is a fascinating method..." — propose rewrite.

### Oversized pages (N)
- `papers/vaswani-2017-attention.md` (820 lines). Suggested split: extract
  «Multi-head attention variants» as a separate breakdown.

## Suggested next moves

- {1–3 concrete next steps: ingest specific source, fix specific frontmatter,
  rebuild tag-index entries}
```

---

## Step 5 — Wait for steering

Stop after the report. Do not edit anything beyond:

- Auto-fixable frontmatter (lowercasing a tag, padding missing `updated`).
- Rebuilding the index if explicitly opted in.

For everything else, the user picks which findings to act on. Treat the report as a menu.

---

## Step 6 — Apply approved fixes; log

Apply only the fixes the user approved. Keep edits surgical — don't refactor adjacent things you noticed in passing (note them for the next lint pass).

Append one log entry summarising the lint run:

```markdown
## [YYYY-MM-DD] lint | wiki audit

- **Findings:** B blockers, S structural, E editorial
- **Fixed in this pass:** {short list of pages touched}
- **Deferred:** {short list — what the user chose not to act on now}
- **Suggested next:** {top 1–3 carry-overs}
```

---

## What this skill is NOT

- Not an ingest workflow. Lint never reads new raw sources. If a finding requires new information, surface it as a suggested ingest target.
- Not a rewrite. Lint surfaces; the user decides what to rewrite. Aggressive auto-rewrites destroy trust in the wiki.
- Not exhaustive. Some problems (deep semantic contradictions, subtle voice issues) won't be caught by a single pass. That's fine — lint is repeated, not perfect.
