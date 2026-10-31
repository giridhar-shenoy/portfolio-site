"""Build the repo cards on the Home page and the table on repos.html from data/repos.json.

  python3 scripts/build_repos.py                   # rewrite the generated blocks
  python3 scripts/build_repos.py --check           # exit 1 if a generated block is stale (CI)
  python3 scripts/build_repos.py --refresh-heroes  # local only: copy each hero GIF from its local
                                                   # clone, record the clone's HEAD commit, and
                                                   # make the still the card shows
"""
import argparse
import json
import shutil
import subprocess
import sys
from html import escape
from pathlib import Path

from sitelib import DATA, PUBLIC, ROOT, load_repos, replace_block, write_or_check


def refresh_heroes(data):
    from PIL import Image  # local-only dependency, not needed for a normal build

    for r in data["repos"]:
        h = r["hero"]
        clone = Path(h["local_clone"]).expanduser()
        src = clone / h["source_path"]
        h["source_commit"] = subprocess.run(["git", "-C", str(clone), "rev-parse", "HEAD"], check=True,
                                            capture_output=True, text=True).stdout.strip()
        dst = PUBLIC / h["gif"]
        shutil.copyfile(src, dst)
        subprocess.run([str(ROOT / "scripts" / "optimize_media.sh"), str(dst)], check=True)
        with Image.open(PUBLIC / h["still"]) as im:
            h["still_width"], h["still_height"] = im.size
        print(f"{r['name']}: {src} @ {h['source_commit'][:7]} -> {h['gif']}, still {im.size}")
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cards(data):
    out = ['\n<ul class="cards">']
    for i, r in enumerate(data["repos"]):
        h = r["hero"]
        lazy = "" if i == 0 else ' loading="lazy"'
        out.append(f"""<li class="card">
<img src="{h['still']}" width="{h['still_width']}" height="{h['still_height']}" alt="{escape(h['alt'])}"{lazy} decoding="async">
<div class="body">
<h3><a href="{r['url']}">{escape(r['name'])}</a></h3>
<p>{escape(r['one_line'])}</p>
<p class="more"><a href="{h['gif']}">Animated GIF</a></p>
</div>
</li>""")
    out.append("</ul>\n")
    return "\n".join(out)


def table(data):
    rows = []
    for r in data["repos"]:
        ci = f"{r['url']}/actions/workflows/ci.yml"
        rows.append(f"""<tr>
<td><a href="{r['url']}">{escape(r['name'])}</a></td>
<td>{escape(r['one_line'])}</td>
<td>{escape(r['stack'])}</td>
<td><a href="{ci}"><img src="{ci}/badge.svg?branch=main" alt="CI status of {escape(r['name'])}" height="20" class="badge"></a></td>
</tr>""")
    return f"""
<div class="table-scroll">
<table>
<thead>
<tr><th scope="col">Repo</th><th scope="col">What it is</th><th scope="col">Stack</th><th scope="col">CI</th></tr>
</thead>
<tbody>
{chr(10).join(rows)}
</tbody>
</table>
</div>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--refresh-heroes", action="store_true")
    a = ap.parse_args()
    data = load_repos()
    if a.refresh_heroes:
        refresh_heroes(data)
    missing = [r["name"] for r in data["repos"] if not r["hero"]["source_commit"] or not r["hero"]["still_width"]]
    if missing:
        sys.exit(f"build_repos: no hero commit/still recorded for {missing}; run --refresh-heroes locally")
    ok = True
    for page, name, body in (("index.html", "cards", cards(data)), ("repos.html", "table", table(data))):
        path = PUBLIC / page
        ok &= write_or_check(path, replace_block(path.read_text(encoding="utf-8"), "build_repos", name, body), a.check)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
