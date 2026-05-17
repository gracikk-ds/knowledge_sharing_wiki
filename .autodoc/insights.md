# Session Insights

Append-only log of insights captured by the `autodoc` skill. One entry per session that produced something worth keeping.

Format of each entry:

```
## [YYYY-MM-DD] <one-line title>

**Category:** <Discovery | Wiki structure | Skill/tool issue | Gotcha>

<body — 1-5 paragraphs>
```

---

## [2026-05-17] Wiki overhaul scope locked

**Category:** Wiki structure

Spec `docs/superpowers/specs/2026-05-17-wiki-overhaul-design.md` defines the
fundament: role, hierarchical structure, rewritten CLAUDE.md, ingest v2,
autodoc, ONBOARDING. Hooks and skill-updater are explicitly out of scope —
they are in the "Next iteration" section of the spec and ship as separate
cycles.
