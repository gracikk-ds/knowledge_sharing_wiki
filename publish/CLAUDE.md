This directory is the vendored **Quartz v4** (`jackyzha0/quartz`) static-site generator that publishes the vault as a website. `content` is a symlink → `../wiki`, so Quartz builds the notes there.

## Build & deploy

The site is deployed to **Vercel** at `ml-notes-wiki.vercel.app` (`vercel.json` sets `cleanUrls`, so `/foo` serves `foo.html`). Requires **Node ≥ 22** (`.node-version` pins v22.16.0).

Run from this directory:

```bash
npx quartz build --serve   # local preview at http://localhost:8080 (live reload)
npx quartz build           # one-off build → public/ (gitignored)
npm run check              # tsc + prettier check (only when editing Quartz internals)
```

Site config is `quartz.config.ts` (title, `baseUrl`, `locale: ru-RU`, plugin pipeline incl. KaTeX, Obsidian-flavored markdown, OG images); layout/components are `quartz.layout.ts`.

## Hard constraint — assets must live under the content root

Quartz only emits files found under `../wiki`. Anything placed outside it is never copied to the build and its embeds 404 on the published site. This is why attachments live in `wiki/images/` and embeds point there.
