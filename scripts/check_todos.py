"""List every element with class "todo" on every page.

  python3 scripts/check_todos.py            # list them; exit 0
  python3 scripts/check_todos.py --strict   # list them; exit 1 if there are any (CI and the
                                            # deploy run it on the published copy, which
                                            # must have none: SITE_ROOT=_site)
"""
import argparse
import re
import sys
from html.parser import HTMLParser

from sitelib import PUBLIC, pages

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Todos(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0        # element depth
        self.open = []        # [depth, line, text parts] for each todo element still open
        self.found = []       # (line, text)

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.depth += 1
        if "todo" in (dict(attrs).get("class") or "").split():
            self.open.append([self.depth, self.getpos()[0], []])

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.open and self.open[-1][0] == self.depth:
            _, line, parts = self.open.pop()
            text = re.sub(r"\s+", " ", "".join(parts)).strip()
            self.found.append((line, text))
            if self.open:
                self.open[-1][2].append(text)
        self.depth -= 1

    def handle_data(self, data):
        if self.open:
            self.open[-1][2].append(data)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    total = 0
    for page in pages():
        p = Todos()
        p.feed(page.read_text(encoding="utf-8"))
        for line, text in sorted(p.found):
            print(f"{page.relative_to(PUBLIC)}:{line}: TODO {text}")
            total += 1
    print(f"{total} TODO block(s)")
    sys.exit(1 if (a.strict and total) else 0)


if __name__ == "__main__":
    main()
