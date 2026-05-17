# AGENTS.md

LLM-maintained ML wiki. Sources land in `raw/` (local-only, gitignored); breakdowns get written to `wiki/` by Claude through skills; the site is built with Quartz and deployed to Vercel from `main`.

Full Claude instructions live in [`.claude/CLAUDE.md`](.claude/CLAUDE.md). The map below is the entry-point for non-Claude agents (Codex, OpenCode, Gemini, Cursor, etc.) that need to find their way around.

## Where to read first

1. [`.claude/role.md`](.claude/role.md) — who the wiki author is, voice, what they don't do.
2. [`.claude/rules/`](.claude/rules/) — auto-loaded by Claude; verify output complies.
   - `01-language-policy.md` — Russian prose + English structure, 3-tier terminology hierarchy.
   - `02-commit-policy.md` — conventional commits, ≤ 300 lines per commit, push policy.
   - `03-illustration-policy.md` — mermaid / matplotlib / source cut-outs, no AI-generated images.
   - `04-frontmatter-schema.md` — required YAML fields per source kind.
3. [`wiki/index.md`](wiki/index.md) — landing page; lists what already exists.
4. [`wiki/tags.md`](wiki/tags.md) — live tag registry; the source of truth for the tag whitelist.
5. [`.autodoc/index.md`](.autodoc/index.md) — session insights from prior runs (skip if missing).

## Skills

User-invocable commands live under [`.claude/skills/`](.claude/skills/). Each has its own `SKILL.md`.

| Skill | Purpose |
|---|---|
| `wiki-ingest` | Turn one source under `raw/` into one breakdown page (9 phases: pre-flight → read source → extract embedded images → optional research dispatch → align plan with user → write page → produce figures → lint pass → update index/tags/log → commit). |
| `wiki-query` | Answer questions against the wiki. Resolves by tag and slug; cites pages inline. |
| `wiki-lint` | Audit pass: frontmatter, broken `[[wiki-links]]`, orphans, tag-index drift, tag-registry consistency. Reports findings; the user picks what to fix. |
| `wiki-quiz` | Generate multiple-choice / open / paper-and-pen quizzes from the wiki; logs sessions to `wiki/log.md`. |
| `onboard` | 7-phase interactive walkthrough for first-time users of the repo. |
| `autodoc` | Append session insights to `.autodoc/`. Run at the end of a substantive session. |
| `write-russian` | Apply the Russian voice rules to an arbitrary piece of text. |

## Agents

Dispatched by skills, not invoked directly.

| Agent | Dispatched by | Purpose |
|---|---|---|
| `wiki-source-researcher` | `wiki-ingest` (phase 4) | Web research when the primary source has a gap that blocks a clear explanation. Returns a structured report; does not edit files. |

## Layout

```
.
├── AGENTS.md             # this file
├── README.md             # project overview (Russian)
├── ONBOARDING.md         # text reference; /onboard for the interactive walkthrough
├── .claude/              # agent config — read freely
│   ├── CLAUDE.md
│   ├── role.md
│   ├── rules/
│   ├── agents/
│   └── skills/
├── raw/                  # source documents — LOCAL ONLY (gitignored)
│   └── papers/  lectures/  clips/  knowledge-sharings/  scratch/
├── wiki/                 # breakdowns: one source = one page
│   ├── index.md
│   ├── tags.md
│   ├── log.md
│   ├── papers/  lectures/  clips/  knowledge-sharings/
│   └── static/figures/   # flat PNGs: <slug>-<figure>.png
├── publish/              # Quartz site; deploys to Vercel from main
└── .autodoc/             # persistent session memory
```

## Commit and push

- Conventional commits with scope (`feat(wiki)`, `docs(skill)`, `chore(autodoc)`, etc.).
- One commit ≤ 300 lines; split big work into atomic commits.
- Push is allowed without per-action approval. Force-push and pushing to `main` from a feature branch still need an explicit user OK.
- `main` deploys to Vercel — run `/wiki-lint` before pushing to `main`.

## Open this repo as its own workspace

Open `knowledge_sharing_wiki/` as the top-level workspace, not a subfolder inside a larger project. Otherwise parent `.claude/CLAUDE.md` files (e.g., from a wrapping ML/DS workspace) load and pollute context with unrelated rules.
