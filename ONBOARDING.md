# Onboarding — ML Notes Wiki

A personal LLM-maintained wiki on machine learning. Sources go in `raw/`, structured explanations go in `wiki/`. The site deploys via Quartz + Vercel.

## First day — 30 minutes

1. Read `CLAUDE.md` (5 min) — repo map and principles.
2. Read `.claude/role.md` (5 min) — how the LLM writes.
3. Open `wiki/index.md` and a finished page like `wiki/ml_concepts/attention/self-attention.md` (10 min) — see the output you are working toward.
4. Open `.autodoc/index.md` (5 min) — see how session insights look.
5. Read this file to the end (5 min).

## Your daily loop

| Situation | What you do |
|---|---|
| You found an article / paper / lecture | Drop the file into `raw/{papers\|clips\|lectures\|scratch}/<filename>` |
| You want a structured breakdown of it | `/wiki-ingest raw/<kind>/<filename>` |
| You want to find something in the wiki | `/wiki-query "<your question>"` |
| You are about to commit | `/wiki-lint` |
| You want to test your memory | `/wiki-quiz <topic>` |
| You are closing the session and learned something | `/autodoc` |

## Gates where Claude stops and waits for you

- After **takeaways** (phase 4 of `/wiki-ingest`) — Claude shows what it plans to write; you approve or steer.
- Before any **commit** — Claude proposes the message; you approve.
- In `/autodoc` — Claude proposes draft insights before appending.

## What Claude never does on its own

- `git push` — push is your action, always.
- Edit or delete files in `raw/`.
- AI-generate images. Only mermaid, matplotlib, or attributed source cut-outs are allowed.
- Commit more than 300 lines in one commit — it splits into atomic commits instead.

## Structure quick map

```
wiki/ml_concepts/          # flat: attention, RoPE, ELBO, diffusion, flow matching, ...
wiki/math_concepts/        # flat: KL divergence, Jensen's inequality, rotation matrix 2D, ...
wiki/methods/              # flat: transformer, VAE, RoPE, DyPE, mean flow, ...
wiki/topics/               # flat: narrative primers
wiki/sources/              # flat: one page per ingested source
wiki/questions/            # flat: open questions
```

Everything stays flat. One concept = one file in the right type folder.

## Where to edit the rules

| You want to change | Edit |
|---|---|
| The voice / how Claude writes | `.claude/role.md` |
| Language policy (banned phrases, calques) | `.claude/rules/01-language-policy.md` |
| Commit policy | `.claude/rules/02-commit-policy.md` |
| Illustration policy | `.claude/rules/03-illustration-policy.md` |
| Frontmatter schema | `.claude/rules/04-frontmatter-schema.md` |
| Page templates | `.claude/skills/_shared/page-templates.md` |
| Russian style guide | `.claude/skills/_shared/russian-style.md` |
| Illustration manual (deep) | `.claude/skills/_shared/illustration-policy.md` |
| The ingest workflow | `.claude/skills/wiki-ingest/SKILL.md` |

## Local preview

```bash
cd publish && npx quartz build --serve
```

Then open <http://localhost:8080>.

## Deploy

Vercel watches `main`. **Push to `main` = publication.** Run `/wiki-lint` before pushing.

## Where to write open questions

`wiki/questions/<slug>.md`. Use the question template from `.claude/skills/_shared/page-templates.md`.

## Open this repo as its own workspace

Open `knowledge_sharing_wiki/` as the workspace root. Do not open a wrapping project (e.g., a parent ML workspace) and edit from there — parent `CLAUDE.md` files will load and pollute context with unrelated rules.
