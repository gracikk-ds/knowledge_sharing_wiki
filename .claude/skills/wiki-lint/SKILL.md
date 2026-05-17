---
name: wiki-lint
description: Health-check the wiki — scan for orphan pages, broken links, missing concept pages, contradictions between pages, stale claims, and frontmatter inconsistencies. Report findings and let the user pick what to act on. Use when the user says "lint the wiki", "audit the wiki", "health check", or asks for a wiki cleanup. Run periodically (every 10–20 ingests is a reasonable cadence).
---

## Pre-flight

- [ ] Read `.claude/role.md`
- [ ] Read `.claude/rules/04-frontmatter-schema.md`

# wiki-lint

Workflow for auditing the wiki's health. The goal is to **surface problems clearly, propose concrete fixes, and let the user decide what to act on**. Don't silently fix structural problems; report them first.

A lint pass is not the same as an ingest. It uses no new sources — it only analyses what's already there.

---

## Checklist (mirror as TodoWrite tasks)

1. **Take inventory.** Count pages by type; spot-check the index for completeness.
2. **Run the checks** (see Checks section below). Each check produces zero or more findings.
3. **Group findings** by severity: blockers (broken links, frontmatter errors), structural (orphans, missing pages), editorial (stale claims, contradictions, voice drift).
4. **Report.** Present findings in a single structured report. Suggest a concrete fix for each.
5. **Wait for user steering.** Don't auto-fix anything beyond trivial frontmatter or index hygiene. The user picks what to act on.
6. **Apply approved fixes.** Edit pages, update index, append a single lint log entry summarising the run.

---

## Step 1 — Inventory

Use the Bash tool to count and list:

```bash
# from wiki/
find ml_concepts/ math_concepts/ methods/ topics/ sources/ questions/ -name "*.md" 2>/dev/null | sort
wc -l index.md log.md
grep -c "^## \[" log.md   # number of log entries
```

Cross-reference:

- Does every page in `ml_concepts/`, `math_concepts/`, etc. appear in `index.md`? Use `grep` or `comm`.
- Does every entry in `index.md` correspond to a real file?

This catches drift between index and filesystem early.

---

## Step 2 — Checks

Run these checks in order. Each section below specifies *how* to detect the problem, *why* it matters, and *what to propose* as a fix.

### Check 1: broken `[[wiki-links]]`

**How:** for every `[[link]]` in every wiki page, confirm a target page exists. Use a grep-and-check loop. A link `[[ml_concepts/foo]]` should match `wiki/ml_concepts/foo.md`. A bare `[[foo]]` should match any of `wiki/{ml_concepts,math_concepts,methods,topics,sources,questions}/foo.md`.

**Why:** broken links are silent rot. Obsidian shows them as red, but if nobody opens the page they sit there forever.

**Propose:** for each broken link, classify as:

- **Stub-worth:** the concept genuinely deserves a page — propose creating a stub.
- **Renamed:** the target was renamed; fix the link to point to the new slug.
- **Spurious:** the link is to something that doesn't make sense as a wiki page — remove it.

### Check 2: orphan pages

**How:** a page is an orphan if no other wiki page links to it AND it's not linked from `index.md`. (Index links don't count as "real" backlinks for this check.) Walk every page's outgoing links and build the inbound set per target.

**Why:** orphans are pages the wiki has forgotten. Either they belong in a topic page, they're stale, or they need their cross-links restored.

**Propose:**

- **Orphan stub:** suggest a parent topic page to link from.
- **Orphan mature page:** suggest 2–3 specific pages that should link to it (based on tags / content).
- **Orphan source:** likely the concept pages weren't updated when this source was ingested. Flag for re-ingest.

### Check 3: missing concept pages

**How:** for every `[[ml_concepts/x]]` or `[[math_concepts/x]]`-style link to a page that doesn't exist yet, list the targets sorted by how many pages reference them. Track both types separately — a missing math concept is a different ingest signal than a missing ML concept.

**Why:** these are exactly the next ingest targets. A concept referenced from five pages but lacking its own page is screaming to be written.

**Propose:** rank the top 5–10 missing concept pages by inbound reference count. Suggest a quick ingest plan for each (or "write a stub from existing context").

### Check 4: stale claims

**How:** scan pages for hedging language and date-bound claims. Specifically:

- Claims of "state-of-the-art" or "current best" with no date.
- Numerical results without a source link.
- Mentions of named models / methods that have since been superseded by a clearly-newer thing in another wiki page (use the log to spot recency).

**Why:** ML moves fast. A page that says "GPT-3 is the largest model" ages badly.

**Propose:** flag the page and section, suggest specific edits (add date, add citation, mark as historical).

