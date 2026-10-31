"""Shared helpers for the site scripts (standard library only)."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
DATA = ROOT / "data" / "repos.json"
# GitHub Pages project site; the deploy workflow publishes public/ here.
BASE_URL = "https://giridhar-shenoy.github.io/portfolio-site/"
BASE_PATH = "/portfolio-site/"
SITE_REPO = "giridhar-shenoy/portfolio-site"


def load_repos():
    return json.loads(DATA.read_text(encoding="utf-8"))


def pages():
    return sorted(PUBLIC.rglob("*.html"))


def replace_block(text, tool, name, body):
    """Replace what sits between <!-- tool:name:begin --> and <!-- tool:name:end -->."""
    pat = re.compile(rf"(<!-- {tool}:{re.escape(name)}:begin -->)(.*?)(<!-- {tool}:{re.escape(name)}:end -->)", re.S)
    if len(pat.findall(text)) != 1:
        sys.exit(f"{tool}: expected exactly one '{name}' block")
    return pat.sub(lambda m: m.group(1) + body + m.group(3), text)


def write_or_check(path, new, check):
    """Write ``new`` to ``path``; with ``check``, only report whether it is up to date."""
    old = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT)
    if old == new:
        print(f"up to date: {rel}")
        return True
    if check:
        print(f"STALE: {rel} (run the script without --check)")
        return False
    path.write_text(new, encoding="utf-8")
    print(f"wrote: {rel}")
    return True
