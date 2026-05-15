---
title: Wiki Log
type: log
created: 2026-05-15
updated: 2026-05-15
---

# Wiki Log

Append-only chronological log of operations on the wiki. Each entry starts with `## [YYYY-MM-DD] {verb} | {short title}` so it's grep-friendly:

```bash
grep "^## \[" wiki/log.md | tail -5     # last 5 entries
grep "^## \[.*\] ingest" wiki/log.md    # all ingests
```

Verbs: `ingest`, `query`, `lint`, `quiz`, `refactor`.

---

## [2026-05-15] init | wiki scaffolded

- **What:** Created CLAUDE.md schema, three project skills (wiki-ingest, wiki-query, wiki-lint), and wiki/ directory structure (concepts, methods, topics, sources, questions). Initialised empty index.md and this log.
- **Pages touched:** [[index]], [[log]]
- **Notes:** Vault is empty — ingest a first source to populate.

## [2026-05-15] ingest | Few-step Generative Models (Flow-Map models) lecture

- **What:** First content ingest. A 31-slide lecture on why diffusion is slow and the modern toolkit of flow-map methods (Consistency Models, Multistep CMs, ShortCut, Mean Flow). Sourced from `raw/lectures/flow-map-models.pdf`.
- **Pages touched:** [[sources/flow-map-models-lecture]] (new), [[topics/few-step-generative-models]] (new, draft), [[ml_concepts/flow-map]] (new, draft), [[ml_concepts/consistency-function]] (new, draft), [[ml_concepts/step-distillation]] (new, draft), [[ml_concepts/diffusion-model]] (new, stub), [[ml_concepts/flow-matching]] (new, stub), [[ml_concepts/probability-flow-ode]] (new, stub), [[ml_concepts/score-function]] (new, stub), [[methods/consistency-distillation]] (new, draft), [[methods/consistency-training]] (new, draft), [[methods/multistep-consistency-model]] (new, draft), [[methods/shortcut-model]] (new, draft), [[methods/mean-flow]] (new, draft), [[methods/progressive-distillation]] (new, stub), [[math_concepts/mean-flow-identity]] (new, draft), [[index]] (updated).
- **Notes:** Flow map is the unifying concept across the whole lecture; raised three open questions ([[questions/why-cant-cms-use-ode-solvers]], [[questions/how-is-mean-flow-time-derivative-computed]], [[questions/why-does-consistency-training-work-without-teacher]]). Background pages (diffusion-model, flow-matching, probability-flow-ode, score-function) deliberately left as stubs — a dedicated source will fill them. Final slide ("Айтишники всё!") is a meme sign-off, not technical content.

## [2026-05-15] ingest | ELBO and VAE lecture

- **What:** Lecture deriving ELBO from first principles (Jensen and Bayes routes), decomposing into reconstruction + regularisation, and walking through the full VAE training story (variational EM, amortised inference, reparameterization trick, closed-form Gaussian KL, final loss). Sourced from `raw/lectures/ELBO_and_VAE.md`.
- **Pages touched:** [[sources/elbo-and-vae-lecture]] (new), [[ml_concepts/elbo]] (new, draft), [[ml_concepts/latent-variable-model]] (new, draft), [[ml_concepts/variational-inference]] (new, draft), [[ml_concepts/amortized-variational-inference]] (new, draft), [[ml_concepts/reparameterization-trick]] (new, draft), [[math_concepts/kl-divergence]] (new, draft), [[math_concepts/jensens-inequality]] (new, draft), [[methods/vae]] (new, draft), [[methods/variational-em]] (new, draft), [[topics/variational-inference]] (new, draft), [[index]] (updated).
- **Notes:** Opens the variational-inference region of the wiki, disjoint from the existing flow-map / consistency-models cluster. The score-function estimator is mentioned only briefly on [[ml_concepts/reparameterization-trick]] and not given its own page — a dedicated source could expand it later. Topic page links to concept page via explicit `[[ml_concepts/variational-inference]]` to disambiguate from `[[topics/variational-inference]]`. No contradictions with existing pages.

## [2026-05-15] refactor | Narrative layer — topic primers, Motivation, Up next

- **What:** Schema and content refactor to add a narrative layer on top of the existing reference layer, addressing two problems: (1) no entry point for "study an area from scratch", (2) `## Intuition` sections jumped to formal answers without naming the motivating question. Plan at `/Users/asgordeev/.claude/plans/parallel-leaping-trinket.md`.
- **Schema (`CLAUDE.md`):** new topic template (primer form: The setting → Core ideas → Methods → Open threads → Reading order recap → Reading queue); ml_concept and method templates get `## Motivation` (replaces Intuition on ml_concept; new section on method) and `## Up next` footer; math_concept template's `## Plain-English statement` absorbs motivated build-up; Quality bar gains `### Motivation voice` and `### Up next footer` subsections; banlist extended with bolded Q&A markers and everyday-object metaphors. Topic page taxonomy row updated from "umbrella link map" to "narrative primer".
- **Skills:** [[.claude/skills/wiki-ingest/SKILL.md]] (Intuition reference updated); [[.claude/skills/wiki-lint/SKILL.md]] (Check 7 extended with Q&A markers and metaphors; new Check 7b — schema migration grep for residual `## Intuition`).
- **Topic primers (rewritten):** [[topics/variational-inference]], [[topics/few-step-generative-models]].
- **ml_concept Motivation + Up next:** [[ml_concepts/elbo]], [[ml_concepts/amortized-variational-inference]], [[ml_concepts/consistency-function]], [[ml_concepts/flow-map]], [[ml_concepts/latent-variable-model]], [[ml_concepts/reparameterization-trick]], [[ml_concepts/step-distillation]], [[ml_concepts/variational-inference]]. Stubs left as-is (no Intuition section to migrate): [[ml_concepts/diffusion-model]], [[ml_concepts/flow-matching]], [[ml_concepts/probability-flow-ode]], [[ml_concepts/score-function]].
- **math_concept Plain-English rewritten:** [[math_concepts/jensens-inequality]], [[math_concepts/kl-divergence]], [[math_concepts/mean-flow-identity]].
- **method Motivation + Up next:** [[methods/consistency-distillation]], [[methods/consistency-training]], [[methods/mean-flow]], [[methods/multistep-consistency-model]], [[methods/shortcut-model]], [[methods/vae]], [[methods/variational-em]]. Stub [[methods/progressive-distillation]] left as-is.
- **Bookkeeping:** [[index]] gains a `## Start here` section pointing at the two primers with their reading paths; alphabetical catalog below unchanged.
- **Voice contract:** all new Motivation sections, primer bodies, and math Plain-English rewrites follow motivated build-up — name what we want → name the naive thing → name why it fails → name the workaround. No Q&A markers, no metaphors, no marketing voice. Reference paragraph is the Motivation on [[ml_concepts/elbo]].
- **Notes:** Voice quality enforced by `wiki-lint` Check 7 going forward. Stubs will get Motivation and Up next when their ingest sources arrive.
