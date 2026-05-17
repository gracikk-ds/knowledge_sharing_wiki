# Quartz + Vercel Publishing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish the `wiki/` directory as a static site at `ml-notes-wiki.vercel.app` with working wikilinks, KaTeX math, Cyrillic search, and a graph view — without touching the existing wiki content, raw sources, CLAUDE.md, or the four `wiki-*` skills.

**Architecture:** Quartz v4 lives in a new `publish/` subdirectory. `publish/content` is a git-tracked symlink to `../wiki`, so Quartz reads the wiki directly with no copy step. Vercel is pointed at `publish/` as its Root Directory and auto-deploys on every push to `main`.

**Tech Stack:** Quartz v4 (static site generator, TypeScript-configured, KaTeX-enabled), Node.js 22+, npm, Vercel (hosting + GitHub integration).

**Spec:** `docs/superpowers/specs/2026-05-17-quartz-vercel-publishing-design.md`

---

## File Structure

Files created by this plan (all under `publish/` unless noted):

| Path | Source | Responsibility |
| --- | --- | --- |
| `publish/content` | git symlink → `../wiki` | Surface `wiki/` to Quartz without copy |
| `publish/quartz/` | scaffolded by `npx quartz create` | Vendored Quartz source (config schema, plugins, components, build pipeline). Treat as a dependency — do not edit in this plan. |
| `publish/quartz.config.ts` | scaffolded then edited in Task 4 | Site title, locale, base URL, plugin list (KaTeX, link resolution, ToC, etc.) |
| `publish/quartz.layout.ts` | scaffolded, left untouched | Page layout (header, sidebar, graph, search). Template defaults are fine for v1. |
| `publish/package.json` | scaffolded | Node project descriptor + scripts |
| `publish/package-lock.json` | scaffolded | Pinned dependency tree |
| `publish/tsconfig.json` | scaffolded | TypeScript config for Quartz |
| `publish/globals.d.ts` | scaffolded | Type declarations |
| `publish/index.d.ts` | scaffolded (may or may not exist depending on version) | Type declarations |
| `publish/.gitignore` | created in Task 5 | Excludes `node_modules/`, `public/`, `.quartz-cache/` |

Files NOT touched by this plan: anything under `wiki/`, `raw/`, `.claude/`, `.obsidian/`, plus `CLAUDE.md` and `README.md`.

---

## Task 1: Preflight checks

**Files:** none (read-only verification)

- [ ] **Step 1: Verify Node.js version is 22 or newer**

Run:
```bash
node --version
```

Expected: `v22.x.x` or higher. Quartz v4 requires Node 22+.

If lower, install Node 22 via `nvm`:
```bash
nvm install 22 && nvm use 22
node --version
```

- [ ] **Step 2: Verify the repo's git remote and current branch**

Run:
```bash
git remote -v && git branch --show-current && git status --short
```

Expected:
- Remote `origin` is `https://github.com/gracikk-ds/knowledge_sharing_wiki.git`
- Branch is `main`
- Working tree clean (no uncommitted changes besides this plan file itself, which is fine)

- [ ] **Step 3: Verify `publish/` does not already exist**

Run:
```bash
ls -la publish 2>&1 | head -3
```

Expected: `ls: cannot access 'publish': No such file or directory` (or equivalent macOS message).

If `publish/` exists from a previous attempt, stop and ask the user before overwriting.

---

## Task 2: Scaffold Quartz template into `publish/`

**Files:**
- Create: `publish/` directory tree (cloned from Quartz template)

- [ ] **Step 1: Clone Quartz upstream into `publish/`**

Run from repo root:
```bash
git clone --depth=1 https://github.com/jackyzha0/quartz.git publish
```

Expected: clone completes, `publish/` contains files including `package.json`, `quartz.config.ts`, `quartz/` (subdir).

- [ ] **Step 2: Remove the nested `.git` directory**

Run:
```bash
rm -rf publish/.git
```

Quartz was cloned with its own git history; we don't want a nested repo inside our own. After this, `publish/` is a plain directory tracked by our repo.

- [ ] **Step 3: Install Quartz's npm dependencies**

Run:
```bash
cd publish && npm install
```

Expected: completes without errors. Creates `publish/node_modules/` and updates `publish/package-lock.json`. Takes 30-90 seconds. Warnings about peer dependencies are normal; errors are not.

- [ ] **Step 4: Verify Quartz CLI is invokable**

