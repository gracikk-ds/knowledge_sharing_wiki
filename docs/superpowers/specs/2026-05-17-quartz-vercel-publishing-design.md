# Quartz + Vercel publishing for the ML Notes wiki

**Date:** 2026-05-17
**Status:** draft
**Repo:** `gracikk-ds/knowledge_sharing_wiki`

## Goal

Publish the `wiki/` content as a static site so the user can browse, share, and link to it from any device. The published site must preserve everything that makes the wiki useful in Obsidian: working `[[wikilinks]]` (including subfolder paths and `|alias` syntax), KaTeX-rendered math, Cyrillic search, a graph view, and the existing folder structure surfaced as navigation.

Authoring stays unchanged. The user keeps writing to `raw/`, Claude keeps writing to `wiki/`, the existing four skills (`wiki-ingest`, `wiki-query`, `wiki-lint`, `wiki-quiz`) keep working as-is. CLAUDE.md, the Obsidian vault, and all internal paths stay untouched.

## Non-goals

- Authoring workflow changes — not in scope.
- Renaming `wiki/` to `content/` — not in scope (approach B was rejected).
- A second repo for site-only files — not in scope (approach C was rejected).
- Custom theme, custom components, or visual redesign — deferred. First deploy uses Quartz defaults with locale and math enabled.
- Custom domain — deferred. First deploy lives on `ml-notes-wiki.vercel.app`.
- Analytics, comments, or any third-party tracking — deferred.
- Excluding pages from publication — not in scope (publish everything under `wiki/`).

## Decisions (locked)

