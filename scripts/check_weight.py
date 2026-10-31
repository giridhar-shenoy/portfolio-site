"""Page weight without video: each page's HTML plus every stylesheet, image and icon it loads.

  python3 scripts/check_weight.py   # exit 1 if any page is over the 500 KB budget

Counts what a first visit downloads from this site: <link href> (stylesheet, icon, manifest)
and <img src>. Not counted: links the reader may click (the GIFs, the CV), the video, and
off-site images (the CI badges on repos.html, which GitHub serves).
"""
import sys
from html.parser import HTMLParser

from sitelib import PUBLIC, pages

BUDGET = 500 * 1024


class Loads(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.urls = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon", "manifest", "apple-touch-icon"):
            if a.get("rel") != "apple-touch-icon":
                self.urls.append(a["href"])
        if tag == "img" and a.get("src"):
            self.urls.append(a["src"])


def main():
    over = 0
    for page in pages():
        p = Loads()
        p.feed(page.read_text(encoding="utf-8"))
        total, parts = page.stat().st_size, []
        for u in p.urls:
            if u.startswith(("http://", "https://")):
                continue
            f = (PUBLIC / u.removeprefix("/portfolio-site/")) if u.startswith("/") else (page.parent / u)
            f = f.resolve()
            if f.is_file():
                total += f.stat().st_size
                parts.append(f"{f.name} {f.stat().st_size // 1024} KB")
        over += total > BUDGET
        flag = "OVER BUDGET" if total > BUDGET else "ok"
        print(f"{page.relative_to(PUBLIC)}: {total / 1024:.1f} KB ({flag}) = html {page.stat().st_size // 1024} KB + "
              + ", ".join(parts))
    sys.exit(1 if over else 0)


if __name__ == "__main__":
    main()