Run from `publish/`:
```bash
npx quartz --help
```

Expected: prints Quartz's usage banner with commands `create`, `build`, `update`, `sync`, `restore`.

---

## Task 3: Initialize Quartz content and replace with symlink

**Files:**
- Create then delete: `publish/content/` (empty directory from `quartz create`)
- Create: `publish/content` (symlink → `../wiki`)

- [ ] **Step 1: Run `npx quartz create` non-interactively**

Run from `publish/`:
```bash
npx quartz create --strategy new --links shortest
```

This creates an empty `content/` directory and writes the default `index.md` placeholder, choosing "shortest" as the markdown link resolution strategy. If the flag names differ in the installed Quartz version, fall back to interactive: `npx quartz create` and answer "Empty content folder" + "Treat links as shortest path".

Expected: prints "Created content folder" or similar, `ls content` shows the placeholder `index.md`.

- [ ] **Step 2: Delete the placeholder `content/` directory**

Run from `publish/`:
```bash
rm -rf content
```

- [ ] **Step 3: Create the content symlink pointing at `../wiki`**

Run from `publish/`:
```bash
ln -s ../wiki content
```

- [ ] **Step 4: Verify the symlink resolves and points where expected**

Run from `publish/`:
```bash
ls -la content && readlink content && ls content/index.md
```

Expected:
- `ls -la content` shows `content -> ../wiki`
- `readlink content` prints `../wiki`
- `ls content/index.md` prints `content/index.md` (i.e. our `wiki/index.md` is now reachable via the symlink)

---

## Task 4: Configure `quartz.config.ts`

**Files:**
- Modify: `publish/quartz.config.ts`

Quartz's scaffolded `quartz.config.ts` ships with sensible defaults. This task overrides the handful of fields the spec calls out.

- [ ] **Step 1: Read the scaffolded `quartz.config.ts` to find the exact field names**

Run:
```bash
cat publish/quartz.config.ts
```

Note the exact spelling of the top-level keys inside `configuration: { ... }`: `pageTitle`, `pageTitleSuffix`, `enableSPA`, `enablePopovers`, `analytics`, `locale`, `baseUrl`, `ignorePatterns`, `defaultDateType`, `theme`. The set may differ slightly between Quartz versions. If a field below doesn't exist in the scaffold, leave it out; if there's a new required field, accept its default.

- [ ] **Step 2: Set `pageTitle` to `"ML Notes Wiki"`**

Edit `publish/quartz.config.ts`. Find the line that starts with `pageTitle:` inside the `configuration:` block and set it to `"ML Notes Wiki"`. The default is usually `"🪴 Quartz 4"`.

- [ ] **Step 3: Set `pageTitleSuffix` to empty string**

Find `pageTitleSuffix:` and set it to `""`. If the field doesn't exist in the scaffold, skip.

- [ ] **Step 4: Set `locale` to `"ru-RU"`**

Find `locale:` and set it to `"ru-RU"`. The default is `"en-US"`. This controls UI strings (sidebar labels, "Recent notes", "Last updated", search prompt). Page content is untouched.

- [ ] **Step 5: Set `baseUrl` to `"ml-notes-wiki.vercel.app"`**

Find `baseUrl:` and set it to `"ml-notes-wiki.vercel.app"` (no scheme, no trailing slash). The default is something like `"quartz.jzhao.xyz"`. This is used by the sitemap, RSS, and any plugin that emits absolute URLs.

- [ ] **Step 6: Set `defaultDateType` to `"modified"`**

Find `defaultDateType:` and set it to `"modified"`. The default is `"created"`. Combined with the `CreatedModifiedDate` transformer's `["frontmatter", "git", "filesystem"]` priority (which is also the Quartz default), this surfaces our frontmatter `updated:` field as the page's displayed date.

- [ ] **Step 7: Set `ignorePatterns` to `[]`**

Find `ignorePatterns:` and set it to `[]` (empty array). The default usually excludes things like `"private"`, `"templates"`, `".obsidian"` — those folders don't exist under `wiki/`, so removing them is a no-op but matches the spec's "no exclusions" decision and keeps the config honest.

- [ ] **Step 8: Enable the KaTeX LaTeX transformer**

Find the `plugins.transformers:` array. It should already contain entries like `Plugin.FrontMatter()`, `Plugin.ObsidianFlavoredMarkdown(...)`, `Plugin.GitHubFlavoredMarkdown()`, `Plugin.CrawlLinks(...)`, etc. Look for `Plugin.Latex(...)`:

