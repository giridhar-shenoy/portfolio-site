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
- **Employer name and unit count**: the site names Orangewood and "30 production 6-axis arms"
  because the site spec says so; the repos' own rule (no employer name or unit count) is not
  applied to the site.
- **GitHub Actions do not start on private repos on this account**: the first check.yml run was
  refused with "The job was not started because recent account payments have failed or your
  spending limit needs to be increased" (run 41156445456). Every check was run locally instead
  (output below). deploy.yml showed as skipped, as designed.

## Acceptance checks (run 31 Oct, output pasted as produced)

| Item | Result |
|---|---|
| Every page validates as HTML5 | yes: Nu checker "All good", 5 files |
| check_links.py passes | yes: 73 internal links/anchors, 0 broken; 12 private-repo URLs 404 as expected; LinkedIn 999 (warning) |
| Every number is 30, February 2026, or inside a TODO | yes: 0 disallowed; names with digits listed for review |
| repos.html lists exactly the four repos; repos.json has a commit per repo | yes |
| Bot & Brew page renders with the video absent and shows the TODO | yes (TODO block in place of the player; screenshot under Lighthouse below) |
| robots.txt allows crawling; no noindex; sitemap lists every page | yes, except 404.html is left out of the sitemap on purpose (see decisions) |
| Page weight without video < 500 KB | yes: largest is index.html at 46.1 KB |
| Conventional commits, none backdated; repo private; nothing deployed | yes: author date = commit date on every commit; PRIVATE; Pages API 404 (not enabled); deploy runs "skipped" |
| CI on GitHub | not run: Actions refused to start the job on this private repo (billing/spending-limit message); all checks run locally |

```text
$ .venv/bin/html5validator --root public --log INFO
INFO:html5validator.cli:Number of files: 5
INFO:html5validator.validator:All good.
exit 0

$ python3 scripts/check_links.py   (summary lines)
internal: 73 links and anchors checked, 0 broken
not checked: mailto:giridharjshenoy@gmail.com
external: 15 URLs: 2 ok, 12 expected 404 until Sunday (private repos), 1 warnings, 0 failed
  warning (host blocks automated requests): 999  https://www.linkedin.com/in/giridhar-j-shenoy/  (404.html:39, index.html:103, repos.html:86, work/bot-and-brew.html:85, work/orangewood-controls.html:55)

$ python3 scripts/check_numbers.py
Allowed digits outside TODO blocks (page · text · why · count):
  404.html · © 2026 · footer copyright line · 1
  index.html · 30 · number: the production arms · 1
  index.html · 60 s · label of the 60-second video · 1
  index.html · MoveIt 2 · name · 1
  index.html · ROS 2 · name · 5
  index.html · UR5e · name · 3
  index.html · Unitree G1 · name · 2
  index.html · ros2_control · name · 1
  index.html · ur5e-teaching-controllers · repo name · 1
  index.html · © 2026 · footer copyright line · 1
  repos.html · MoveIt 2 · name · 2
  repos.html · ROS 2 · name · 3
  repos.html · UR5e · name · 2
  repos.html · Unitree G1 · name · 1
  repos.html · pybind11 · name · 1
  repos.html · ros2_control · name · 2
  repos.html · ur5e-teaching-controllers · repo name · 2
  repos.html · © 2026 · footer copyright line · 1
  work/bot-and-brew.html · February 2026 · number: Bot & Brew wound down · 1
  work/bot-and-brew.html · ROS 2 · name · 1
  work/bot-and-brew.html · © 2026 · footer copyright line · 1
  work/orangewood-controls.html · 30 · number: the production arms · 1
  work/orangewood-controls.html · 6-axis · verbatim Orangewood paragraph · 3
  work/orangewood-controls.html · ROS 2 · name · 1
  work/orangewood-controls.html · UR5e · name · 3
  work/orangewood-controls.html · ur5e-teaching-controllers · repo name · 1
  work/orangewood-controls.html · © 2026 · footer copyright line · 1
Digits inside TODO blocks (page · token · count):
  work/bot-and-brew.html · 60-second · 1
  work/bot-and-brew.html · public/assets/video/bot-and-brew-60s-poster.jpg · 1
  work/bot-and-brew.html · public/assets/video/bot-and-brew-60s.en.vtt · 1
  work/bot-and-brew.html · public/assets/video/bot-and-brew-60s.mp4 · 1
Disallowed numbers: 0

$ python3 -c "...count rows in repos.html and commits in data/repos.json"
repos.html rows: ['ur5e-teaching-controllers', 'pointcloud-constrained-planning', 'humanoid-upper-body-retargeting', 'sim-demo-to-policy']
  ur5e-teaching-controllers: docs/assets/hero.gif @ 28074acc45aff82b68c393409ace02b865d0d6f3
  pointcloud-constrained-planning: docs/assets/constrained_vs_unconstrained.gif @ e79d0666362a3e88bbd8b8709a14cb9814e50444
  humanoid-upper-body-retargeting: docs/assets/retarget_synthetic.gif @ c32d36ad11020ad8c78b810c642dacc5eaa5dc8a
  sim-demo-to-policy: docs/assets/rollouts.gif @ 275adf56767cafda3c2e556225a70c62d10d555e

$ python3 scripts/check_todos.py | grep bot-and-brew | head -2
work/bot-and-brew.html:48: TODO The 60-second video goes here. Missing files: public/assets/video/bot-and-brew-60s.mp4 public/assets/video/bot-and-brew-60s-poster.jpg public/assets/video/bot-and-brew-60s.en.vtt Add them (raw footage can go in public/assets/video/src/ for scripts/optimize_media.sh), then run scripts/build_media.py.

$ cat public/robots.txt; grep -ril noindex public || echo "no noindex"
User-agent: *
Allow: /

Sitemap: https://giridhar-shenoy.github.io/portfolio-site/sitemap.xml
no noindex anywhere under public/

$ sitemap <loc> vs pages
https://giridhar-shenoy.github.io/portfolio-site/
https://giridhar-shenoy.github.io/portfolio-site/repos.html
https://giridhar-shenoy.github.io/portfolio-site/work/orangewood-controls.html
https://giridhar-shenoy.github.io/portfolio-site/work/bot-and-brew.html
./404.html
./index.html
./repos.html
./work/bot-and-brew.html
./work/orangewood-controls.html

$ python3 scripts/check_weight.py
404.html: 7.6 KB (ok) = html 1 KB + favicon.png 0 KB, site.css 5 KB
index.html: 46.1 KB (ok) = html 6 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 5 KB, ur5e-teaching-controllers.webp 7 KB, pointcloud-constrained-planning.webp 10 KB, humanoid-upper-body-retargeting.webp 8 KB, sim-demo-to-policy.webp 5 KB
repos.html: 12.5 KB (ok) = html 6 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 5 KB
work/bot-and-brew.html: 10.6 KB (ok) = html 4 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 5 KB
work/orangewood-controls.html: 9.7 KB (ok) = html 3 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 5 KB

$ git log --format="%h  author %ad  commit %cd  %s" --date=format:"%F %T %z"
bb9a987  author 2026-10-31 07:14:15 +0530  commit 2026-10-31 07:14:15 +0530  docs: record unattended decisions and the changelog entry
57cc255  author 2026-10-31 07:14:15 +0530  commit 2026-10-31 07:14:15 +0530  test: check page weight against the 500 KB budget
e865c64  author 2026-10-31 07:09:57 +0530  commit 2026-10-31 07:09:57 +0530  docs: explain preview, repos.json, the TODO convention and deploy
ee3723b  author 2026-10-31 07:09:57 +0530  commit 2026-10-31 07:09:57 +0530  ci: run the checks on push; add a Pages deploy that is switched off
96a6a9f  author 2026-10-31 07:09:57 +0530  commit 2026-10-31 07:09:57 +0530  test: add link, TODO, number and visibility checks
674fb25  author 2026-10-31 07:09:57 +0530  commit 2026-10-31 07:09:57 +0530  feat: generate the Open Graph image and icons
d861462  author 2026-10-31 07:09:57 +0530  commit 2026-10-31 07:09:57 +0530  feat: render a TODO where the video or CV file is missing
09a5ef6  author 2026-10-31 07:09:57 +0530  commit 2026-10-31 07:09:57 +0530  feat: build the repo cards and table from data/repos.json
8c480f9  author 2026-10-31 07:09:57 +0530  commit 2026-10-31 07:09:57 +0530  feat: add the five pages and the stylesheet
d6ace16  author 2026-10-31 07:01:57 +0530  commit 2026-10-31 07:01:57 +0530  chore: start the portfolio site repository

$ gh repo view --json visibility -q .visibility; gh api repos/giridhar-shenoy/portfolio-site/pages
PRIVATE
{"message":"Not Found","documentation_url":"https://docs.github.com/rest/pages/pages#get-a-apiname-pages-site","status":"404"}gh: Not Found (HTTP 404)

$ gh run list --workflow deploy.yml
completed	skipped	docs: record unattended decisions and the changelog entry	deploy	main	push	41156774243	7s	2026-10-31T01:44:18Z
completed	skipped	docs: explain preview, repos.json, the TODO convention and deploy	deploy	main	push	41156445444	1s	2026-10-31T01:40:06Z
```

