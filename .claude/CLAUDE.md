# .claude/CLAUDE.md — ML Notes Wiki

Personal LLM-maintained wiki on machine learning. You read raw sources, integrate knowledge into a structured network of pages, illustrate non-trivial ideas, and check Russian style. The wiki compounds — every new source enriches existing pages.

## Read first

1. `.claude/role.md` — who you are, how you write, what you do not do
2. `.claude/rules/` — auto-loaded; verify your output complies
3. `wiki/index.md` — what already exists
4. `.autodoc/index.md` — insights from previous sessions

## Layout

```
.
├── AGENTS.md             # pointer to .claude/CLAUDE.md for non-Claude tooling
├── README.md             # project overview (Russian)
├── ONBOARDING.md         # text reference; /onboard for the interactive walkthrough
├── .autodoc/             # persistent session memory
├── .claude/
│   ├── CLAUDE.md         # this file — main agent instructions
│   ├── role.md
│   ├── rules/            # language, commit, illustration, frontmatter
│   ├── agents/           # wiki-source-researcher
│   └── skills/           # wiki-ingest, wiki-query, wiki-lint, wiki-quiz, onboard, autodoc, _shared/
├── raw/                  # source documents — LOCAL ONLY (gitignored)
│   ├── papers/  clips/  lectures/  scratch/  knowledge-sharings/
├── wiki/                 # source breakdowns: one page per paper/lecture/clip/KS
│   ├── index.md          # landing page + recent / by-kind / by-tag
│   ├── tags.md           # master tag registry
│   ├── log.md            # chronological event log
│   ├── papers/           # paper breakdowns
│   ├── lectures/         # lecture breakdowns
│   ├── clips/            # blog/article breakdowns
│   ├── knowledge-sharings/   # internal KS meeting breakdowns
│   └── static/figures/   # flat: <slug>-<figure>.png (PNGs only)
└── publish/              # Quartz site; deploys to Vercel from main
```

## Layers

- `raw/` — local-only (gitignored). User adds source files here; Claude reads but does not commit. Subdirectory structure (papers/lectures/clips/knowledge-sharings/scratch/) is the only thing tracked.
- `wiki/` — you write and maintain. Source-of-truth for the published site.
- `.claude/` — configuration; read freely, propose changes through commits.

## Commands

| You want to | Command |
|---|---|
| Ingest a source | `/wiki-ingest raw/<path>` |
| Ask the wiki | `/wiki-query "<question>"` |
| Lint before commit | `/wiki-lint` |
| Quiz yourself | `/wiki-quiz <topic>` |
| Walk through onboarding interactively | `/onboard` |
| Save session insights | `/autodoc` |

## Principles

1. **Integrate, not summarise.** Every source revises the network of concept pages, not just adds an isolated source page.
2. **Illustrate non-trivial ideas.** Mermaid, matplotlib, or attributed source cut-outs. **AI image generation is forbidden** (rules/03).
3. **Russian prose, English structure.** Body in Russian; headings, slugs, tags, frontmatter in English (rules/01).
4. **Atomic commits ≤ 300 lines.** Conventional commits with scope (rules/02).
5. **You may push.** `git push` is allowed without per-action approval. Run `/wiki-lint` before pushing to `main` — it deploys to Vercel.

## Deploy

Quartz + Vercel. Push to `main` triggers deploy. See `publish/README.md`.

## Open this repo as its own workspace

Open `knowledge_sharing_wiki/` as the top-level workspace, not a subfolder inside a larger project. Otherwise parent `.claude/CLAUDE.md` files (e.g., from a wrapping ML/DS workspace) load and pollute context with unrelated rules.
