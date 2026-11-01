"""Generate the Open Graph image and the icons: plain text on a flat colour, no artwork.

  python3 scripts/make_images.py   # needs Pillow and the DejaVu fonts (local only)

Writes public/assets/img/{og.png, favicon.png, apple-touch-icon.png, icon-192.png, icon-512.png}.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

from sitelib import PUBLIC

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BG, FG, MUTED = "#1f4e79", "#ffffff", "#cfe0f1"
NAME = "Giridhar J Shenoy"
TAGLINE = ("Robotics engineer — manipulator control and ROS 2 systems. Controllers shipped on 30 production "
           "arms; humanoid planning and retargeting; moving into learning-based manipulation.")
OUT = PUBLIC / "assets" / "img"


def font(bold, size):
    return ImageFont.truetype(FONT_DIR + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)


def og():
    im = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(im)
    d.text((80, 150), NAME, font=font(True, 76), fill=FG)
    y = 280
    for line in textwrap.wrap(TAGLINE, 46):
        d.text((80, y), line, font=font(False, 36), fill=MUTED)
        y += 52
    im.save(OUT / "og.png", optimize=True)


def icon(size, name):
    im = Image.new("RGB", (size, size), BG)
    d = ImageDraw.Draw(im)
    f = font(True, int(size * 0.42))
    box = d.textbbox((0, 0), "GJS", font=f)
    while box[2] - box[0] > size * 0.86:
        f = font(True, f.size - 1)
        box = d.textbbox((0, 0), "GJS", font=f)
    d.text(((size - (box[2] - box[0])) / 2 - box[0], (size - (box[3] - box[1])) / 2 - box[1]), "GJS", font=f, fill=FG)
    im.save(OUT / name, optimize=True)


if __name__ == "__main__":
    og()
    for size, name in ((32, "favicon.png"), (180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")):
        icon(size, name)
    for p in sorted(OUT.glob("*.png")):
        print(f"{p.stat().st_size:8d} B  {p.relative_to(PUBLIC)}")
