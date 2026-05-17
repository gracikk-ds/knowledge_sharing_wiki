# Onboarding — ML Notes Wiki

A personal LLM-maintained wiki on machine learning. Sources go in `raw/`, structured explanations go in `wiki/`. The site deploys via Quartz + Vercel.

## First day — 30 minutes

1. Read `CLAUDE.md` (5 min) — repo map and principles.
2. Read `.claude/role.md` (5 min) — how the LLM writes.
3. Open `wiki/index.md` and browse one breakdown under `wiki/papers/` or `wiki/knowledge-sharings/` (10 min) — see the output you are working toward.
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
wiki/papers/             # paper breakdowns:  su-2021-roformer.md
wiki/lectures/           # lecture breakdowns: karpathy-makemore-3.md
wiki/clips/              # blog/article breakdowns: illustrated-transformer-jay-alammar.md
wiki/knowledge-sharings/ # KS meeting breakdowns: 2026-05-15-attention-deep-dive-by-grigoriy.md
wiki/index.md            # entry point: recent / by kind / by tag
wiki/log.md              # append-only chronological event log
```

One page per source. Concepts live *inside* the breakdown; there are no separate concept pages.

To find «everything about RoPE», open `wiki/index.md`, scroll to «By tag», find the line for `positional-encoding`. It lists every breakdown that touches the concept.

## Worked example

See `docs/superpowers/specs/2026-05-18-wiki-source-breakdowns-design.md` §9 for a full example of a paper breakdown (the RoFormer/RoPE paper). It shows the template on a real source — what each section actually looks like, what kind of mermaid diagram qualifies as «идея в одной картинке», how `где: …` lists work under formulas, how «Связанные разборы» links work.

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

Inline on the breakdown page in the «Открытые вопросы» section (optional, between «Как это работает» and «Вывод»). There is no separate questions folder — open threads live attached to the source that raised them.

## Open this repo as its own workspace

Open `knowledge_sharing_wiki/` as the workspace root. Do not open a wrapping project (e.g., a parent ML workspace) and edit from there — parent `CLAUDE.md` files will load and pollute context with unrelated rules.
