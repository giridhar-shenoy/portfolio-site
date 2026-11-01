# Third-party material

No third-party code, fonts or icons are vendored. The site uses the reader's system fonts.
Two exceptions, both on the Industry work page (`work/orangewood-controls.html`):

- `public/assets/img/orangewood-arms.jpg`: a photo used with Orangewood Labs' written permission
  (1 Nov 2026), metadata stripped.
- `public/assets/img/myactuator-team.jpg`: a still (3:01.06) from MyActuator's company video
  (https://www.youtube.com/watch?v=0hYw6lilqxE), used with MyActuator's permission and credited
  and linked in its caption, metadata stripped. The downloaded video stays in the git-ignored
  `media_src/`.
 The hero GIFs come from the author's own repositories (see `data/repos.json`
for each source path and commit).

Tools used at build or check time, not shipped with the site: Python 3 standard library,
Pillow (Open Graph image and icons), ffmpeg (`scripts/optimize_media.sh`), html5validator
(Nu Html Checker) in CI, Lighthouse for the local audit.
