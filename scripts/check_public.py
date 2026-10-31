"""Check that every repo the site links to, and the site repo itself, is publicly visible.

  python3 scripts/check_public.py                  # strict: exit 1 unless all are public
  python3 scripts/check_public.py --allow-private  # local, CI and deploy: print what it found, exit 0

It asks the GitHub API without a token, i.e. as an anonymous reader would: a private repo looks
exactly like a missing one (HTTP 404).
"""
import argparse
import json
import sys
import urllib.error
import urllib.request

from sitelib import SITE_REPO, load_repos


def visibility(full_name):
    req = urllib.request.Request(f"https://api.github.com/repos/{full_name}",
                                 headers={"Accept": "application/vnd.github+json", "User-Agent": "check_public.py"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return "private" if json.load(r).get("private") else "public"
    except urllib.error.HTTPError as e:
        return "not visible anonymously (HTTP 404: private or missing)" if e.code == 404 else f"unknown (HTTP {e.code})"
    except urllib.error.URLError as e:
        return f"unknown (network: {e.reason})"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--allow-private", action="store_true")
    a = ap.parse_args()
    data = load_repos()
    names = [f"{data['owner']}/{r['name']}" for r in data["repos"]] + [SITE_REPO]
    bad = 0
    for n in names:
        v = visibility(n)
        bad += v != "public"
        print(f"{v:>10}  {n}" if v == "public" else f"{n}: {v}")
    if bad and a.allow_private:
        print(f"{bad} repo(s) not public; continuing because of --allow-private")
        return
    if bad:
        sys.exit(f"{bad} repo(s) not public")
    print("all public")


if __name__ == "__main__":
    main()