### Check 5: contradictions

**How:** for each concept page, look for claims that other pages disagree with. Common shapes:

- Two source pages cite the same paper but report different numbers.
- A concept page says "X is required" but another page describes a method without X.
- A topic page lists [[a]] and [[b]] as alternatives but one is described elsewhere as a special case of the other.

You won't catch all of these in a pass; flag the obvious ones.

**Why:** silent contradictions erode trust in the wiki.

**Propose:** for each contradiction, either (a) reconcile inline by adding context, (b) open a `[[questions/...]]` page, or (c) flag for the next ingest of a tie-breaking source.

### Check 6: frontmatter hygiene

Frontmatter rules are in `.claude/rules/04-frontmatter-schema.md`. Enforce all rules from that file.

**Why:** Dataview queries (and future tooling) depend on this being uniform.

**Propose:** auto-fix candidates only (lowercasing a tag, padding a missing `updated` field with the file's mtime). Anything substantive is a "user please review" item.

### Check 7: voice drift

**How:** sample 5–10 random pages and check for banned filler:

- "in conclusion", "in summary", "it is important to note", "let's dive in"
- "powerful", "fascinating", "revolutionised" (when describing the concept itself rather than its measured impact)
- Meta-commentary ("this page covers…", "this section discusses…")
- Bolded Q&A markers in Motivation sections or primer bodies: `**Question.**`, `**First attempt.**`, `**Catch.**`, `**Attempt 1.**`. These break the "motivated build-up" voice.
- Everyday-object metaphors in Motivation / primer prose (fishing, lakes, cooking, archery). The voice should be direct prose, not analogies.

**Why:** the wiki's quality bar erodes one page at a time if not policed.

**Propose:** quote the offending sentences with their file paths so the user can decide whether to rewrite.

### Check 8: page size

**How:** wc -l every page. Flag any page over 750 lines.

**Why:** long pages usually want to be split.

**Propose:** identify a natural split (a sub-concept that could become its own page) and suggest it.

### Check 9: index drift

**How:** compare `wiki/index.md` against the actual filesystem.

**Why:** the index is the LLM's table of contents during queries; if it's wrong, queries miss pages.

**Propose:** rebuild the affected index sections. This is one of the few fixes safe to auto-apply if the user opts in.

---

## Step 3 — Group findings

Bucket findings by severity:

| Severity | Bucket | Example |
|---|---|---|
| **Blocker** | Breaks the wiki's read path | Broken links, malformed frontmatter, index/filesystem drift |
| **Structural** | Affects discoverability or compounding | Orphans, missing concept pages, contradictions |
| **Editorial** | Affects quality / trust | Stale claims, voice drift, oversized pages |

---

## Step 4 — Report

Single structured report, in this order. Be concise. Don't pad sections with "no findings" if there's nothing to report — drop the empty sections instead.

```markdown
# Wiki Lint — YYYY-MM-DD

Inventory: {C concepts, M methods, T topics, S sources, Q questions}
Log entries: N

## Blockers

### Broken links (N)
- [[ml_concepts/foo]] in `methods/bar.md` → target missing. Propose: stub
  `ml_concepts/foo`.
- ...

### Frontmatter issues (N)
- `ml_concepts/baz.md` — missing `status` field. Propose: set to `draft`.

### Index drift (N)
- `wiki/index.md` lists [[x]] but file is gone. Propose: remove entry.

## Structural

### Orphans (N)
- [[ml_concepts/lonely]] — no inbound links from concept/method pages.
  Propose: link from [[topics/related-topic]].
- ...

### Missing concept pages (top N)
- `[[ml_concepts/momentum]]` — referenced by 4 pages, no page exists.
  Propose: write stub from existing context (sources A, B).
- `[[math_concepts/kl-divergence]]` — referenced by 3 pages, no page exists.
  Propose: ingest a math source or write step-by-step from existing context.
- ...

### Contradictions (N)
- [[ml_concepts/lr-warmup]] says X; [[sources/paper-y]] reports Y.
  Propose: reconcile by adding regime context.

## Editorial

### Stale claims (N)
- `ml_concepts/scaling-laws.md` references "current SOTA" without a date.
  Propose: add citation date.

### Voice drift (N)
- `methods/adamw.md`: "This is a fascinating method that revolutionised..."
  — propose rewrite.

### Oversized pages (N)
- `ml_concepts/attention.md` (612 lines). Suggested split: extract "Multi-head
  variants" into `ml_concepts/multi-head-attention.md`.

## Suggested next moves

- {1–3 concrete next steps: ingest specific source, write specific stub,
  run a focused refactor}
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
