# Changelog

All notable changes to this site are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Repository skeleton: MIT license for the code, content license, notes, changelog.
- Five pages: Home (tagline, About, repo cards, the Bot & Brew video link), the Orangewood
  controllers case study, the Bot & Brew post-mortem (TODO blocks for the text only the author
  can write), the repos table and a 404; robots.txt, sitemap.xml, site.webmanifest.
- One stylesheet: system fonts, ~70ch measure, dark mode, print styles.
- `data/repos.json` and `scripts/build_repos.py`: repo cards and table from one source, hero GIFs
  copied from the local clones with their commit recorded, WebP stills for the cards.
- `scripts/build_media.py`: the 60 s video and CV slots show a TODO while the file is missing.
- `scripts/make_images.py`: Open Graph image and icons, plain text on a flat colour.
- Checks: `check_links`, `check_todos`, `check_numbers`, `check_public`, `check_weight`.
- Workflows: `check.yml` on every push and PR; `deploy.yml` to GitHub Pages, gated on the
  `DEPLOY_ENABLED` repository variable (not set).
- `scripts/build_site.py`: writes `_site/`, the published copy, without the TODO blocks and
  whatever they leave empty.

### Changed

- The deploy publishes `_site/` instead of `public/`, runs the checks non-strict and lists the
  TODOs in the job summary, so a TODO no longer blocks it; `check.yml` builds and checks
  `_site/` too.
- The Home "Watch 60 s" button and the Bot & Brew clause that points at the player follow the
  video file, like the player itself.
- Bot & Brew page: the author's text from `content/bot-and-brew.md` (intro, video caption,
  "What the kiosk did", Entrepreneur First paragraph), the 60 s video at 2× speed with poster
  and captions, and the link to the full-length version; no TODO blocks left on the site.
- Home links the CV (PDF).
- Bot & Brew rewrite: the page is titled "Bot & Brew: a robotic coffee kiosk" (Home's link
  follows) and carries the author's new text, with "How it went" and "What I take from it"
  in place of the Entrepreneur First aside; the video's captions are off unless the viewer
  turns them on; `build_media.py` reads the video caption from `content/bot-and-brew.md`.
- `optimize_media.sh --video SRC` makes the 60 s clip, its poster and captions from the
  full-length video; `check_numbers.py` allows the facts stated in `content/bot-and-brew.md`
  on the Bot & Brew page.

### Removed

- The link to the full-length Bot & Brew video (Google Drive) and its "2 min" allowance in
  `check_numbers.py`.
- humanoid-upper-body-retargeting from the Home cards and the Repos table (it stays private),
  with its GIF and still.