### Lighthouse

Run 08:07–08:09, in the quiet window between the two R2 benchmark runs (Chrome is installed at
/usr/bin/google-chrome; no browser was installed; Lighthouse 12.6.0 ran through `npx`, which
downloads the npm package — the site spec asks for Lighthouse when Chrome is present, and there
is no apt or pip Lighthouse). Reports and the score table: `docs/lighthouse/2026-10-31/`.

| Page | Perf | A11y | BP | SEO |
|---|---|---|---|---|
| index | 100 | 100 | 100 | 100 |
| repos | 100 | 100 | 100 | 100 |
| work/orangewood-controls | 100 | 100 | 100 | 100 |
| work/bot-and-brew | 100 | 100 | 100 | 100 |
| 404 (local only) | 100 | 95 | 96 | 100 |

404 misses A11y/BP only locally: its `/portfolio-site/` URLs do not resolve from `public/`.
Headless-Chrome screenshots at 412 px and 1280 px then showed the repos table breaking repo names
one letter per line; fixed in a95fee1 (rows become labelled blocks on phones). Re-run of repos.html after the fix (09:01): 100 / 100 / 100 / 100; a 412 px screenshot shows
labelled blocks with whole repo names.

## TODOs on the site, by page

- **index.html**: CV (PDF) — add `public/assets/cv/giridhar-shenoy-cv.pdf`, run `scripts/build_media.py`.
- **work/bot-and-brew.html**:
  - the 60 s video: `public/assets/video/bot-and-brew-60s.mp4`, `bot-and-brew-60s-poster.jpg`
    (or let `scripts/optimize_media.sh` make it), `bot-and-brew-60s.en.vtt` captions; then
    `scripts/build_media.py`;
  - the link to the 2-minute YouTube (unlisted) version;
  - "What the kiosk did": step by step, the hardware, the control and sensing stack;
  - "What failed, technical";
  - "What failed, commercial": why it was not deployed and why it wound down;
  - "What I would do differently";
  - "What transferred to my engineering".
- **Not a page TODO, but before launch**: the four repos and this repo must be public, Pages
  source set to GitHub Actions, and `DEPLOY_ENABLED=true` (README "Deploy").

## CHANGELOG entry for this session

See `CHANGELOG.md` → `[Unreleased]` → Added (skeleton, five pages, stylesheet, repos.json and
build_repos.py, build_media.py, make_images.py, the five checks, check.yml and the gated
deploy.yml).

## Preview

```bash
cd ~/work/site && python3 -m http.server -d public 8000   # open http://localhost:8000/
```

## Follow-up of 1 Nov 2026

Task: remove from history the one NOTES.md line that named the excluded topic, make the deploy independent of
TODOs, drop humanoid-upper-body-retargeting from the site, rewrite ~/work/FLIP_BACK.md, re-run
the checks. Decisions below were taken without waiting, as the task asked.

### State found at 00:58 IST, before any change

- `portfolio-site` was already **PUBLIC** (the task assumed private), and the repository
  variable `DEPLOY_ENABLED` was already `true` (set 2026-10-31T19:27:08Z). A `deploy` run
  started by hand at 19:27Z failed in "Strict checks" on `check_public.py`
  (`humanoid-upper-body-retargeting: not visible anonymously`). Pages itself was not enabled
  (Pages API 404). Visibility of the others: ur5e-teaching-controllers, pointcloud-constrained-planning,
  sim-demo-to-policy and giridhar-shenoy PUBLIC; humanoid-upper-body-retargeting and
  piper-mit-teleop PRIVATE. 0 stars, 0 watchers, 0 forks.
- I did not change visibility, Pages or `DEPLOY_ENABLED`. Because the variable is `true`, every
  push below triggers the deploy job; with Pages off it stops at `configure-pages`, so nothing
  is published.

