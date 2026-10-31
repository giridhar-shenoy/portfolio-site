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

## Decisions taken unattended (31 Oct)
