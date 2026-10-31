"""Check every link on every page: internal files and #anchors, and external URLs (HEAD, then GET).

  python3 scripts/check_links.py                 # local and CI: private-repo 404s are expected
  python3 scripts/check_links.py --strict        # a private-repo 404 is a failure too
  python3 scripts/check_links.py --no-external   # offline: internal links and anchors only

While the repos are private, their GitHub URLs (and CI badges) return 404 to an anonymous
reader; those are listed as "expected until Sunday" and do not fail the check. LinkedIn answers
automated requests with HTTP 999; that is listed as a warning.
"""
import argparse
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import PurePosixPath
from urllib.parse import unquote, urldefrag

from sitelib import BASE_PATH, BASE_URL, PUBLIC, SITE_REPO, load_repos, pages

URL_ATTRS = {("a", "href"), ("link", "href"), ("img", "src"), ("source", "src"), ("track", "src"),
             ("video", "poster"), ("script", "src"), ("iframe", "src")}
META_URLS = {"og:url", "og:image"}


class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.urls = set(), []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        for t, attr in URL_ATTRS:
            if tag == t and a.get(attr):
                self.urls.append((self.getpos()[0], a[attr]))
        if tag == "meta" and a.get("property") in META_URLS and a.get("content"):
            self.urls.append((self.getpos()[0], a["content"]))


def parse(page):
    p = Links()
    p.feed(page.read_text(encoding="utf-8"))
    return p


def resolve(page, url):
    """Map an internal URL to (file under public/, fragment), or None if it is external."""
    url, frag = urldefrag(url)
    if url.startswith(BASE_URL):
        rel = PurePosixPath(url[len(BASE_URL):])
    elif url.startswith(BASE_PATH):
        rel = PurePosixPath(url[len(BASE_PATH):])
    elif url.startswith(("http://", "https://", "mailto:", "//")):
        return None
    elif url == "":
        return page, frag
    else:
        rel = PurePosixPath(page.parent.relative_to(PUBLIC).as_posix()) / unquote(url)
    target = (PUBLIC / rel).resolve()
    if url.endswith("/") or url in ("", ".", "./", "../") or target.is_dir():
        target = target / "index.html"
    return target, frag


def fetch(url):
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(url, method=method, headers={"User-Agent": "Mozilla/5.0 (check_links.py)"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue
            return e.code
        except (urllib.error.URLError, TimeoutError) as e:
            return f"error: {getattr(e, 'reason', e)}"
    return "error: no response"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--no-external", action="store_true")
    a = ap.parse_args()
    data = load_repos()
    private_prefixes = tuple(f"https://github.com/{data['owner']}/{r['name']}" for r in data["repos"]) + (
        f"https://github.com/{SITE_REPO}",)

    parsed = {page.resolve(): parse(page) for page in pages()}
    broken, external, skipped = [], {}, set()
    n_internal = 0
    for page, p in parsed.items():
        where = page.relative_to(PUBLIC)
        for line, url in p.urls:
            r = resolve(page, url)
            if r is None:
                if url.startswith("mailto:"):
                    skipped.add(url)
                else:
                    external.setdefault(url, []).append(f"{where}:{line}")
                continue
            n_internal += 1
            target, frag = r
            if not target.is_file():
                broken.append(f"{where}:{line}: {url} -> missing file {target.relative_to(PUBLIC.resolve())}")
            elif frag and target.suffix == ".html":
                ids = parsed[target].ids if target in parsed else parse(target).ids
                if frag not in ids:
                    broken.append(f"{where}:{line}: {url} -> no id '{frag}' in {target.relative_to(PUBLIC.resolve())}")

    print(f"internal: {n_internal} links and anchors checked, {len(broken)} broken")
    for b in broken:
        print(f"  BROKEN {b}")
    print(f"not checked: {', '.join(sorted(skipped)) or 'none'}")

    failed, expected, warned, ok = [], [], [], []
    if a.no_external:
        print(f"external: {len(external)} URLs not checked (--no-external)")
    else:
        for url in sorted(external):
            status = fetch(url)
            row = f"{status}  {url}  ({', '.join(sorted(set(external[url])))})"
            if isinstance(status, int) and status < 400:
                ok.append(row)
            elif status == 404 and url.startswith(private_prefixes) and not a.strict:
                expected.append(row)
            elif status == 999:
                warned.append(row)
            else:
                failed.append(row)
        print(f"external: {len(external)} URLs: {len(ok)} ok, {len(expected)} expected 404 until Sunday "
              f"(private repos), {len(warned)} warnings, {len(failed)} failed")
        for title, rows in (("ok", ok), ("expected until Sunday (repo still private)", expected),
                            ("warning (host blocks automated requests)", warned), ("FAILED", failed)):
            for row in rows:
                print(f"  {title}: {row}")
    sys.exit(1 if (broken or failed) else 0)


if __name__ == "__main__":
    main()
