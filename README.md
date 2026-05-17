# ml_notes

A personal LLM-maintained ML obsidian wiki. Raw sources go into `raw/`; Claude reads them and incrementally builds a network of linked markdown pages in `wiki/`. Each new source enriches existing pages instead of being re-derived per query.

## Layout

```
raw/                # source documents (immutable)
  papers/           # arXiv PDFs
  clips/            # web articles
  lectures/         # slides, transcripts
  scratch/          # own notes
wiki/               # everything the LLM writes
  ml_concepts/      # ML ideas (attention, dropout)
  math_concepts/    # math objects with step-by-step walkthroughs
  methods/          # specific algorithms (AdamW, LoRA)
  topics/           # narrative primers across an area — entry point for a reader
  sources/          # one page per ingested document
  questions/        # open questions
  index.md          # flat catalog of all pages
  log.md            # chronological event log
CLAUDE.md           # schema, taxonomy, style rules
.claude/skills/     # ingest / query / lint / quiz workflows
```

You own `raw/` and `CLAUDE.md`. Claude owns `wiki/`.

## Setup

Open the repository as a vault in Obsidian — `[[wiki-links]]`, backlinks, and the graph view all depend on it.

## Workflow

Four operations, each invoked by asking Claude in plain language:

| Skill         | Trigger                                          | What it does                                              |
| ------------- | ------------------------------------------------ | --------------------------------------------------------- |
| `wiki-ingest` | "ingest this", "add this source"                 | Read a raw source, update concept/method pages, log it    |
| `wiki-query`  | "what does the wiki say about X", any ML question | Synthesize an answer from wiki pages with citations       |
| `wiki-lint`   | "lint the wiki", "audit"                         | Scan for orphans, broken links, contradictions            |
| `wiki-quiz`   | "quiz me", "interview prep"                      | Generate a test (MCQ, open questions, paper problems)     |

## Working on this repo

- Read the wiki: start from `wiki/topics/` — these are narrative primers that walk through an area and link into the concept, method, and source pages.
- Add a source: drop the file under the right `raw/` subdirectory, then ask Claude to ingest it.
- Ask a question: phrase it directly — Claude reads `wiki/index.md` first, then drills into relevant pages.
- Health-check: run `wiki-lint` every 10–20 ingests.
- Never edit anything under `raw/` after committing it — corrections live in `wiki/` pages that link back to the source.

See `CLAUDE.md` for the full schema, page templates, and style rules.