- If present and configured as `Plugin.Latex({ renderEngine: "katex" })`, no change needed.
- If present but with a different `renderEngine` (e.g. `"mathjax"`), change it to `"katex"`.
- If absent, append `Plugin.Latex({ renderEngine: "katex" })` to the transformers array.

- [ ] **Step 9: Confirm `CrawlLinks` uses `markdownLinkResolution: "shortest"`**

Find the `Plugin.CrawlLinks(...)` entry in the transformers array. Verify it has `markdownLinkResolution: "shortest"`. If it has a different value (or no value), set it to `"shortest"`. The `npx quartz create --links shortest` from Task 3 should have already done this — this step is a belt-and-suspenders check.

- [ ] **Step 10: Read back the final config and visually scan for sanity**

Run:
```bash
cat publish/quartz.config.ts
```

Confirm all seven settings from steps 2-8 are in place and that the file is syntactically intact (matched braces, no stray commas). Don't try to compile it yet — Task 6 does that.

---

## Task 5: Add `publish/.gitignore`

**Files:**
- Create: `publish/.gitignore`

- [ ] **Step 1: Create `publish/.gitignore` with the build/install excludes**

Create the file with this exact content:

```gitignore
node_modules/
public/
.quartz-cache/
```

`node_modules/` — installed dependencies, regenerated by `npm ci` on Vercel.
`public/` — Quartz's build output, regenerated on every deploy.
`.quartz-cache/` — Quartz's incremental build cache.

- [ ] **Step 2: Verify git would track the symlink, config, and lock file but not node_modules**

Run from repo root:
```bash
git status --short publish/
```

Expected output includes (as untracked):
- `publish/.gitignore`
- `publish/content` (the symlink)
- `publish/package.json`
- `publish/package-lock.json`
- `publish/quartz.config.ts`
- `publish/quartz.layout.ts`
- `publish/quartz/` (and its contents)
- `publish/tsconfig.json`
- `publish/globals.d.ts`

Expected output does NOT include `publish/node_modules/` or `publish/public/`.

---

## Task 6: Local build + verification checklist

This task IS the test suite. The spec defines nine verification items; each is a sub-step here with concrete pass criteria.

**Files:** none modified directly. If any check fails, fix the offending file and re-run from Step 1.

- [ ] **Step 1: Run a clean build**

Run from `publish/`:
```bash
npx quartz build
```

Expected: exits 0. The output ends with something like "Done processing N files in Xs". Warnings about missing files (broken wikilinks to stub pages) are expected and OK — they should not be fatal. A non-zero exit means a real config or content error; fix before continuing.

- [ ] **Step 2: Start the dev server with live reload**

Run from `publish/`:
```bash
npx quartz build --serve
```

Expected: server starts on `http://localhost:8080` and prints "Started a Quartz server listening at ...". Leave this running in one terminal; do the next checks in a browser.

- [ ] **Step 3: Verify the home page renders from `wiki/index.md`**

Open `http://localhost:8080/` in a browser.

Expected: the page renders "Wiki Index" as the H1, followed by the "Start here" topic list (`topics/variational-inference`, `topics/few-step-generative-models`, etc.). If the home page shows Quartz's default placeholder instead, the symlink in Task 3 didn't work — re-check `ls -la publish/content`.

- [ ] **Step 4: Verify KaTeX renders inline and display math**

Open `http://localhost:8080/ml_concepts/self-attention/`.

Expected:
- Inline math like $q_m = W_Q\, x_m$ in the "Formal description" section renders as proper math (not raw `$q_m = ...$` text).
- The display equation $$\alpha_{m, n} = \mathrm{softmax}_n\!\left(\frac{q_m^\top k_n}{\sqrt{d_k}}\right)$$ renders centered with proper fraction layout.

If math is rendered as raw text with `$` signs visible, the `Plugin.Latex` entry from Task 4 Step 8 isn't being picked up — recheck the config and rebuild.

- [ ] **Step 5: Verify all three wikilink flavors resolve**

On the home page (`http://localhost:8080/`), hover or click these links from the topic list:

1. `[[topics/variational-inference]]` (subfolder-prefixed) → should navigate to `/topics/variational-inference/`
2. From inside the self-attention page, an aliased link like `[[ml_concepts/multi-head-attention|multi-head]]` should show as "multi-head" in the rendered text but link to `/ml_concepts/multi-head-attention/`
3. From inside any page, a bare wikilink like `[[self-attention]]` (if any) should resolve to `/ml_concepts/self-attention/` via shortest-path resolution