### Decisions taken (1 Nov)

1. **History rewrite done as specified, although the repo was already public.** Removing the
   word from the branch history is still the point. Backup first (bundle of all refs, kept only
   in the session scratchpad), then git-filter-repo a40bce548d2c (pip, in `.venv`) with one
   `--replace-text` rule: the exact line that started
   `- **Not in the site, though the context block mentions it**:` (in ed98984, formerly
   e865c64) becomes `(removed)`. The two continuation lines of that bullet were not part of
   the rule and stay. Origin re-added, `main` force-pushed (`6ebceb0...4bfa75e (forced
   update)`). Verification: the task's `git log -p --all | grep -ci` on the word → `0`; 14
   commits; the tree of HEAD is unchanged (`693d2af` before and after); author and committer
   dates are the original ones.
   Commit IDs that changed (old → new):

   | old | new | subject |
   |---|---|---|
   | e865c64 | ed98984 | docs: explain preview, repos.json, the TODO convention and deploy |
   | 57cc255 | 8b8f002 | test: check page weight against the 500 KB budget |
   | bb9a987 | 8371ee0 | docs: record unattended decisions and the changelog entry |
   | b8eae52 | 6bb7bb1 | docs: paste the acceptance check output and the TODO list |
   | 287be21 | a95fee1 | fix: keep repo names and the CI column readable in the repos table |
   | ea91d0e | 5338d5b | docs: add the Lighthouse reports and scores for 31 Oct |
   | 6ebceb0 | 4bfa75e | docs: re-run Lighthouse on the repos page after the table fix |

   The two prose references to 287be21 (this file, `docs/lighthouse/2026-10-31/summary.md`)
   now say a95fee1. The `git log` lines pasted under "Acceptance checks" keep the old IDs,
   because they are output as produced on 31 Oct; use the table above to map them.
2. **The old commits are still public by ID.** After the force-push, GitHub still serves
   `e865c64` and `bb9a987` anonymously (`/commit/<id>` → HTTP 200), and the Actions tab of this
   public repo lists 11 runs on the old IDs (e865c64, bb9a987, b8eae52, ea91d0e, 6ebceb0), each
   linking to its commit. Not done by me (deletion on GitHub, not asked for): delete those runs
   and ask GitHub Support to remove the unreachable commits; the commands are in
   ~/work/FLIP_BACK.md.
3. **The deploy no longer depends on TODOs.** `scripts/build_site.py` (new, standard library)
   writes `_site/`, a copy of `public/` without any element with class `todo`; the deploy
   uploads `_site/`, not `public/`. The deploy's checks are the non-strict ones from
   `check.yml` (`check_public.py --allow-private`, `check_links.py` without `--strict`,
   numbers, weight, html5validator), and the `check_todos.py` list goes to the job summary.
   The published copy is then checked: `check_todos.py --strict` on it (it must have none, so
   this only fails if the stripping breaks), internal links, html5validator. `check.yml` runs
   the same published-copy step, so a push shows what a deploy would publish. `SITE_ROOT=_site`
   (one line in `sitelib.py`) points a check at the copy. The `DEPLOY_ENABLED` gate is kept.
4. **Whatever the stripping leaves empty goes too**: a heading with nothing under it before the
   next heading of the same or a higher level (or the end of its parent), and an element that
   held a TODO and now holds nothing. Without this, the published Bot & Brew page would have
   kept the video heading and three empty post-mortem headings, and Home an empty `<p>` where
   the CV line was. Pages without a TODO are copied byte for byte (404, repos, Orangewood).
5. **Markup only, no text, on Bot & Brew**: each post-mortem heading and its content now sit in
   a `<section>`, so the rule knows where a section ends. Otherwise "What transferred to my
   engineering" would have kept the Entrepreneur First aside as its content.
