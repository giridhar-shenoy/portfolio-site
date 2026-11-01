# portfolio-site

Source of Giridhar J Shenoy's site: plain HTML and one CSS file in `public/`, a few Python
scripts that generate the repo cards and media slots and check the pages, and two GitHub
Actions workflows. No framework, no build tool, no analytics, system fonts only.

## Preview

```bash
python3 -m http.server -d public 8000    # then open http://localhost:8000/
```

To see the pages as they will be published (TODO blocks taken out, see below):

```bash
python3 scripts/build_site.py && python3 -m http.server -d _site 8000
```

`404.html` uses URLs under `/portfolio-site/` (GitHub Pages serves it for missing paths at any
depth), so its stylesheet and links only resolve on the deployed site.

## Layout

| Path | What it is |
|---|---|
| `public/` | The site exactly as published: five pages, `robots.txt`, `sitemap.xml`, `site.webmanifest`, `assets/` |
| `data/repos.json` | The repos on the site: one line, stack, hero GIF source and commit (schema below) |
| `scripts/build_repos.py` | Writes the Home cards and the `repos.html` table from `data/repos.json`; `--refresh-heroes` copies the GIFs from the local clones |
| `content/bot-and-brew.md` | The author's text of the Bot & Brew page (intro, video caption, "What the kiosk did", "How it went", "What I take from it"); the page is that text converted to HTML by hand, word for word, except the caption, which `build_media.py` reads from the file |
| `scripts/build_media.py` | Fills the video and CV slots: a TODO block while a file is missing, the player or link once it exists; the Home "Watch 60 s" button follows the video |
| `scripts/build_site.py` | Writes `_site/`, the published copy: `public/` without the TODO blocks (see below) |
| `scripts/optimize_media.sh` | GIF → still (WebP) for the cards; `--video SRC`: the full-length video → the 60 s clip at 2× speed (≤ 8 MB), its poster (≤ 150 KB) and captions |
| `scripts/make_images.py` | Open Graph image and icons (Pillow, local only) |
| `scripts/check_*.py` | `check_links`, `check_todos`, `check_numbers`, `check_public` (see below) |
| `.github/workflows/` | `check.yml` on every push and PR; `deploy.yml` to Pages, switched off until launch |

Generated blocks sit between `<!-- build_repos:NAME:begin/end -->` and
`<!-- build_media:NAME:begin/end -->` markers; edit `data/repos.json` or add the file, then
re-run the script. CI fails if a generated block is stale.

## data/repos.json

```jsonc
{
  "owner": "giridhar-shenoy",
  "repos": [{
    "name": "ur5e-teaching-controllers",           // GitHub repo name, shown as the link text
    "url": "https://github.com/giridhar-shenoy/…",  // repo URL; the CI badge is derived from it
    "one_line": "…",                                // from the README's first screen; no numbers
    "stack": "…",                                   // languages and main tools, language split first
    "hero": {
      "local_clone": "~/work/r1",                   // where --refresh-heroes copies from
      "source_path": "docs/assets/hero.gif",        // path of the GIF in that repo
      "source_commit": "<40-hex>",                  // HEAD of the clone when it was copied
      "gif": "assets/img/<name>.gif",               // the copy, linked from the card
      "still": "assets/img/<name>.webp",            // the frame the card shows (optimize_media.sh)
      "still_width": 640, "still_height": 480,
      "alt": "…"
    }
  }]
}
```

The cards show a still and link to the GIF, so the Home page stays well under its weight budget
and nothing moves on the page.

## TODO convention

Anything not known yet is a visible block with `class="todo"` (rendered with a dashed yellow
border and the word TODO), never prose that looks like a fact. `scripts/check_todos.py` lists
every one. TODOs never reach the published site and never block a deploy: the deploy publishes
`_site/`, which `scripts/build_site.py` writes from `public/` without any element with class
`todo`, and without a heading or element that this leaves empty. So a section whose only
content is a TODO goes too, and while the video or the CV file is missing, the Home "Watch 60 s"
button or the CV line is left out. The deploy lists the TODOs in its job summary. The local
preview of `public/` keeps them.

## Checks

| Script | Local / CI | Deploy |
|---|---|---|
| `check_links.py` | internal links and `#anchors` must resolve; external URLs get HEAD (then GET); 404s from the private repos are listed as expected | same, then `--no-external` on `_site/` |
| `check_todos.py` | lists TODO blocks | lists them in the job summary; `--strict` on `_site/`, which must have none |
| `check_numbers.py` | every digit a reader sees is 30, February 2026, a name, or inside a TODO | same |
| `check_public.py` | `--allow-private`: prints each repo's visibility | same |
| `html5validator` | Nu Html Checker over `public/` | over `public/` and `_site/` |

`SITE_ROOT=_site` points any check at the published copy instead of `public/`; `check.yml`
also builds and checks `_site/`, so a push shows what the deploy would publish.

## Deploy

`deploy.yml` publishes `_site/` to GitHub Pages on a push to `main`, after the checks. The
checks run non-strict, as in `check.yml`, so neither a TODO nor a private repo stops a deploy.
It is switched off: the job runs only when the repository variable `DEPLOY_ENABLED` is `true`.
To launch:

1. Make the repos in `data/repos.json` and this repo public (`check_public.py` prints each
   one's visibility).
2. Settings → Pages → Source: GitHub Actions.
3. `gh variable set DEPLOY_ENABLED --body true -R giridhar-shenoy/portfolio-site`.
4. `gh workflow run deploy.yml -R giridhar-shenoy/portfolio-site` (or push to `main`).
5. Open every URL in `public/sitemap.xml`; each should return 200.

The site is then at https://giridhar-shenoy.github.io/portfolio-site/.

## License

Code (scripts, workflows, HTML templates, CSS): MIT, see `LICENSE`. Written content and media:
© 2026 Giridhar J Shenoy, all rights reserved, see `CONTENT_LICENSE.md`.