If any link is rendered as red/broken text or 404s when the target file exists, switch `markdownLinkResolution` from `"shortest"` to `"absolute"` in `quartz.config.ts` (Task 4 Step 9), rebuild, and re-check.

- [ ] **Step 6: Verify stub-link rendering**

The wiki has links to pages that don't exist yet (the "stub link" pattern from CLAUDE.md). On the home page, the entry for `[[ml_concepts/diffusion-model]]` exists as a 2-line stub — find a page that links to a *missing* target.

Open `http://localhost:8080/ml_concepts/self-attention/` and look for any wikilink that points to a file not under `wiki/`. The link should render greyed out, with no crash, no console error, and the build (from Step 1) must not have failed because of it.

If you can't find a clearly-broken link, this check passes by default — the goal is to confirm Quartz doesn't choke on missing targets.

- [ ] **Step 7: Verify Cyrillic search works**

Use the site search (icon in the top-right of any page, or keyboard shortcut shown in the search UI). Type a Russian word that appears in the wiki, e.g. `softmax` (English, baseline check) then `активаций` (Cyrillic).

Expected:
- `softmax` returns hits including `wiki/ml_concepts/self-attention.md` and several others.
- `активаций` returns at least one hit (the wiki uses this word in motivation sections).

If Cyrillic queries return no results despite the word being in the content, search-index encoding is broken — file as a bug; for v1 we accept English-only search and move on.

- [ ] **Step 8: Verify graph view renders**

Click the graph icon (usually bottom-right of a page) on `http://localhost:8080/ml_concepts/self-attention/`.

Expected: a local graph of nodes around the self-attention page, with edges to `multi-head-attention`, `positional-encoding`, `transformer`, etc. The global graph (button next to local) should show clusters.

- [ ] **Step 9: Verify `log.md` with pipe characters in headings renders**

Open `http://localhost:8080/log/`.

Expected: page renders without truncation or crash. Headings like `## [2026-05-15] ingest | Karpathy — makemore part 3` show up; the `|` character should not break the markdown render. URL fragments may be ugly (`/log/#2026-05-15-ingest--karpathy--makemore-part-3` or similar) but should be valid.

- [ ] **Step 10: Verify dark/light theme toggle**

Click the theme toggle (sun/moon icon, usually top-right). The page should switch palettes without re-loading.

- [ ] **Step 11: Stop the dev server**

In the terminal running `npx quartz build --serve`, press `Ctrl+C`.

---

## Task 7: Commit and push `publish/` setup

**Files:**
- Stage: everything under `publish/` that isn't gitignored

- [ ] **Step 1: Review what will be committed**

Run from repo root:
```bash
git status --short && git diff --stat publish/.gitignore 2>/dev/null
```

Expected: a list of new files under `publish/` (config, package files, scaffolded Quartz source, the symlink), no `node_modules/` or `public/` entries.

- [ ] **Step 2: Stage the publish directory**

Run from repo root:
```bash
git add publish/
```

- [ ] **Step 3: Verify the content symlink was staged as a symlink**

Run:
```bash
git ls-files --stage publish/content
```

Expected: mode `120000` (the git mode for symlinks). If it's mode `100644`, git stored the symlink as a regular file containing the path `../wiki` — that won't work on Vercel. Re-create with `core.symlinks=true` in the local git config and re-stage.

- [ ] **Step 4: Commit**

Run:
```bash
git commit -m "$(cat <<'EOF'
Add Quartz site scaffolding in publish/

Vendors Quartz v4 with content/ symlinked to ../wiki. Config sets
pageTitle "ML Notes Wiki", locale ru-RU, baseUrl
ml-notes-wiki.vercel.app, KaTeX math, shortest wikilink resolution.
Vercel will deploy from publish/ on push to main.
EOF
)"
```

- [ ] **Step 5: Push to GitHub**

Run:
```bash
git push origin main
```

Expected: push succeeds. The Vercel project (set up in the next task) will detect this commit and start the first deploy.

---

## Task 8: Connect Vercel project

**Files:** none (Vercel dashboard work)

This task is run by the user in a browser. The agent cannot do this autonomously because it requires a logged-in Vercel session.

- [ ] **Step 1: Open Vercel's import flow**

