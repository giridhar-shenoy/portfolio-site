"""Fill the media slots: a missing file renders a visible TODO block, a present one renders the
player or link, and the build passes either way.

  python3 scripts/build_media.py           # rewrite the slots from what is on disk
  python3 scripts/build_media.py --check   # exit 1 if a slot does not match the files (CI)

Slots: the 60 s Bot & Brew video (mp4 + poster + WebVTT captions, off unless the viewer turns
them on) and the CV (PDF). The video's caption is the "Video caption" section of
content/bot-and-brew.md. The Home "Watch 60 s" button follows the video (a TODO while the video
is missing).
"""
import argparse
import html
import os
import re
import struct
import sys

from sitelib import PUBLIC, ROOT, replace_block, write_or_check

VIDEO = {
    "mp4": "assets/video/bot-and-brew-60s.mp4",
    "poster": "assets/video/bot-and-brew-60s-poster.jpg",
    "vtt": "assets/video/bot-and-brew-60s.en.vtt",
}
CV = "assets/cv/giridhar-shenoy-cv.pdf"
CONTENT = ROOT / "content" / "bot-and-brew.md"


def video_caption():
    """The "## Video caption" section of the author's text, as one line of HTML-escaped text."""
    m = re.search(r"^## Video caption\n(.*?)(?=^## |\Z)", CONTENT.read_text(encoding="utf-8"), re.M | re.S)
    if not m or not m.group(1).strip():
        sys.exit(f"build_media: no '## Video caption' section in {CONTENT.relative_to(ROOT)}")
    return html.escape(" ".join(m.group(1).split()), quote=False)


def boxes(f, end):
    """Yield (type, end offset) for each MP4 box from the current position up to ``end``; the
    file is left at the start of the box's payload."""
    while f.tell() + 8 <= end:
        start = f.tell()
        size, kind = struct.unpack(">I4s", f.read(8))
        if size == 1:
            size = struct.unpack(">Q", f.read(8))[0]
        elif size == 0:
            size = end - start
        yield kind, start + size
        f.seek(start + size)


def video_size(path):
    """Width and height of the video track, read from the MP4's track header (moov/trak/tkhd),
    so a local build and CI (which has no ffprobe) write the same attributes."""
    with open(path, "rb") as f:
        for kind, end in boxes(f, os.fstat(f.fileno()).st_size):
            if kind != b"moov":
                continue
            for kind, trak_end in boxes(f, end):
                if kind != b"trak":
                    continue
                for kind, box_end in boxes(f, trak_end):
                    if kind == b"tkhd":
                        f.seek(box_end - 8)  # tkhd ends with width and height, 16.16 fixed point
                        w, h = struct.unpack(">II", f.read(8))
                        if w and h:
                            return w >> 16, h >> 16
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
<track kind="captions" src="{up}{VIDEO['vtt']}" srclang="en" label="English">
<a href="{up}{VIDEO['mp4']}">Download the video (MP4)</a>
</video>
<figcaption>{video_caption()}</figcaption>
</figure>
"""


def watch_slot(up):
    if video_present():
        return f'\n<p><a class="button" href="{up}work/bot-and-brew.html#video">Watch 60 s</a></p>\n'
    return ('\n<p class="todo">The "Watch 60 s" button goes here once the video is added '
            '(<code>scripts/build_media.py</code>).</p>\n')


def cv_slot(up):
    if (PUBLIC / CV).is_file():
        return f'<a href="{up}{CV}">CV (PDF)</a>'
    return f'<span class="todo">CV (PDF): add <code>public/{CV}</code>, then run <code>scripts/build_media.py</code>.</span>'


SLOTS = (("work/bot-and-brew.html", "bot-and-brew-60s", video_slot, "../"),
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
