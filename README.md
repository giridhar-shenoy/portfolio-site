# portfolio-site

Source of Giridhar J Shenoy's site: plain HTML and one CSS file in `public/`, a few Python
scripts that generate the repo cards and media slots and check the pages, and two GitHub
Actions workflows. No framework, no build tool, no analytics, system fonts only.

## Preview

```bash
python3 -m http.server -d public 8000    # then open http://localhost:8000/
```

`404.html` uses URLs under `/portfolio-site/` (GitHub Pages serves it for missing paths at any
depth), so its stylesheet and links only resolve on the deployed site.

## Layout

| Path | What it is |
|---|---|
| `public/` | The site exactly as published: five pages, `robots.txt`, `sitemap.xml`, `site.webmanifest`, `assets/` |
| `data/repos.json` | The four repos: one line, stack, hero GIF source and commit (schema below) |
| `scripts/build_repos.py` | Writes the Home cards and the `repos.html` table from `data/repos.json`; `--refresh-heroes` copies the GIFs from the local clones |
| `scripts/build_media.py` | Fills the video and CV slots: a TODO block while a file is missing, the player or link once it exists |
| `scripts/optimize_media.sh` | GIF → still (WebP) for the cards; raw video → H.264 MP4 and poster |
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
every one; `--strict` fails while any remain, and the deploy workflow runs it strict, so the
site cannot be published with a TODO on it.

## Checks

| Script | Local / CI | Deploy |
|---|---|---|
| `check_links.py` | internal links and `#anchors` must resolve; external URLs get HEAD (then GET); 404s from the private repos are listed as expected | `--strict`: those 404s fail too |
| `check_todos.py` | lists TODO blocks | `--strict`: any TODO fails |
| `check_numbers.py` | every digit a reader sees is 30, February 2026, a name, or inside a TODO | same |
| `check_public.py` | `--allow-private`: prints each repo's visibility | strict: every repo must be public |
| `html5validator` | Nu Html Checker over `public/` | same |

## Deploy

`deploy.yml` publishes `public/` to GitHub Pages on a push to `main`, after the strict checks.
It is switched off: the job runs only when the repository variable `DEPLOY_ENABLED` is `true`.
To launch:

1. Make the four project repos and this repo public.
2. Resolve every TODO (`python3 scripts/check_todos.py --strict` passes).
3. Settings → Pages → Source: GitHub Actions.
4. `gh variable set DEPLOY_ENABLED --body true`, then push to `main` (or run the workflow).

The site is then at https://giridhar-shenoy.github.io/portfolio-site/.

## License

Code (scripts, workflows, HTML templates, CSS): MIT, see `LICENSE`. Written content and media:
© 2026 Giridhar J Shenoy, all rights reserved, see `CONTENT_LICENSE.md`.
