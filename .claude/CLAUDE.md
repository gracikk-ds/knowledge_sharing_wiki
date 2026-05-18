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
├── .autodoc/             # persistent session memory
├── .claude/
│   ├── CLAUDE.md         # this file — main agent instructions
│   ├── role.md
│   ├── rules/            # language, commit, illustration, frontmatter
│   ├── agents/           # wiki-source-researcher
│   ├── skills/           # wiki-ingest, wiki-query, wiki-lint, wiki-quiz,
│   │                     # onboard, autodoc, write-russian, skill-updater,
│   │                     # _shared/
│   └── proposed-changes/ # skill-updater drafts (gitignored)
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
| Lint before push to main | `/wiki-lint` |
| Quiz yourself | `/wiki-quiz <topic>` |
| Walk through onboarding interactively | `/onboard` |
| Save session insights | `/autodoc` |
| Propose updates to `.claude/` itself | `/skill-updater` (only when the user asks, or when `.autodoc/insights.md` has ≥ 5 new entries since the last apply commit) |

## Principles

1. **Integrate, not summarise.** Every source revises the network of concept pages, not just adds an isolated source page.
2. **Illustrate non-trivial ideas.** Mermaid, matplotlib, or attributed source cut-outs. **AI image generation is forbidden** (rules/03).
3. **Russian prose, English structure.** Body in Russian; headings, slugs, tags, frontmatter in English (rules/01).
4. **Atomic commits ≤ 300 lines.** Conventional commits with scope (rules/02).
5. **You may push.** `git push` is allowed without per-action approval. Before pushing to `main` (Vercel deploys from it), run `/wiki-lint` and fix blockers. Force-push and pushing `main` from a feature branch still need explicit user OK.
6. **You do not edit your own instructions autonomously.** Changes to `.claude/role.md`, `.claude/rules/*.md`, and `.claude/skills/*/SKILL.md` go through `/skill-updater` — predict → user review → apply. The skill activates only when the user explicitly asks, or when `.autodoc/insights.md` has ≥ 5 new entries since the last skill-updater apply commit AND that commit is ≥ 14 days old.
7. **Git hooks** (`bash .githooks/install.sh` once):
   - `pre-commit`: frontmatter check on wiki pages + soft warning on commits > 300 lines.
   - `pre-push`: fires on every push, every branch. If ≥ 2 substantive commits (wiki/, .claude/, raw/) landed since the last `chore(autodoc):` commit reachable from HEAD, the hook prompts to run `/autodoc` first. Reply `y` to push anyway. The hook can't run Claude — it nudges; you run the skill.

## Deploy

Quartz + Vercel. Push to `main` triggers deploy. See `publish/README.md`.

## Open this repo as its own workspace

Open `knowledge_sharing_wiki/` as the top-level workspace, not a subfolder inside a larger project. Otherwise parent `.claude/CLAUDE.md` files (e.g., from a wrapping ML/DS workspace) load and pollute context with unrelated rules.
