"""Write the published copy of the site: public/ with every TODO block taken out.

  python3 scripts/build_site.py         # writes _site/ (what the deploy uploads)
  python3 scripts/build_site.py OUT     # writes OUT/ instead

Every element with class "todo" is removed from every page, and so is whatever that leaves
empty: a heading with nothing under it (before the next heading of the same or a higher level,
or the end of its parent), and an element that held a TODO and now holds nothing. Pages without
a TODO are copied byte for byte. The local preview serves public/ and keeps the TODOs.
"""
import argparse
import shutil
import sys
from html.parser import HTMLParser

from sitelib import ROOT

SRC = ROOT / "public"  # not sitelib.PUBLIC: SITE_ROOT may point that at the output
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}
KEEP = {"#root", "html", "head", "body", "main"}  # never pruned, even if empty
NOT_PUBLISHED = {SRC / "assets" / "video" / "src"}  # raw footage (git-ignored)


class Node:
    def __init__(self, tag, attrs, start, parent):
        self.tag, self.attrs, self.start, self.end = tag, attrs, start, None
        self.parent, self.children, self.removed = parent, [], False


class Tree(HTMLParser):
    """Element tree with source offsets. Non-blank text is kept as '#text' leaves; comments and
    whitespace are not kept (they never count as content)."""

    def __init__(self, text):
        super().__init__(convert_charrefs=False)
        self.text = text
        self.line_starts = [0] + [i + 1 for i, c in enumerate(text) if c == "\n"]
        self.root = Node("#root", {}, 0, None)
        self.stack = [self.root]
        self.feed(text)
        self.close()
        for node in self.stack[1:]:
            sys.exit(f"build_site: <{node.tag}> at offset {node.start} is never closed")
        self.root.end = len(text)

    def here(self):
        line, col = self.getpos()
        return self.line_starts[line - 1] + col

    def add(self, node):
        self.stack[-1].children.append(node)

    def handle_starttag(self, tag, attrs):
        node = Node(tag, dict(attrs), self.here(), self.stack[-1])
        self.add(node)
        if tag in VOID:
            node.end = node.start + len(self.get_starttag_text())
        else:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, dict(attrs), self.here(), self.stack[-1])
        node.end = node.start + len(self.get_starttag_text())
        self.add(node)

    def handle_endtag(self, tag):
        if tag in VOID or tag not in (n.tag for n in self.stack[1:]):
            return
        start = self.here()
        end = self.text.index(">", start) + 1
        while True:
            node = self.stack.pop()
            node.end = end if node.tag == tag else start
            if node.tag == tag:
                return

    def text_leaf(self):
        leaf = Node("#text", {}, self.here(), self.stack[-1])
        self.add(leaf)

    def handle_data(self, data):
        if data.strip():
            self.text_leaf()

    def handle_entityref(self, name):
        self.text_leaf()

    def handle_charref(self, name):
        self.text_leaf()


def walk(node):
    yield node
    for c in node.children:
        yield from walk(c)


def live(children):
    return [c for c in children if not c.removed]


def has_removed(node):
    return any(n.removed for n in walk(node) if n is not node)


def heading_level(node):
    return int(node.tag[1]) if node.tag in HEADINGS else None


def prune(root):
    """Mark the TODO elements, then whatever their removal leaves empty, until nothing changes.
    Returns the counts by reason."""
    counts = {"todo": 0, "heading": 0, "emptied": 0}
    for n in walk(root):
        if "todo" in (n.attrs.get("class") or "").split() and not any(a.removed for a in ancestors(n)):
            n.removed = True
            counts["todo"] += 1
    changed = True
    while changed:
        changed = False
        for n in walk(root):
            if n.removed or any(a.removed for a in ancestors(n)) or n.tag.startswith("#"):
                continue
            if n.tag in HEADINGS:
                after = live(n.parent.children)
                rest = after[after.index(n) + 1:]
                level = heading_level(rest[0]) if rest else 0
                if not rest or (level is not None and level <= heading_level(n)):
                    n.removed, changed = True, True
                    counts["heading"] += 1
            elif n.tag not in KEEP and n.tag not in VOID and not live(n.children) and has_removed(n):
                n.removed, changed = True, True
                counts["emptied"] += 1
    return counts


def ancestors(node):
    p = node.parent
    while p is not None:
        yield p
        p = p.parent


def cut(text, root):
    """The text with every outermost removed element cut out; a cut that leaves its line blank
    takes the whole line."""
    spans = []
    for n in walk(root):
        if n.removed and not any(a.removed for a in ancestors(n)):
            s, e = n.start, n.end
            line_start = text.rfind("\n", 0, s) + 1
            line_end = text.find("\n", e)
            line_end = len(text) if line_end < 0 else line_end
            if not text[line_start:s].strip() and not text[e:line_end].strip():
                s, e = line_start, min(line_end + 1, len(text))
            spans.append((s, e))
    out, pos = [], 0
    for s, e in sorted(spans):
        out.append(text[pos:max(s, pos)])
        pos = max(pos, e)
    out.append(text[pos:])
    return "".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("out", nargs="?", default=str(ROOT / "_site"))
    a = ap.parse_args()
    out = (ROOT / a.out).resolve()
    if out in (SRC, ROOT) or SRC in out.parents or out in ROOT.parents:
        sys.exit(f"build_site: refusing to write to {out}")
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(SRC, out, ignore=lambda d, names: [n for n in names if (SRC / d / n) in NOT_PUBLISHED])
    for page in sorted(out.rglob("*.html")):
        text = page.read_text(encoding="utf-8")
        tree = Tree(text)
        counts = prune(tree.root)
        rel = page.relative_to(out)
        if not any(counts.values()):
            print(f"{rel}: no TODO, copied unchanged")
            continue
        page.write_text(cut(text, tree.root), encoding="utf-8")
        print(f"{rel}: removed {counts['todo']} TODO block(s), {counts['heading']} heading(s) left empty, "
              f"{counts['emptied']} element(s) left empty")
    print(f"wrote {out.relative_to(ROOT) if ROOT in out.parents else out}")


if __name__ == "__main__":
    main()
