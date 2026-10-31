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
