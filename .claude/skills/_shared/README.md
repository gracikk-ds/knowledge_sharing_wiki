# `_shared/` — Read-on-Demand References

This folder holds reference documents that several skills read with explicit `Read` calls. They are **not** auto-loaded.

## Convention

A skill that depends on a `_shared/` reference does this at pre-flight:

```
1. Read `.claude/role.md`
2. Read `.claude/skills/_shared/page-templates.md`
3. Read `.claude/skills/_shared/illustration-policy.md`
4. Read `.claude/skills/_shared/russian-style.md`
```

Each `Read` is one explicit step in the skill's checklist.

## Why not auto-load?

These files are long (200-500 lines each). Auto-loading them all would burn context for every conversation. Skills load only what they need.

## Files

| File | Purpose | Loaded by |
|---|---|---|
| `page-templates.md` | Template A (source breakdown for paper/lecture/clip), Template B (knowledge-sharing variant), cross-cutting rules (term introduction, formula annotation, code-formula bridge) | `wiki-ingest` phase 5 |
| `illustration-policy.md` | Full manual with chooser logic for mermaid vs matplotlib vs cut-out | `wiki-ingest` phase 6 |
| `russian-style.md` | Detailed Russian style guide with examples | `wiki-ingest` phase 7 |

`.claude/role.md` lives at the `.claude/` root (not in `_shared/`) because it is shorter and conceptually a top-level identity file rather than a workflow reference.

## Adding a new `_shared/` file

Add it to the table above. Update the relevant skill's pre-flight checklist to read it. Do not implicitly couple a skill to a `_shared/` file without naming it in the skill's checklist.