In a browser, open `https://vercel.com/new` while logged in. If the GitHub integration isn't already set up, follow Vercel's prompts to install the Vercel GitHub App on the `gracikk-ds` account (or whichever account owns the `knowledge_sharing_wiki` repo) and grant it access to the `knowledge_sharing_wiki` repo.

- [ ] **Step 2: Import the repo**

Find `knowledge_sharing_wiki` in the import list and click "Import".

- [ ] **Step 3: Configure project settings on the import screen**

Set exactly these values:

| Field | Value |
| --- | --- |
| Project Name | `ml-notes-wiki` |
| Framework Preset | `Other` |
| Root Directory | `publish` |
| Build Command | `npx quartz build` |
| Output Directory | `public` |
| Install Command | `npm ci` |
| Node.js Version | `22.x` |
| Environment Variables | (none) |

The Root Directory is the most important field. If it's left blank, Vercel will try to build from the repo root and fail.

- [ ] **Step 4: Click "Deploy"**

Vercel will clone the repo, `cd` into `publish/`, run `npm ci`, then `npx quartz build`. Watch the build log.

Expected: build completes in 1-3 minutes. If it fails, the most common causes are:
- Node version mismatch → set Node 22.x in Settings → General → Node.js Version, then redeploy
- Symlink wasn't stored as a symlink (Task 7 Step 3) → re-do that step and push again
- `baseUrl` typo causing absolute-link generation to fail → fix in `quartz.config.ts` and push again

- [ ] **Step 5: Note the assigned URL**

After the deploy succeeds, Vercel shows the live URL. It should be `https://ml-notes-wiki.vercel.app`. If Vercel assigned a different subdomain (e.g. someone else already owns `ml-notes-wiki`), note the actual URL and update `baseUrl` in `quartz.config.ts` to match, then commit and push (which triggers a redeploy).

---

## Task 9: Verify the live deploy

**Files:** none (browser verification)

Re-run the checklist from Task 6 against the live URL. Most checks should behave identically; differences usually mean a `baseUrl` mismatch or asset-loading issue.

- [ ] **Step 1: Open the live home page**

Open `https://ml-notes-wiki.vercel.app/` (or whatever URL Task 8 Step 5 assigned).

Expected: same page as the local home in Task 6 Step 3.

- [ ] **Step 2: Verify the four critical interactions on the live site**

Repeat these from Task 6 against the live URL:
- KaTeX math on `/ml_concepts/self-attention/` (Task 6 Step 4)
- Wikilink navigation (Task 6 Step 5)
- Cyrillic search (Task 6 Step 7)
- Theme toggle (Task 6 Step 10)

All should behave the same as local.

- [ ] **Step 3: Verify the sitemap and RSS use the correct absolute URLs**

Open `https://ml-notes-wiki.vercel.app/sitemap.xml` and `https://ml-notes-wiki.vercel.app/index.xml`.

Expected: URLs in both files start with `https://ml-notes-wiki.vercel.app/...`. If they start with `https://quartz.jzhao.xyz/...` or any other host, `baseUrl` was not picked up — fix in `quartz.config.ts`, commit, push, wait for redeploy, re-check.

- [ ] **Step 4: Confirm auto-deploy works**

Make a trivial change to the wiki — pick any page and edit one word, or add a stub page. Commit + push to main. Within ~2 minutes, Vercel should show a new deployment in its dashboard and the live site should reflect the change.

If auto-deploy doesn't trigger, check Vercel project → Settings → Git → Production Branch is set to `main` and Auto-deploy is enabled.

- [ ] **Step 5: Done**

The site is live. Out-of-scope follow-ups (custom domain, theme tweaks, hiding `log.md`, a custom reading-order component, a GH Actions sanity gate) are tracked in the spec's "Out-of-scope follow-ups" section and can be picked up as separate plans.

---

## Notes for the executor

- The plan assumes a Unix-like environment (macOS or Linux). On Windows, the symlink step (Task 3 Step 3) requires Developer Mode or running as Administrator. The user is on macOS, so this isn't a concern.
- Tasks 1-7 are fully scriptable. Task 8 requires a logged-in human in the Vercel dashboard. Task 9 is browser-driven verification.
- If `npx quartz create` in Task 3 prompts interactively despite the flags, accept "Empty content folder" + "Treat links as shortest path". The end state matches what the flags would have produced.
- The spec's "Risks and mitigations" table covers the recovery paths for the most likely failure modes. Reference it when something goes wrong during Task 6 or Task 8.
