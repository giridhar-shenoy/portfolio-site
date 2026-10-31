# NOTES — portfolio-site

## Session of 31 Oct 2026 (unattended, overnight run)

Environment: Ubuntu 26.04, system `python3 --version` → Python 3.14.4. html5validator 0.4.2 in
`.venv` (pip, `--system-site-packages` not needed: nothing here imports rclpy). Java at
/usr/bin/java (needed by html5validator). Chrome at /usr/bin/google-chrome. No Docker.

### Plan

1. Skeleton: git init on main, .gitignore, LICENSE (MIT), CONTENT_LICENSE.md, README.md,
   NOTES.md, CHANGELOG.md, THIRD_PARTY.md. Commit; create the private GitHub repo; push.
2. Information architecture: one sentence per page in this file.
3. One stylesheet: system fonts, 16 px gutters, ~70ch measure, dark mode, print styles.
4. Pages: index, work/orangewood-controls, work/bot-and-brew, repos, 404; robots.txt,
   sitemap.xml, site.webmanifest; Open Graph image and icons generated with Pillow.
5. Scripts: build_repos.py, build_media.py, check_public.py, check_todos.py, check_links.py,
   check_numbers.py, optimize_media.sh.
6. Workflows: check.yml (runs on push and PR), deploy.yml (written, gated off, not triggered).
7. Lighthouse, headless, in a quiet window (not while an R1/R2 benchmark is running).
8. README: preview, repos.json schema, TODO convention, deploy flow.
9. Acceptance checks with their output pasted below; TODO list by page; CHANGELOG entry.

### Information architecture (one sentence per page)

- `index.html` (Home): says who I am in one tagline and one About paragraph, then routes to the
  four repos (one card each), the Bot & Brew video, the Repos page and the two case studies.
- `work/orangewood-controls.html`: states what I shipped at Orangewood in one paragraph, links
  Orangewood's own public page, and routes to ur5e-teaching-controllers as the public rebuild.
- `work/bot-and-brew.html`: shows the 60 s video first, states the few established facts, and
  holds TODO blocks where the post-mortem text will go; routes back to Home.
- `repos.html`: one table (repo, one line, stack, CI badge) that routes to each repository.
- `404.html`: says the page does not exist and routes to Home.

## Decisions taken unattended (31 Oct)

- **Docker is not installed** (and apt is off-limits), so R1/R2 regeneration ran natively in the
  /tmp/verify clones, following each README's native Ubuntu 26.04 + Lyrical instructions.
- **Site root is `public/`**, not the repo root, so the deploy publishes only the pages and
  assets — never NOTES.md, scripts or data. All spec paths (`assets/…`, `work/…`) are relative
  to `public/`.
- **Base URL** `https://giridhar-shenoy.github.io/portfolio-site/` (Pages project site, no
  custom domain). Canonical, Open Graph and sitemap URLs use it. robots.txt is served at
  `/portfolio-site/robots.txt`, where crawlers do not look (they read only the host root);
  allow-all is the default anyway, and the sitemap can be submitted by hand.
- **Home cards show a still, not the animated GIF**: the four GIFs total about 5.9 MB, against a
  500 KB page budget and "no animation" on Home. Each card links to its GIF ("Animated GIF").
  Stills are the middle frame of each GIF, 640 px wide WebP, 5–11 KB.
- **Two extra scripts** beyond the five listed: `build_media.py` (the video and CV slots must
  show a TODO while the file is missing, which static HTML cannot do by itself) and
  `make_images.py` (Open Graph image and icons), plus `check_numbers.py` to verify the
  numbers acceptance item by command. `sitelib.py` holds their shared helpers. All Python
  standard library, except Pillow in the local-only image script and `--refresh-heroes`.
- **deploy.yml is gated** on the repository variable `DEPLOY_ENABLED == 'true'`. "On push to
  main" would otherwise run it on every push tonight; with the gate a push shows a skipped job
  and nothing is built or published. The variable is not set.
- **One `theme-color`** instead of a light/dark pair: the Nu checker bundled with html5validator
  0.4.2 rejects `media` on `<meta>`.
- **"Numbers"**: names that contain digits (ROS 2, MoveIt 2, UR5e, Unitree G1, ros2_control,
  pybind11, ur5e-teaching-controllers), the verbatim "6-axis", the spec-mandated "© 2026" footer
  and the "Watch 60 s" label are not treated as numbers; `check_numbers.py` lists every one so
  they can be reviewed. The stack column says "C++" rather than "C++17" to keep digits out.
- **sitemap.xml lists the four content pages, not 404.html** (a sitemap entry for an error
  page is a soft-404 signal to search engines).
- **The Entrepreneur First line** sits at the end of the Bot & Brew page as "Separately, I was in
  the Entrepreneur First Bangalore cohort.", so it does not imply EF was part of Bot & Brew.
- **Orangewood public link**: https://www.ycombinator.com/companies/orangewood-labs returned 200
  in this session (`curl -L` → 200, title "Orangewood Labs: … | Y Combinator");
  /launches/orangewood-labs returned 404 and was not used.
- **The CV slot stays a TODO**: ~/work/resume/Giridhar_J_Shenoy_CV.pdf exists but still has
  TODOs in it, and the spec says the CV does not exist yet; it was not copied.
(removed)
  Orangewood and "30 production 6-axis arms" because the site spec says so; the repos' own NDA
  rule (no employer name or unit count) is not applied to the site.