| Topic                       | Decision                                                                                           |
| --------------------------- | -------------------------------------------------------------------------------------------------- |
| Repo layout                 | Approach A: Quartz lives in `publish/` subdirectory; `publish/content` is a git-tracked symlink to `../wiki`. |
| Site title                  | "ML Notes Wiki"                                                                                    |
| Vercel project slug         | `ml-notes-wiki` → first deploy at `ml-notes-wiki.vercel.app`                                       |
| Content scope               | Publish everything under `wiki/`. `ignorePatterns` empty initially; revisit if individual pages need hiding later. |
| Math renderer               | KaTeX (via Quartz's `Plugin.Latex({ renderEngine: "katex" })`)                                     |
| Link resolution             | Quartz `markdownLinkResolution: "shortest"`. Switch to `"absolute"` only if the build shows ambiguous matches. |
| UI locale                   | `ru-RU` (sidebar labels, dates, search prompt — content is mixed Russian/English already)         |
| Date displayed              | `defaultDateType: "modified"` → uses frontmatter `updated`                                         |
| Deploy trigger              | Auto-deploy on push to `main` via Vercel's GitHub integration. PR branches get preview URLs.       |
| Custom domain               | Deferred                                                                                           |

## Final repo layout

```
ml_notes/
├── wiki/                      # unchanged — source of truth, published as-is
├── raw/                       # unchanged, NOT published
├── CLAUDE.md, .claude/        # unchanged, NOT published
├── README.md                  # NOT published
├── docs/                      # NEW — design specs, plans, project meta (NOT published)
│   └── superpowers/
│       └── specs/
│           └── 2026-05-17-quartz-vercel-publishing-design.md  # this file
└── publish/                   # NEW — the Quartz site
    ├── content                # symlink → ../wiki  (git-tracked symlink)
    ├── quartz/                # Quartz source files (vendored from upstream template)
    ├── quartz.config.ts
    ├── quartz.layout.ts
    ├── package.json
    ├── package-lock.json
    ├── tsconfig.json
    ├── globals.d.ts
    └── .gitignore             # node_modules/, public/, .quartz-cache/
```

Why a symlink rather than copying files at build time: a symlink keeps a single source of truth, lets local `npx quartz build --serve` reflect edits to `wiki/` instantly, and is honored by Vercel's build runner (Linux + git stores the symlink). The trade-off is that anyone running this on Windows would need to enable symlinks; that's not in scope for this user.

## Quartz configuration

`publish/quartz.config.ts` (key fields, not exhaustive — everything else stays at template defaults):

```ts
import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
  configuration: {
    pageTitle: "ML Notes Wiki",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "ru-RU",
    baseUrl: "ml-notes-wiki.vercel.app",  // updated when a custom domain is added
    ignorePatterns: [],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: { /* template defaults */ },
      colors: { /* template defaults — light + dark via toggle */ },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({ priority: ["frontmatter", "git", "filesystem"] }),
      Plugin.SyntaxHighlighting({ theme: { light: "github-light", dark: "github-dark" }, keepBackground: false }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({ enableSiteMap: true, enableRSS: true }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
```

`publish/quartz.layout.ts` stays at template defaults for v1: graph view + search + dark/light toggle + breadcrumbs + explorer in the sidebar. Custom layout tweaks belong in a follow-up PR after the first deploy is verified.

## Vercel project settings

Settings to enter in the Vercel dashboard when importing the repo:

| Setting               | Value                                                       |
| --------------------- | ----------------------------------------------------------- |
| Framework Preset      | Other                                                       |
| Root Directory        | `publish/`                                                  |
| Build Command         | `npx quartz build`                                          |
| Output Directory      | `public`                                                    |
| Install Command       | `npm ci`                                                    |
| Node.js Version       | 22.x (matches Quartz's current requirement)                 |
| Production Branch     | `main`                                                      |
| Auto-deploy           | On every push to `main`. PR branches get preview URLs.      |
| Environment Variables | none                                                        |

The site's eventual public URL is `https://ml-notes-wiki.vercel.app`. The Quartz `baseUrl` in config must match this exactly (no scheme, no trailing slash) for the sitemap and RSS feed to generate correct absolute links.

## Authoring & local preview

Nothing in the authoring loop changes. New workflow additions:

- **Local preview:** `cd publish && npx quartz build --serve` → live-reload at `http://localhost:8080`.
- **Verify before push:** running the build locally before pushing catches broken wikilinks, math syntax errors, and frontmatter problems that would otherwise fail the Vercel deploy.

No new skill is needed; the four existing `wiki-*` skills already cover authoring and maintenance.

## Verification checklist (run during step 4 of the build order, before pushing)

The first local build must pass all of these:

1. `npx quartz build` exits 0 with no errors.
2. Inline math `$\alpha_{m,n}$` and display math `$$ ... $$` render via KaTeX on a sample page (`wiki/ml_concepts/self-attention.md` is a good test — it has both).
3. A bare wikilink (`[[self-attention]]`), a subfolder wikilink (`[[ml_concepts/self-attention]]`), and an aliased wikilink (`[[ml_concepts/multi-head-attention|multi-head]]`) all resolve to the right destination.
4. A wikilink to a stub page that doesn't exist (e.g. `[[ml_concepts/diffusion-model]]` — currently a 2-line stub) renders without crashing the build. Broken links to non-existent files render greyed out.
5. The home page is `wiki/index.md` and renders the topic list at the top.
6. Cyrillic text in `wiki/sources/elbo-and-vae-lecture.md` is searchable via the in-site search.
7. The graph view shows the cluster structure (topics, concepts, methods linked together).
8. `wiki/log.md`'s `## [YYYY-MM-DD] ingest | ...` headings produce valid anchor URLs without breaking the page render.
9. Dark/light theme toggle works.

Items 3, 4, and 8 are the highest-risk: Quartz wikilink resolution and the `|` character in markdown headings are the two things most likely to misbehave on real content.

## Build order (the implementation plan will expand this)

1. Scaffold `publish/` with `npx quartz create`, accept defaults.
2. Replace `publish/content/` with a symlink to `../wiki`. Commit the symlink.
3. Edit `publish/quartz.config.ts`: set `pageTitle`, `locale`, `baseUrl`, `defaultDateType`, and enable the KaTeX plugin per spec above.
4. Run `npx quartz build --serve` locally. Walk through the verification checklist above. Fix anything that fails.
5. Add `publish/.gitignore` for `node_modules/`, `public/`, `.quartz-cache/`. Commit configuration + lock file.
6. Push to `main`.
7. In Vercel: import the repo, set Root Directory to `publish/`, accept the build/output settings above, set the project name to `ml-notes-wiki`. Wait for first deploy.
8. Open `https://ml-notes-wiki.vercel.app` and re-run the verification checklist on the live site. Fix anything that fails differently from local (most likely: `baseUrl`-derived absolute links in the sitemap/RSS).
9. Done. Custom domain and theme tweaks are separate follow-ups.

## Risks and mitigations

| Risk                                                                                       | Mitigation                                                                                     |
| ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Quartz's `shortest` link mode picks the wrong page when two pages share a basename         | Switch to `"absolute"` and use full paths in wikilinks. The wiki currently has no basename collisions across folders, so this is unlikely. |
| KaTeX rejects a macro the wiki uses (`\text{...}`, `\mathrm`, custom commands)             | Quartz's KaTeX integration supports the standard KaTeX macro set, which covers everything currently used in the wiki. Failures will surface in step 4 and can be fixed per-page. |
| `log.md` heading like `## [2026-05-15] ingest \| Karpathy — makemore part 3` produces a broken slug | The `|` is valid in markdown headings and gets slugified by Quartz's slugifier. Verification step 8 catches any regression. |
| The git-tracked symlink confuses Vercel's clone step                                       | Vercel uses standard `git clone` on a Linux runner — symlinks survive. If this ever fails, fall back to a build-time `cp -r ../wiki content/` step in the Quartz config or a `prebuild` npm script. |
| Quartz upstream releases break the config schema                                           | The Quartz source is vendored into `publish/quartz/`, pinned to whatever version `npx quartz create` produces. Upgrades become an intentional, separate change. |
| First Vercel build fails on a typo in `baseUrl` or the build command                       | Verification step 8 catches this on the live URL. Fix and push; redeploy is automatic.         |

## Out-of-scope follow-ups (track separately)

- Custom domain (`notes.<user>.<tld>` or similar).
- Theme: typography tweak for Cyrillic rendering, palette aligned with personal aesthetics.
- Hide `wiki/log.md` from the published site if it ever becomes noisy.
- A small custom Quartz component for the topic-primer reading-order list.
- Add a GitHub Actions job that runs `npx quartz build` on PRs as a pre-Vercel sanity gate.
