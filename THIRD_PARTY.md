# Third-party material

No third-party code, fonts or icons are vendored. The site uses the reader's system fonts.
Two exceptions, both on the Industry work page (`work/orangewood-controls.html`):

- `public/assets/img/orangewood-arms.jpg`: a photo used with Orangewood Labs' written permission
  (1 Nov 2026), metadata stripped.
- MyActuator's YouTube video, embedded from `youtube-nocookie.com`; the player and video load
  from YouTube, nothing of it is copied into this repository.
 The hero GIFs come from the author's own repositories (see `data/repos.json`
for each source path and commit).

Tools used at build or check time, not shipped with the site: Python 3 standard library,
Pillow (Open Graph image and icons), ffmpeg (`scripts/optimize_media.sh`), html5validator
(Nu Html Checker) in CI, Lighthouse for the local audit.
