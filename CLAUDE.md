# CLAUDE.md — ML Notes Wiki

Personal LLM-maintained wiki on machine learning. You read raw sources, integrate knowledge into a structured network of pages, illustrate non-trivial ideas, and check Russian style. The wiki compounds — every new source enriches existing pages.

## Read first

1. `.claude/role.md` — who you are, how you write, what you do not do
2. `.claude/rules/` — auto-loaded; verify your output complies
3. `wiki/index.md` — what already exists
4. `.autodoc/index.md` — insights from previous sessions

## Layout

```
.
├── CLAUDE.md             # this file
├── AGENTS.md             # pointer to this file
├── ONBOARDING.md         # 30-min onboarding for new colleagues
├── .autodoc/             # persistent session memory
├── .claude/
│   ├── role.md
│   ├── rules/            # language, commit, illustration, frontmatter
│   ├── agents/           # wiki-source-researcher
│   └── skills/           # wiki-ingest, wiki-query, wiki-lint, wiki-quiz, autodoc, _shared/
├── raw/                  # source documents (immutable)
│   ├── papers/  clips/  lectures/  scratch/
├── wiki/                 # everything you write
│   ├── index.md  log.md
│   ├── ml_concepts/{attention,probabilistic,generative}/...
│   ├── math_concepts/    # flat
│   ├── methods/{architectures,attention,distillation,generative,inference,positional}/...
│   ├── topics/  sources/  questions/      # flat
└── publish/              # Quartz site; deploys to Vercel from main
```

## Layers

- `raw/` — immutable, you read only.
- `wiki/` — you write and maintain.
- `.claude/` — configuration; read freely, propose changes through commits.

## Commands

| You want to | Command |
|---|---|
| Ingest a source | `/wiki-ingest raw/<path>` |
| Ask the wiki | `/wiki-query "<question>"` |
| Lint before commit | `/wiki-lint` |
| Quiz yourself | `/wiki-quiz <topic>` |
| Save session insights | `/autodoc` |

## Principles

1. **Integrate, not summarise.** Every source revises the network of concept pages, not just adds an isolated source page.
2. **Illustrate non-trivial ideas.** Mermaid, matplotlib, or attributed source cut-outs. **AI image generation is forbidden** (rules/03).
3. **Russian prose, English structure.** Body in Russian; headings, slugs, tags, frontmatter in English (rules/01).
4. **Atomic commits ≤ 300 lines.** Conventional commits with scope (rules/02).
5. **No `git push` without explicit user action.** Ever.

## Deploy

Quartz + Vercel. Push to `main` triggers deploy. See `publish/README.md`.

## Open this repo as its own workspace

Open `knowledge_sharing_wiki/` as the top-level workspace, not a subfolder inside a larger project. Otherwise parent CLAUDE.md files (e.g., from a wrapping ML/DS workspace) load and pollute context with unrelated rules.
