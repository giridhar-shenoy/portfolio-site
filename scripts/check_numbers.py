"""Inventory every digit a reader can see on the site, and fail on any that is not allowed.

  python3 scripts/check_numbers.py

The rule: the only numbers on the site are 30 (the production arms, on the Home page and the
Orangewood page) and February 2026, unless they sit inside a visible TODO block. Digits that
are part of a name (ROS 2, MoveIt 2, UR5e, Unitree G1, ros2_control, pybind11,
ur5e-teaching-controllers, MP4), the "6-axis" in the Orangewood
paragraph, the copyright year in the footer and the "60 s" label of the video are listed
separately so they can be reviewed, and are not counted as numbers.

Scanned: visible text, <title>, alt / title / aria-label attributes, and the description and
Open Graph text fields. Not scanned: URLs, file names, image dimensions.

The Bot & Brew page also carries the numbers its author states in content/bot-and-brew.md;
they are allowed there only, as the group "facts stated by the author", and so is the "2 min"
in the label of the full-length video link. A number is anything with a digit in it, so only
the digit-bearing entries can fail; the spelled-out ones (nine bar, two months, ...) are matched
so that they appear in the inventory for review.
"""
import re
import sys
from collections import Counter
from html.parser import HTMLParser

from sitelib import PUBLIC, pages

HOME, ORANGEWOOD, BOT_AND_BREW = "index.html", "work/orangewood-controls.html", "work/bot-and-brew.html"
AUTHOR = "facts stated by the author (content/bot-and-brew.md)"
# (regex, why it is allowed, pages it is allowed on or None for every page)
ALLOWED = [
    (r"\bnine bar\b", AUTHOR, {BOT_AND_BREW}),
    (r"\btwo months\b", AUTHOR, {BOT_AND_BREW}),
    (r"\bthirty and fifty\b", AUTHOR, {BOT_AND_BREW}),
    (r"\bfive feet by five\b", AUTHOR, {BOT_AND_BREW}),
    (r"\beight minutes\b", AUTHOR, {BOT_AND_BREW}),
    (r"\bJanuary 2026\b", AUTHOR, {BOT_AND_BREW}),
    (r"\bAugust 2025\b", AUTHOR, {BOT_AND_BREW}),
    (r"\bFebruary 2026\b", AUTHOR, {BOT_AND_BREW}),
    (r"\bSeptember 2026\b", AUTHOR, {BOT_AND_BREW}),
    (r"\b1 November 2026\b", AUTHOR, {BOT_AND_BREW}),
    (r"\bsix-axis\b", AUTHOR, {BOT_AND_BREW}),
    (r"\b2×", AUTHOR, {BOT_AND_BREW}),
    (r"\bLubanCat 5\b", AUTHOR, {BOT_AND_BREW}),
    (r"\bFR5\b", AUTHOR, {BOT_AND_BREW}),
    (r"\b2 min\b", "label of the full-length video link", {BOT_AND_BREW}),
    (r"\b30\b", "number: the production arms", {HOME, ORANGEWOOD}),
    (r"\bFebruary 2026\b", "number: Bot & Brew wound down", None),
    (r"\bROS 2\b", "name", None),
    (r"\bMoveIt 2\b", "name", None),
    (r"\bUR5e\b", "name", None),
    (r"\bUnitree G1\b", "name", None),
    (r"\bros2_control\b", "name", None),
    (r"\bpybind11\b", "name", None),
    (r"\bMP4\b", "name: the video file format", None),
    (r"\bur5e-teaching-controllers\b", "repo name", None),
    (r"\b6-axis\b", "verbatim Orangewood paragraph", {ORANGEWOOD}),
    (r"© 2026", "footer copyright line", None),
    (r"\b60 s\b", "label of the 60-second video", None),
]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
TEXT_ATTRS = ("alt", "title", "aria-label")
META_TEXT = {"description", "og:title", "og:description", "og:image:alt"}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth, self.todo, self.skip = 0, [], 0
        self.chunks = []  # (line, text, inside_todo)

    def add(self, text):
        if text.strip():
            self.chunks.append((self.getpos()[0], text, bool(self.todo)))

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for k in TEXT_ATTRS:
            if a.get(k):
                self.add(a[k])
        if tag == "meta" and (a.get("name") in META_TEXT or a.get("property") in META_TEXT):
            self.add(a.get("content") or "")
        if tag in VOID:
            return
        self.depth += 1
        if tag in ("script", "style"):
            self.skip += 1
        if "todo" in (a.get("class") or "").split():
            self.todo.append(self.depth)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag in ("script", "style"):
            self.skip -= 1
        if self.todo and self.todo[-1] == self.depth:
            self.todo.pop()
        self.depth -= 1

    def handle_data(self, data):
        if not self.skip:
            self.add(data)


def main():
    allowed, in_todo, bad = Counter(), Counter(), []
    for page in pages():
        rel = page.relative_to(PUBLIC).as_posix()
        p = Text()
        p.feed(page.read_text(encoding="utf-8").replace("<wbr>", ""))  # keep names whole
        for line, text, todo in p.chunks:
            text = re.sub(r"\s+", " ", text)
            if todo:
                for m in re.finditer(r"\S*\d\S*", text):
                    in_todo[(rel, m.group(0))] += 1
                continue
            rest = text
            for rx, why, where in ALLOWED:
                if where is None or rel in where:
                    for m in re.finditer(rx, rest):
                        allowed[(rel, m.group(0), why)] += 1
                    rest = re.sub(rx, " ", rest)
            for m in re.finditer(r"\S*\d\S*", rest):
                bad.append(f"{rel}:{line}: '{m.group(0)}' in: {text.strip()[:100]}")
    print("Allowed digits outside TODO blocks (page · text · why · count):")
    for (rel, tok, why), n in sorted(allowed.items()):
        print(f"  {rel} · {tok} · {why} · {n}")
    print("Digits inside TODO blocks (page · token · count):")
    for (rel, tok), n in sorted(in_todo.items()):
        print(f"  {rel} · {tok} · {n}")
    print(f"Disallowed numbers: {len(bad)}")
    for b in bad:
        print(f"  {b}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
