"""Fill the media slots: a missing file renders a visible TODO block, a present one renders the
player or link, and the build passes either way.

  python3 scripts/build_media.py           # rewrite the slots from what is on disk
  python3 scripts/build_media.py --check   # exit 1 if a slot does not match the files (CI)

Slots: the 60 s Bot & Brew video (mp4 + poster + WebVTT captions) and the CV (PDF). Two more
follow the video: the Home "Watch 60 s" button (a TODO while the video is missing) and the
clause on the Bot & Brew page that points at the player (left out while it is missing).
"""
import argparse
import json
import shutil
import subprocess
import sys

from sitelib import PUBLIC, replace_block, write_or_check

VIDEO = {
    "mp4": "assets/video/bot-and-brew-60s.mp4",
    "poster": "assets/video/bot-and-brew-60s-poster.jpg",
    "vtt": "assets/video/bot-and-brew-60s.en.vtt",
}
CV = "assets/cv/giridhar-shenoy-cv.pdf"


def video_size(path):
    if not shutil.which("ffprobe"):
        return None
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height", "-of", "json", str(path)], capture_output=True, text=True)
    try:
        s = json.loads(out.stdout)["streams"][0]
        return s["width"], s["height"]
    except (KeyError, IndexError, ValueError):
        return None


def video_present():
    return all((PUBLIC / f).is_file() for f in VIDEO.values())


def video_slot(up):
    missing = [f for f in VIDEO.values() if not (PUBLIC / f).is_file()]
    if missing:
        items = "\n".join(f"<li><code>public/{f}</code></li>" for f in missing)
        return f"""
<div class="todo">The 60-second video goes here. Missing files:
<ul>
{items}
</ul>
Add them (raw footage can go in <code>public/assets/video/src/</code> for
<code>scripts/optimize_media.sh</code>), then run <code>scripts/build_media.py</code>.</div>
"""
    wh = video_size(PUBLIC / VIDEO["mp4"])
    dims = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
    return f"""
<figure>
<video controls preload="metadata" playsinline poster="{up}{VIDEO['poster']}"{dims}>
<source src="{up}{VIDEO['mp4']}" type="video/mp4">
<track kind="captions" src="{up}{VIDEO['vtt']}" srclang="en" label="English" default>
<a href="{up}{VIDEO['mp4']}">Download the video (MP4)</a>
</video>
<figcaption>The autonomous latte cycle, start to finish, with no human intervention.</figcaption>
</figure>
"""


def watch_slot(up):
    if video_present():
        return f'\n<p><a class="button" href="{up}work/bot-and-brew.html#video">Watch 60 s</a></p>\n'
    return ('\n<p class="todo">The "Watch 60 s" button goes here once the video is added '
            '(<code>scripts/build_media.py</code>).</p>\n')


def video_ref_slot(up):
    return "; the video above is that cycle" if video_present() else ""


def cv_slot(up):
    if (PUBLIC / CV).is_file():
        return f'<a href="{up}{CV}">CV (PDF)</a>'
    return f'<span class="todo">CV (PDF): add <code>public/{CV}</code>, then run <code>scripts/build_media.py</code>.</span>'


SLOTS = (("work/bot-and-brew.html", "bot-and-brew-60s", video_slot, "../"),
         ("work/bot-and-brew.html", "video-ref", video_ref_slot, "../"),
         ("index.html", "watch", watch_slot, ""),
         ("index.html", "cv", cv_slot, ""))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    ok = True
    for page, name, render, up in SLOTS:
        path = PUBLIC / page
        ok &= write_or_check(path, replace_block(path.read_text(encoding="utf-8"), "build_media", name, render(up)),
                             a.check)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
