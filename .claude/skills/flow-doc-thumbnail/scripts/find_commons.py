#!/usr/bin/env python3
"""Find reference photos on Wikimedia Commons and print verified links.

Usage:
    python3 find_commons.py "Gamal Abdel Nasser" [--limit 8] [--min-width 1000]

For each hit it prints the file page (to show the user), the direct original
file URL (to download), the size, and the license, so every link you hand the
user is real and big enough for Flow.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "flow-doc-thumbnail/1.0 (reference-image finder)"


def call(params):
    params = {**params, "format": "json", "formatversion": "2"}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(params), headers={"User-Agent": UA})
    for wait in (5, 15, 30, None):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            # Commons rate-limits shared IPs; back off and retry a few times.
            if e.code != 429 or wait is None:
                raise
            time.sleep(int(e.headers.get("Retry-After") or wait))


def strip(html):
    return re.sub(r"<[^>]+>", "", html or "").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("--limit", type=int, default=8)
    ap.add_argument("--min-width", type=int, default=1000)
    a = ap.parse_args()

    data = call({
        "action": "query",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {a.query}",
        "gsrnamespace": 6,
        "gsrlimit": a.limit * 3,
        "prop": "imageinfo",
        "iiprop": "url|size|extmetadata",
        "iiextmetadatafilter": "LicenseShortName|ImageDescription|DateTimeOriginal",
    })
    pages = sorted(data.get("query", {}).get("pages", []), key=lambda p: p.get("index", 0))
    shown = 0
    for p in pages:
        info = (p.get("imageinfo") or [{}])[0]
        w, h = info.get("width", 0), info.get("height", 0)
        if w < a.min_width and h < a.min_width:
            continue
        meta = info.get("extmetadata", {})
        print(f"- {p['title'][5:]}")
        print(f"  page: {info.get('descriptionurl')}")
        print(f"  file: {info.get('url', '').split('?')[0]}")
        print(f"  size: {w}x{h} | license: {strip(meta.get('LicenseShortName', {}).get('value'))}"
              f" | date: {strip(meta.get('DateTimeOriginal', {}).get('value'))[:20]}")
        desc = strip(meta.get("ImageDescription", {}).get("value"))
        if desc:
            print(f"  desc: {desc[:160]}")
        shown += 1
        if shown >= a.limit:
            break
    if not shown:
        print("No results at that size. Try another wording, English names, or --min-width 600.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
