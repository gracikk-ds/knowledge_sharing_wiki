---
name: wiki-ingest
description: Process a new raw source into the wiki — read it, discuss takeaways, create or update concept/method/source pages, refresh the index, append to the log. Use whenever the user wants to add a source to the wiki, says "ingest", "add this source", "process this", "file this into the wiki", or hands you a path under `raw/`.
---

# wiki-ingest

Workflow for ingesting one raw source into the wiki. Read this whole skill before acting; the order matters.

The goal is **integration, not summarisation**. A good ingest revises the network of concept pages, not just adds a source page in isolation.

---

## Checklist (mirror as TodoWrite tasks)

1. **Locate and read the source.** Confirm path under `raw/`. Read it fully. For PDFs, use the Read tool's PDF support; for long PDFs, page through in ranges.
2. **Brief reconnaissance.** Skim `wiki/index.md` and identify which existing pages (if any) the source touches. List them mentally before reading the source again.
3. **Discuss takeaways with the user.** Present 3–7 bullets in your own words and ask for steering before editing anything. Stop here and wait.
4. **Plan the edits.** Decide: which concept/method pages get created, which get updated, what the source page says, what (if anything) contradicts existing content.
5. **Apply edits in this order:** create/update concept and method pages → write the source page → update `wiki/index.md` → append a log entry.
6. **Report what changed.** List every page touched. Surface contradictions and any newly-orphaned `[[stub-links]]` so the user can decide whether to ingest more sources or run `wiki-lint`.

---

## Step 1 — Locate and read the source

- Confirm the source lives in `raw/` (papers/, clips/, scratch/, lectures/). If the user dropped a file elsewhere, move it into the right subdirectory before proceeding (or ask).
- Read the full text. For PDFs, use the Read tool's `pages` parameter for anything over 10 pages.
- For markdown clips that reference images on disk: read the markdown first, identify which images are load-bearing (figures, diagrams, equations), then read those images individually. Don't read all images by default — only the ones whose context the prose can't carry alone.
- Take silent notes as you read. Do not start writing wiki pages yet.

---

## Step 2 — Brief reconnaissance

Open `wiki/index.md` and identify candidate pages the source might touch. Make a short mental list of:

- Concept pages that already exist and are likely to be revised.
- Concepts mentioned in the source that **don't** have pages yet.
- Methods (algorithms) introduced or referenced.
- Existing claims in the wiki that this source might confirm, refine, or contradict.

This costs you one extra read but prevents the most common ingest failure: writing a source page that lives in isolation and never updates the concepts.

---

## Step 3 — Discuss takeaways with the user

Present takeaways in plain prose, in your own words. Format:

```
Source: {title} ({source_kind}, {date})

Takeaways:
- {bullet 1}
- {bullet 2}
...

Likely wiki impact:
- New: [[concept-x]], [[method-y]]
- Update: [[concept-a]] (add ...), [[concept-b]] (refine ...)
- Contradicts: {existing claim, if any}

Anything you want me to emphasise or skip before I file this?
```

**Stop and wait for the user's response.** Do not write any wiki pages in this step. The user may redirect emphasis, point out things you missed, or say "skip section X". If the user says "go", proceed to step 4.

If the user has explicitly asked you to work without stopping for clarifying questions, still emit the takeaways block — but immediately proceed to step 4 unless something is genuinely ambiguous.

---

## Step 4 — Plan the edits

For each page you're about to touch, decide:

- **Status transition.** Stub → draft? Draft → mature? Stay put?
- **Section impact.** Are you adding to "Motivation", revising "Formal description", adding to "Variations", or flagging in "Open questions"? On topic primers, are you extending "The setting" / "Core ideas" / "Methods that grow from these ideas"?
- **Contradictions.** If this source disagrees with something already in the wiki, prefer one of: (a) note the disagreement in both the source page and the concept page, with attributions to each source; (b) revise the concept page if the new source is clearly more authoritative — but say so in the log. Do not silently overwrite.
- **Stub policy.** If the source mentions ten concepts and you can't write all ten properly, write stubs for the ones you can't fill out and a full draft for the central ones. Stubs are fine; missing links are worse.

Write the plan as a short list before editing. You can keep this in your working memory; no need to share it with the user unless the user asked to preview changes.

---

## Step 5 — Apply edits

**Order matters.** Do concept/method pages first, source page second, index third, log last. This way the source page can reference its real impact, and the log entry can list every page actually touched.

### 5a. Create / update concept and method pages

Follow the templates in `CLAUDE.md`. For each page:

- If creating: full frontmatter, all standard sections (even if some are short or empty).
- If updating: bump `updated` to today's date, increment `sources` if you added a new citation, bump `status` if appropriate, then edit the relevant sections.
- Maintain alphabetical or thematic order within sections (e.g., "Variations and related concepts" usually reads in order of relatedness, not alphabetical).
- Every claim that came from this source must cite back to it via `[[sources/{slug}]]`.

### 5b. Write the source page

Use the source-page template in `CLAUDE.md`. Required:

- `source_path` pointing to the raw file.
- `source_kind`, `source_date`, `ingested` (today).
- "Concepts touched" lists every concept page you edited, with one-line descriptions of what the source contributed.
- "Contradictions and revisions" section — even if it just says "none".

### 5c. Update `wiki/index.md`

- Add new pages to their type sections.
- Update one-line summaries for any page whose summary changed.
- Bump the `_Last updated: YYYY-MM-DD_` line.
- Keep alphabetical order within each section.

### 5d. Append to `wiki/log.md`

Use this exact heading format (the leading `##` and the bracketed date make the log grep-friendly):

```markdown
## [YYYY-MM-DD] ingest | {short source title}

- **What:** {one-line description of the source}
- **Pages touched:** [[a]], [[b]], [[c]]
- **Notes:** {contradictions, questions raised, things to revisit; omit if none}
```

---

## Step 6 — Report what changed

After the writes complete, post a concise summary to the user:

```
Ingested: {title}

Wrote:
- [[a]] (new, draft)
- [[b]] (updated, +1 source)
- [[sources/{slug}]] (new)

Stubs created (good ingest targets next):
- [[c]], [[d]]

Open questions surfaced:
- [[questions/...]]

Log entry: [YYYY-MM-DD] ingest | {short title}
```

Do **not** include a "what I learned" summary at this point — that lives on the source page now, where it belongs.

---

## Edge cases

- **The source is already in the wiki.** Check the `sources/` directory before reading. If a source page already exists, ask the user whether to re-ingest (overwrite), incrementally extend, or skip.
- **The source is too long for one pass.** Ingest chapter-by-chapter or section-by-section, each as its own ingest with its own log entry. Use distinct source-page slugs (`textbook-ch3`, `textbook-ch4`).
- **The source is mostly noise.** Some scratch notes are 90% half-formed. Be selective: ingest what's actually new or clarifying; skip the rest. Say so on the source page.
- **The source contradicts an existing `mature` page.** Don't downgrade silently. Note the contradiction in both pages and consider opening a `[[questions/...]]` page.
- **The source is empty / a thin abstract.** File a stub source page with what little you can extract, but don't update concept pages on thin evidence.

---

## What this skill is NOT

- Not a query workflow. If the user asks "what does the wiki say about X" without handing you a source, use `wiki-query` instead.
- Not a lint workflow. If you discover lots of orphan stubs or contradictions across the wiki during ingest, surface them and suggest `wiki-lint` rather than fixing them in this session.
- Not a chat. The user wants the wiki to compound. Every ingest should leave the wiki measurably richer, not just longer.