6. **Two pieces of existing text depend on the video and now follow it** (build_media.py slots,
   restored verbatim when the three files exist): the Home "Watch 60 s" button, a TODO while
   the video is missing (its `#video` target is not on the published page; the Home "Bot &
   Brew" heading goes with it, as nothing is left under it), and the clause "; the video above
   is that cycle", left out while the video is missing. Checked both ways in a scratch
   worktree: with empty placeholder files for the video and CV, the button, the clause and the
   CV link come back exactly as before, and the published Bot & Brew page keeps the video
   section without the 2-minute link (still a TODO).
   Published now: Bot & Brew = title, intro, "What the kiosk did" with its sentence, "What
   failed, commercial" with its sentence, the Entrepreneur First aside. Home = everything
   except the CV line and the Bot & Brew heading and button.
7. **Your CV file**: `public/assets/cv/giridhar-shenoy-cv.pdf` appeared untracked at 00:55. Not
   committed and not opened (text and scripts only; the task treats the CV as missing). The
   generated blocks were written in a clean worktree, so they match what CI and the deploy see.
   In this working tree, while that file is present, `build_media.py --check` reports
   `index.html` stale and `build_media.py` would add the CV link. To publish it: `git add` the
   PDF, run `scripts/build_media.py`, commit.
8. **Not changed, page text**: the Bot & Brew description and Open Graph description still say
   "a fully autonomous latte cycle on video, what failed, and what transferred"; the published
   page has neither the video nor those sections yet.
9. **humanoid-upper-body-retargeting removed from the site**: its entry in `data/repos.json`,
   rebuilt with `build_repos.py` (no `--refresh-heroes`, so the other three heroes and their
   recorded commits are unchanged). The Home cards and the Repos table now list exactly
   ur5e-teaching-controllers, pointcloud-constrained-planning and sim-demo-to-policy. Its GIF
   and still were deleted from `public/assets/img/` too: nothing links to them any more, and
   they would otherwise be published at a guessable URL while the repo stays private. Two
   wording changes follow from the removal: the Repos page description and Open Graph
   description drop "humanoid retargeting" from the list of topics, and the README's
   `data/repos.json` row says "the repos on the site" instead of "the four repos". The Home
   tagline and About paragraph ("humanoid planning and retargeting", "led planning for a
   humanoid") describe the work, not the repo, and were not changed.
10. **~/work/FLIP_BACK.md rewritten** (a file, not in any repo): five repos public
    (ur5e-teaching-controllers, pointcloud-constrained-planning, sim-demo-to-policy,
    giridhar-shenoy, portfolio-site); humanoid-upper-body-retargeting and piper-mit-teleop not
    flipped; CI re-runs with `gh workflow run ci.yml --ref main` (all three code repos have a
    `workflow_dispatch` trigger; the site uses `check.yml`); the site launch steps (Pages source
    "GitHub Actions", `DEPLOY_ENABLED`, `gh workflow run deploy.yml`, every sitemap URL → 200).
    It also records the state found at 00:58 (the five already public, `DEPLOY_ENABLED` already
    `true`), and adds an optional section for the old-commit runs from decision 2.
11. **The deploy after these commits (run on fcafa99)**: every check step passed on GitHub,
    including the published-copy step; the job then failed at `actions/configure-pages@v5`
    (`enablement: false`) because Pages is not enabled. That is expected until Pages is
    switched on; nothing was uploaded or published. `check` on fcafa99: success.

### Checks (run 1 Nov after the step 4 commit, output pasted as produced)

Local checks on the working tree at 1024f4d, then the published copy (`_site/`), the visibility
print and the history count, then the generated-block check in a clean worktree. In this working
tree, `build_media.py --check` reports `index.html` STALE only because of the untracked CV file
(decision 7).

```text
$ .venv/bin/html5validator --root public --log INFO
INFO:html5validator.cli:Files to validate: 
  public/404.html
  public/index.html
  public/repos.html
  public/work/orangewood-controls.html
  public/work/bot-and-brew.html
INFO:html5validator.cli:Number of files: 5
INFO:html5validator.validator:All good.
exit 0

$ python3 scripts/check_links.py
internal: 70 links and anchors checked, 0 broken
not checked: mailto:giridharjshenoy@gmail.com
external: 12 URLs: 11 ok, 0 expected 404 until Sunday (private repos), 1 warnings, 0 failed
  ok: 200  https://github.com/giridhar-shenoy  (404.html:38, index.html:96, repos.html:79, work/bot-and-brew.html:94, work/orangewood-controls.html:54)
  ok: 200  https://github.com/giridhar-shenoy/pointcloud-constrained-planning  (index.html:63, repos.html:58)
  ok: 200  https://github.com/giridhar-shenoy/pointcloud-constrained-planning/actions/workflows/ci.yml  (repos.html:61)
  ok: 200  https://github.com/giridhar-shenoy/pointcloud-constrained-planning/actions/workflows/ci.yml/badge.svg?branch=main  (repos.html:61)
  ok: 200  https://github.com/giridhar-shenoy/sim-demo-to-policy  (index.html:71, repos.html:64)
  ok: 200  https://github.com/giridhar-shenoy/sim-demo-to-policy/actions/workflows/ci.yml  (repos.html:67)
  ok: 200  https://github.com/giridhar-shenoy/sim-demo-to-policy/actions/workflows/ci.yml/badge.svg?branch=main  (repos.html:67)
  ok: 200  https://github.com/giridhar-shenoy/ur5e-teaching-controllers  (index.html:55, repos.html:52, work/orangewood-controls.html:47)
  ok: 200  https://github.com/giridhar-shenoy/ur5e-teaching-controllers/actions/workflows/ci.yml  (repos.html:55)
  ok: 200  https://github.com/giridhar-shenoy/ur5e-teaching-controllers/actions/workflows/ci.yml/badge.svg?branch=main  (repos.html:55)
  ok: 200  https://www.ycombinator.com/companies/orangewood-labs  (work/orangewood-controls.html:44)
  warning (host blocks automated requests): 999  https://www.linkedin.com/in/giridhar-j-shenoy/  (404.html:39, index.html:97, repos.html:80, work/bot-and-brew.html:95, work/orangewood-controls.html:55)
exit 0

$ python3 scripts/check_numbers.py
Allowed digits outside TODO blocks (page · text · why · count):
  404.html · © 2026 · footer copyright line · 1
  index.html · 30 · number: the production arms · 1
  index.html · MoveIt 2 · name · 1
  index.html · ROS 2 · name · 5
  index.html · UR5e · name · 3
  index.html · ros2_control · name · 1
  index.html · ur5e-teaching-controllers · repo name · 1
  index.html · © 2026 · footer copyright line · 1
  repos.html · MoveIt 2 · name · 2
  repos.html · ROS 2 · name · 3
  repos.html · UR5e · name · 2
  repos.html · ros2_control · name · 2
  repos.html · ur5e-teaching-controllers · repo name · 1
  repos.html · © 2026 · footer copyright line · 1
  work/bot-and-brew.html · February 2026 · number: Bot & Brew wound down · 1
  work/bot-and-brew.html · ROS 2 · name · 1
  work/bot-and-brew.html · © 2026 · footer copyright line · 1
  work/orangewood-controls.html · 30 · number: the production arms · 1
  work/orangewood-controls.html · 6-axis · verbatim Orangewood paragraph · 3
  work/orangewood-controls.html · ROS 2 · name · 1
  work/orangewood-controls.html · UR5e · name · 3
  work/orangewood-controls.html · ur5e-teaching-controllers · repo name · 1
  work/orangewood-controls.html · © 2026 · footer copyright line · 1
Digits inside TODO blocks (page · token · count):
  index.html · 60 · 1
  work/bot-and-brew.html · 60-second · 1
  work/bot-and-brew.html · public/assets/video/bot-and-brew-60s-poster.jpg · 1
  work/bot-and-brew.html · public/assets/video/bot-and-brew-60s.en.vtt · 1
  work/bot-and-brew.html · public/assets/video/bot-and-brew-60s.mp4 · 1
Disallowed numbers: 0
exit 0

$ python3 scripts/check_todos.py
index.html:47: TODO CV (PDF): add public/assets/cv/giridhar-shenoy-cv.pdf, then run scripts/build_media.py.
index.html:81: TODO The "Watch 60 s" button goes here once the video is added (scripts/build_media.py).
work/bot-and-brew.html:48: TODO The 60-second video goes here. Missing files: public/assets/video/bot-and-brew-60s.mp4 public/assets/video/bot-and-brew-60s-poster.jpg public/assets/video/bot-and-brew-60s.en.vtt Add them (raw footage can go in public/assets/video/src/ for scripts/optimize_media.sh), then run scripts/build_media.py.
work/bot-and-brew.html:57: TODO Link to the longer version (YouTube, unlisted): URL not available yet.
work/bot-and-brew.html:63: TODO For Giri to write: what the kiosk did, step by step; the hardware; the control and sensing stack.
work/bot-and-brew.html:68: TODO For Giri to write: what failed technically, and how each failure showed up.
work/bot-and-brew.html:74: TODO For Giri to write: why it was not deployed, and why the company wound down.
work/bot-and-brew.html:79: TODO For Giri to write.
work/bot-and-brew.html:84: TODO For Giri to write.
9 TODO block(s)
exit 0

$ python3 scripts/check_weight.py
404.html: 8.4 KB (ok) = html 1 KB + favicon.png 0 KB, site.css 6 KB
index.html: 37.3 KB (ok) = html 6 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 6 KB, ur5e-teaching-controllers.webp 7 KB, pointcloud-constrained-planning.webp 10 KB, sim-demo-to-policy.webp 5 KB
repos.html: 12.5 KB (ok) = html 5 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 6 KB
work/bot-and-brew.html: 11.5 KB (ok) = html 4 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 6 KB
work/orangewood-controls.html: 10.4 KB (ok) = html 3 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 6 KB
exit 0

$ python3 scripts/build_site.py
404.html: no TODO, copied unchanged
index.html: removed 2 TODO block(s), 1 heading(s) left empty, 1 element(s) left empty
repos.html: no TODO, copied unchanged
work/bot-and-brew.html: removed 7 TODO block(s), 4 heading(s) left empty, 4 element(s) left empty
work/orangewood-controls.html: no TODO, copied unchanged
wrote _site
exit 0

$ SITE_ROOT=_site python3 scripts/check_todos.py --strict
0 TODO block(s)
exit 0

$ SITE_ROOT=_site python3 scripts/check_links.py --no-external
internal: 70 links and anchors checked, 0 broken
not checked: mailto:giridharjshenoy@gmail.com
external: 12 URLs not checked (--no-external)
exit 0

$ .venv/bin/html5validator --root _site --log INFO
INFO:html5validator.cli:Files to validate: 
  _site/404.html
  _site/index.html
  _site/repos.html
  _site/work/orangewood-controls.html
  _site/work/bot-and-brew.html
INFO:html5validator.cli:Number of files: 5
INFO:html5validator.validator:All good.
exit 0

$ python3 scripts/check_public.py --allow-private
    public  giridhar-shenoy/ur5e-teaching-controllers
    public  giridhar-shenoy/pointcloud-constrained-planning
    public  giridhar-shenoy/sim-demo-to-policy
    public  giridhar-shenoy/portfolio-site
all public
exit 0

$ git log -p --all | grep -ci <the word from step 1>
0

$ # clean worktree of 1024f4d (no untracked files, as in CI)
$ python3 scripts/build_repos.py --check && python3 scripts/build_media.py --check
up to date: public/index.html
up to date: public/repos.html
up to date: public/work/bot-and-brew.html
exit 0
```

## Media and Bot & Brew content (1 Nov 2026)

Task: the 60 s video, poster and captions from the full-length video; the Bot & Brew page from
`content/bot-and-brew.md`; the CV; the numbers check; deploy if enabled. Decisions taken
without waiting, as the task asked.

### Decisions taken (1 Nov, media and content)

1. **Source file name**: the full-length video is `public/assets/video/src/Demo_video.mp4`
   (not `bot-and-brew-full.mp4` as the task says): 2560×1440 H.264, about 30 fps, 123.9 s,
   with audio, 376,623,263 B. Used as is, not renamed; `src/` is git-ignored, so it stays local.
2. **The 60 s clip** comes from the task's command, now built into
   `scripts/optimize_media.sh --video SRC` so it can be regenerated. Run under
   `~/work/.locks/heavy.lock` (2 min 21 s wall). CRF 24 → 10,077,822 B, 25 → 8,464,928 B,
   26 → **7,177,426 B** (kept; the 8 MB limit taken as 8,000,000 B). Result: 1280×720 H.264
   yuv420p, 30 fps, 1860 frames (every second frame of the source's 3718: the whole cycle at
   2×, nothing cut), 62.0 s, no audio, faststart. Poster: the frame at 5 s, `-q:v 2`, 86,576 B
   (limit 150,000 B), showing the arm with the portafilter at the grinder. Captions: one cue,
   `00:00:00.000 --> 00:01:01.999`, with the task's text. The script's old generic loop
   (every file in `src/` → same-name MP4 at 1× with audio, plus a poster at 1 s) was replaced,
   because it would have written `Demo_video.mp4`, not the slot's files.
3. **Page text, word for word**: the intro, the video caption (the `<figcaption>` that
   `build_media.py` writes), the four "What the kiosk did" paragraphs and the Entrepreneur
   First paragraph are the file's text, HTML-escaped (`&` → `&amp;`) and nothing else; a
   script compared every paragraph of the file with the page's text: all seven present
   verbatim. The only other text in that part of the page is the task's link label
   "Full-length version (2 min, Google Drive)".
4. **Headings**: the file's headings name the parts they replace. "Intro", "Video caption" and
   "Entrepreneur First" are labels, so they are not shown; "What the kiosk did" is also the
   page's section heading and stays. The file has **no "What was hard, technically" section**
   (the task names one), so the page has no such heading. The page's other sections ("What
   failed, technical", "What failed, commercial" with its one sentence, "What I would do
   differently", "What transferred to my engineering") are not in the file and were removed
   with every TODO block. The video section's heading "The latte cycle on video" is not one of
   the file's headings and stays.
5. **Entrepreneur First paragraph** replaces the one-line aside in the same place and keeps
   its `aside` class (muted text), as the task replaces "the Entrepreneur First line".
6. **Removed with the old text**: the `video-ref` slot in `build_media.py` (the clause "; the
   video above is that cycle" belonged to the replaced sentence).
7. **Descriptions trimmed, deletion only**: the Bot & Brew description and Open Graph
   description no longer promise "what failed" and "what transferred", which the page no
   longer has (decision 8 of the follow-up above). No new words.
8. **check_numbers.py**: a group "facts stated by the author (content/bot-and-brew.md)",
   allowed on the Bot & Brew page only, with the task's fourteen items ("thirty to fifty"
   appears in the file as "thirty and fifty" and is matched that way). The check fails only on
   digits, so the spelled-out entries just put those numbers in the inventory. Two more
   allowances: "2 min" (the task's link label) and "MP4" as a name (the player's generated
   fallback link "Download the video (MP4)"). A negative test on a scratch copy
   (`SITE_ROOT`) with "9 bar", "8 minutes" and "31 production arms" failed with exactly those.
9. **The CV** is committed and linked from Home by `build_media.py`. I checked only that it is
   a 2-page PDF with no "TODO"/"TBD"/"lorem"/"xxx" in its text; I did not read it otherwise.
10. **`content/bot-and-brew.md` is committed** as the source of the page text (outside
    `public/`, so not published).
11. **sitemap.xml**: `lastmod` 2026-11-01 for Home, repos and Bot & Brew, which changed today.
12. **Deploy**: `DEPLOY_ENABLED` is `true`, but Pages is still not enabled (Pages API 404 at
    01:40), so the push runs the deploy job and it stops at `configure-pages`; nothing goes
    live, and the live URLs cannot be fetched yet.

### For the author: where the file disagrees with something else on the site

- **Cycle time vs the video.** The file says "One cycle took roughly eight minutes", but the
  full-length video of "one autonomous cycle" is 2 min 4 s, and the caption, the captions file
  and the Home "Watch 60 s" button present the 60 s clip as that cycle "at 2× speed". If a cycle
  took about eight minutes, the full-length video is already condensed (several angles; the
  footage carries a "Bot and Brew" title), so "2× speed" understates the compression and
  "Full-length version" reads as real time.
- **"An engineering post-mortem"** (the page title, and Home's "Case study: Bot & Brew, an
  engineering post-mortem"): the page no longer has a section on what failed or what
  transferred; the only verdict is the Entrepreneur First paragraph's "not a venture-scale
  business".
- Not from the file: Home's tagline says "Controllers running on 30 production arms" (present
  tense), while the Orangewood page says both controllers "stayed in service until the next
  hardware generation".

### Checks (run 1 Nov before the content commit, output pasted as produced)

```text
$ .venv/bin/html5validator --root public --log INFO
INFO:html5validator.cli:Number of files: 5
INFO:html5validator.validator:All good.
exit 0

$ python3 scripts/check_links.py
internal: 76 links and anchors checked, 0 broken
not checked: mailto:giridharjshenoy@gmail.com
external: 13 URLs: 12 ok, 0 expected 404 until Sunday (private repos), 1 warnings, 0 failed
  ok: 200  https://drive.google.com/file/d/1dx2QZJ8dTxYjlFIyCTR4aFR4TP-qykYk/view  (work/bot-and-brew.html:57)
  ok: 200  https://github.com/giridhar-shenoy  (404.html:38, index.html:96, repos.html:79, work/bot-and-brew.html:75, work/orangewood-controls.html:54)
  ok: 200  https://github.com/giridhar-shenoy/pointcloud-constrained-planning  (index.html:63, repos.html:58)
  ok: 200  https://github.com/giridhar-shenoy/pointcloud-constrained-planning/actions/workflows/ci.yml  (repos.html:61)
  ok: 200  https://github.com/giridhar-shenoy/pointcloud-constrained-planning/actions/workflows/ci.yml/badge.svg?branch=main  (repos.html:61)
  ok: 200  https://github.com/giridhar-shenoy/sim-demo-to-policy  (index.html:71, repos.html:64)
  ok: 200  https://github.com/giridhar-shenoy/sim-demo-to-policy/actions/workflows/ci.yml  (repos.html:67)
  ok: 200  https://github.com/giridhar-shenoy/sim-demo-to-policy/actions/workflows/ci.yml/badge.svg?branch=main  (repos.html:67)
  ok: 200  https://github.com/giridhar-shenoy/ur5e-teaching-controllers  (index.html:55, repos.html:52, work/orangewood-controls.html:47)
  ok: 200  https://github.com/giridhar-shenoy/ur5e-teaching-controllers/actions/workflows/ci.yml  (repos.html:55)
  ok: 200  https://github.com/giridhar-shenoy/ur5e-teaching-controllers/actions/workflows/ci.yml/badge.svg?branch=main  (repos.html:55)
  ok: 200  https://www.ycombinator.com/companies/orangewood-labs  (work/orangewood-controls.html:44)
  warning (host blocks automated requests): 999  https://www.linkedin.com/in/giridhar-j-shenoy/  (404.html:39, index.html:97, repos.html:80, work/bot-and-brew.html:76, work/orangewood-controls.html:55)
exit 0

$ python3 scripts/check_numbers.py
Allowed digits outside TODO blocks (page · text · why · count):
  404.html · © 2026 · footer copyright line · 1
  index.html · 30 · number: the production arms · 1
  index.html · 60 s · label of the 60-second video · 1
  index.html · MoveIt 2 · name · 1
  index.html · ROS 2 · name · 5
  index.html · UR5e · name · 3
  index.html · ros2_control · name · 1
  index.html · ur5e-teaching-controllers · repo name · 1
  index.html · © 2026 · footer copyright line · 1
  repos.html · MoveIt 2 · name · 2
  repos.html · ROS 2 · name · 3
  repos.html · UR5e · name · 2
  repos.html · ros2_control · name · 2
  repos.html · ur5e-teaching-controllers · repo name · 1
  repos.html · © 2026 · footer copyright line · 1
  work/bot-and-brew.html · 1 November 2026 · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · 2 min · label of the full-length video link · 1
  work/bot-and-brew.html · 2× · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · August 2025 · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · FR5 · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · February 2026 · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · January 2026 · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · LubanCat 5 · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · MP4 · name: the video file format · 1
  work/bot-and-brew.html · MoveIt 2 · name · 1
  work/bot-and-brew.html · ROS 2 · name · 2
  work/bot-and-brew.html · September 2026 · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · eight minutes · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · five feet by five · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · nine bar · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · six-axis · facts stated by the author (content/bot-and-brew.md) · 2
  work/bot-and-brew.html · thirty and fifty · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · two months · facts stated by the author (content/bot-and-brew.md) · 1
  work/bot-and-brew.html · © 2026 · footer copyright line · 1
  work/orangewood-controls.html · 30 · number: the production arms · 1
  work/orangewood-controls.html · 6-axis · verbatim Orangewood paragraph · 3
  work/orangewood-controls.html · ROS 2 · name · 1
  work/orangewood-controls.html · UR5e · name · 3
  work/orangewood-controls.html · ur5e-teaching-controllers · repo name · 1
  work/orangewood-controls.html · © 2026 · footer copyright line · 1
Digits inside TODO blocks (page · token · count):
Disallowed numbers: 0
exit 0

$ python3 scripts/check_todos.py
0 TODO block(s)
exit 0

$ python3 scripts/check_weight.py
404.html: 8.4 KB (ok) = html 1 KB + favicon.png 0 KB, site.css 6 KB
index.html: 37.2 KB (ok) = html 6 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 6 KB, ur5e-teaching-controllers.webp 7 KB, pointcloud-constrained-planning.webp 10 KB, sim-demo-to-policy.webp 5 KB
repos.html: 12.5 KB (ok) = html 5 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 6 KB
work/bot-and-brew.html: 12.7 KB (ok) = html 5 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 6 KB
work/orangewood-controls.html: 10.4 KB (ok) = html 3 KB + favicon.png 0 KB, site.webmanifest 0 KB, site.css 6 KB
exit 0

$ python3 scripts/build_repos.py --check && python3 scripts/build_media.py --check
up to date: public/index.html
up to date: public/repos.html
up to date: public/work/bot-and-brew.html
exit 0

$ python3 scripts/build_site.py
404.html: no TODO, copied unchanged
index.html: no TODO, copied unchanged
repos.html: no TODO, copied unchanged
work/bot-and-brew.html: no TODO, copied unchanged
work/orangewood-controls.html: no TODO, copied unchanged
wrote _site
exit 0

$ SITE_ROOT=_site python3 scripts/check_todos.py --strict
0 TODO block(s)
exit 0

$ SITE_ROOT=_site python3 scripts/check_links.py --no-external
internal: 76 links and anchors checked, 0 broken
not checked: mailto:giridharjshenoy@gmail.com
external: 13 URLs not checked (--no-external)
exit 0

$ .venv/bin/html5validator --root _site --log INFO
INFO:html5validator.cli:Number of files: 5
INFO:html5validator.validator:All good.
exit 0

$ ls -l public/assets/video public/assets/cv (published media)
76492 public/assets/cv/giridhar-shenoy-cv.pdf
86576 public/assets/video/bot-and-brew-60s-poster.jpg
133 public/assets/video/bot-and-brew-60s.en.vtt
7177426 public/assets/video/bot-and-brew-60s.mp4
```

13. **CI fix after the content commit**: `check` and `deploy` failed on f564fd5 in "Generated
    blocks are up to date" / "Build": `STALE: public/work/bot-and-brew.html`. The runner has no
    `ffprobe`, so `build_media.py` wrote the player without `width="1280" height="720"`, while my
    machine has it. `build_media.py` now reads the size from the MP4's track header (`tkhd`) in
    plain Python, so both write the same block; checked against ffprobe on the clip (1280×720)
    and the source (2560×1440).

## Bot & Brew rewrite (1 Nov 2026)

Task: the author's new text for `content/bot-and-brew.md`, the page made from it, a new title,
captions off by default, the full-length link removed.

### Decisions taken (1 Nov, Bot & Brew rewrite)

1. **`content/bot-and-brew.md`** replaced with the author's text, word for word, from
   "## Intro" through "...before building the hardware." (the spaces before the closing
   delimiter dropped). Its own wording is kept as written ("inhouse", "business side things").
2. **Page text, word for word**: no script in `scripts/` makes this comparison (the grep for
   `bot-and-brew.md` finds only `check_numbers.py`, which checks numbers, not wording), so, as
   on 1 Nov, a scratch script compared it: all nine paragraphs of the file appear verbatim on
   the page (after `&` → `&amp;` and whitespace collapse). The only other text in `<main>` is
   the h1, the h2s and the player's fallback link "Download the video (MP4)".
3. **Structure**: intro under the h1; the video section (heading "The latte cycle on video"
   kept); then "What the kiosk did", "How it went" (`id="how-it-went"`) and "What I take from
   it" (`id="what-i-take"`) as `<section>`s with h2s, like the existing one. "Intro" and
   "Video caption" are labels, not shown. The `<p class="aside">` Entrepreneur First paragraph
   is gone; the `.aside` rule in `site.css` is now unused and was left in place (the
   stylesheet was not part of the task).
4. **Title** "Bot & Brew: a robotic coffee kiosk" in `<title>`, h1 and og:title; description and
   og:description as the task gives them; Home's "More" link reads "Case study: Bot & Brew, a
   robotic coffee kiosk". `grep -rn "post-mortem\|post mortem" public/ scripts/ data/ content/
   README.md` returns nothing; CHANGELOG.md and NOTES.md keep the old name as history.
5. **Captions off by default**: `default` removed from the `<track>`; the track and the `.vtt`
   stay (cue text unchanged). Checked in headless Chrome: the new page's track mode is
   `disabled`, the previous commit's was `showing`.
6. **Figcaption from the file**: `build_media.py` reads the "## Video caption" section of
   `content/bot-and-brew.md` (whitespace collapsed, HTML-escaped) and exits with an error if the
   section is missing, so a caption edit is one change in the file plus `build_media.py`, and
   CI's `--check` catches a page that was not regenerated.
7. **Full-length link removed** from the page, with the "2 min" entry and its docstring mention
   in `check_numbers.py`. The Drive file was not touched. `check_links.py` now sees 12
   external URLs instead of 13.
8. **check_numbers.py**: nothing in the new text was flagged, so no entry was added. "eight
   minutes" now counts 2 (caption and "What the kiosk did"). The intro's "Two months" (capital
   T) is not matched by the lowercase `\btwo months\b`; it has no digit, so it cannot fail and
   only misses the review inventory. Left as is, so the check is not loosened.
9. **README** row for `content/bot-and-brew.md` updated to the new section names; CHANGELOG
   entries added. `sitemap.xml` already has `lastmod` 2026-11-01 for Home and Bot & Brew.
10. Video, poster, `optimize_media.sh`, CV and the other pages were not touched.

## Industry work page (1 Nov 2026)

Task: the Orangewood page becomes "Industry work: Orangewood Labs and MyActuator", with a line
per controller, Orangewood's media and a MyActuator section; Home's About names both employers.

### Decisions taken (1 Nov, Industry work)

1. **File and URL kept**: `public/work/orangewood-controls.html` (linked, in the sitemap);
   `sitemap.xml` `lastmod` for it → 2026-11-01. Title, h1 and og:title, description and
   og:description as the task gives them. Nav label "Industry work" on all five pages (the nav is
   hand-written in each page; no script generates it).
2. **Page text, word for word**: a scratch script compared every h1/h2/p/li of the published page
   with the task's text, in order: identical. The first paragraph is unchanged. h2 ids added for
   anchors (`orangewood`, `myactuator`), as the page's old h2 had one. The "Code and results" h2
   and its sentence are gone; with them the page no longer mentions the UR5e.
3. **Repo links**: every occurrence of a repo name links to `https://github.com/giridhar-shenoy/<repo>`,
   the URL the Repos page uses (three for ur5e-teaching-controllers, one for
   pointcloud-constrained-planning), as plain anchors without the table's `<wbr>` breaks.
4. **Media links**: TechCrunch is the 2 Aug 2023 article
   https://techcrunch.com/2023/08/02/orangewood-wants-to-build-a-cheap-programmable-robotic-arm-for-manufacturing/
   (found by search, 200 with the trailing slash). **No demo video**: the task left
   `<DEMO_VIDEO_URL>` as a placeholder and I found no video Orangewood links itself (YC company
   and launch pages, orangewood.co); the author chose to ship without that item. Add it as one
   more `<li>` in "Orangewood's own media" when there is a URL. Links only; nothing of either
   employer's product is embedded.
5. **check_numbers.py**: the four flagged tokens (2022, 2024, 2024, 2025) are allowed as the two
   ranges, `\b2022 to 2024\b` and `\b2024 to 2025\b`, reason "employment years, as on the CV",
   Orangewood page only; not as bare years, so a stray year anywhere still fails. Docstring rule
   updated. Negative test on a scratch copy (`SITE_ROOT`): "since 2024", "12 arms", "2024 to
   2026" on the page and "2022 to 2024" on Home all failed (6 disallowed, exit 1).
6. **Home**: only the nav label, the About sentence and the "More" item changed.
7. **Rules checked**: no "Simulink" or "auto-tuner" anywhere in `public/`; the page has no video,
   image, GIF or iframe and no sentence about applying or hiring. Home's About still ends with
   "open to engineering seats at robotics companies and research-engineer seats in labs alike"
   (unchanged, as the task said nothing else on Home changes).

## Industry work page, final (1 Nov 2026)

Task (prompt 5, superseding prompts 3, 3b and 4): MyActuator first with MyActuator's own video,
Orangewood second with the workshop photo and the method lines.

Orangewood gave written permission on 1 Nov 2026 to use this photo on the site.

### Decisions taken (1 Nov, Industry work final)

1. **Photo**: the original (`IMG-20230925-WA0007.jpg.jpeg`, 576×1280, 109,192 B) is copied to
   `media_src/orangewood-arms-original.jpeg`; `/media_src/` is added to `.gitignore`, so the
   original is never committed. It already had no EXIF, GPS, ICC or XMP (WhatsApp strips them).
   `public/assets/img/orangewood-arms.jpg` was made with Pillow: orientation applied, a fresh RGB
   image (no info carried over), Lanczos to a 1200 px longer side, JPEG quality 82, optimized,
   progressive, saved with no exif/icc/comment. Result: **540×1200, 117,456 B (114.7 KiB)**, under
   200 KB at the first quality tried. Verified by walking the JPEG segments: only the JFIF APP0
   header (density 1×1), quantization and Huffman tables, frame and scan; no APP1 (EXIF/XMP), APP2
   (ICC) or COM. No crop.
2. **Placeholders**: `<SS>` and `<M:SS>` were not filled, so the iframe has no `?start=` and the
   figcaption ends at "their YouTube channel." without the "I appear at" sentence.
   `<DEMO_VIDEO_URL>` was not filled: bullet dropped. `<TECHCRUNCH_URL>` was also left as a
   placeholder in this prompt, but the TechCrunch link was found, checked and accepted in the
   previous round (live since 571bf2c), so it stays; drop it if that was not intended.
3. **Video**: oEmbed confirms 0hYw6lilqxE is "Myactuator Company Introduction." by "Actuator My"
   (`https://www.youtube.com/@actuatormy8760`, the channel linked in the caption) and is
   embeddable. Nothing was downloaded from YouTube. Neither `check_public.py` (repo visibility
   only) nor the README spec ("no framework, no build tool, no analytics") forbids a third-party
   iframe, so the embed is used, not the fallback link; `check_links.py` HEAD-checks the iframe
   `src` (200).
4. **`loading="lazy"` removed from the iframe**: the pinned validator (html5validator 0.4.2,
   also in CI) rejects `loading` on `<iframe>` ("Attribute loading not allowed on element iframe
   at this point"); the attribute is in the current HTML standard but newer than that validator.
   The validator was not loosened. The video is the first thing in `<main>`, so on desktop it is
   in the first viewport and would have loaded at once anyway. The `<img>` keeps
   `loading="lazy"`.
5. **CSS**: the task's three rules, plus `display: block` and `border: 0` on the iframe (no
   default inset border) and `display: block` on `.photo img`; `.photo-right img { width: 100% }`
   below 721 px (full width above the text); from 721 px `.photo-right` floats right,
   `max-width: 34%`, `margin-left: 1.5rem`. To keep the float inside its page and section:
   `main { display: flow-root }` and `main h2 { clear: both }` (nothing else on the site floats).
6. **Previews** (headless Chrome, fresh profile each time; a reused profile had served the old
   cached stylesheet): Industry work at 1280 px: full-width 16:9 video, photo floated right beside
   the Orangewood paragraph and list. At 390 px: video full width, photo full width above the text
   (about 358×796 px, nearly a phone screen tall, as specified).
7. **Home photo left out**: at 390 px the portrait filled about a whole phone screen right under
   "About", pushing the About text and CV link a screen down. At 1280 px it sat well beside the
   paragraph. Per the task, Home has no photo. Home's only change in this round: the "More" item
   "Industry work: MyActuator and Orangewood Labs". The About sentence was already the task's.
8. **check_numbers.py**: the one new flagged token was "2023." in the photo caption. Allowed as
   `\bworkshop, 2023\b` on this page only, beside the two ranges; all three carry the reason
   "employment and photo years, as on the CV". Bare years are still not allowed. Negative test on
   a scratch copy: "No public rebuild in 2023." on the page and "In the workshop, 2023," on Home
   both failed (exit 1).
9. **Placeholder grep**: `grep -rn "post-mortem\|TODO\|<SS>\|<M:SS>\|<TECHCRUNCH\|<DEMO" public/`
   finds nothing in any HTML page. Its only hits are `site.css:401` and `:420`, the existing
   comment and `content: "TODO"` label that style TODO blocks (the mechanism README describes).
   They were left as they are.
10. **Licence notes**: `CONTENT_LICENSE.md` claimed every image under `public/assets/` as the
    author's, and `THIRD_PARTY.md` said "None". Both now name the photo (used with Orangewood's
    written permission) as the exception; `THIRD_PARTY.md` also notes the YouTube embed.
11. **Rules checked**: no other image added; no "Simulink" or "auto-tuner" in `public/`; alt and
    captions are exactly the task's; no sentence about applying or hiring on the page. Home's
    About still ends "open to engineering seats at robotics companies and research-engineer seats
    in labs alike" (unchanged, see the previous section).
