"""Collect candidate images per shot from Bing Images (full-size URLs)."""
import time, json, re, html, hashlib, io, sys, os, urllib.parse
from concurrent.futures import ThreadPoolExecutor
import requests
from PIL import Image

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}
ROOT = os.path.dirname(os.path.abspath(sys.argv[1]))
OUT = os.path.join(ROOT, "images")
PER_QUERY, MAX_PER_SHOT, MIN_W = 4, 8, 640
SKIP = ("ytimg.com", "236x", "lookaside", "fbsbx")

def search(q):
    """Yandex Images (Bing returns unrelated results to this IP)."""
    url = "https://yandex.com/images/search?text=" + urllib.parse.quote(q)
    t = html.unescape(requests.get(url, headers=UA, timeout=20).text)
    out, seen = [], set()
    for u in re.findall(r'"img_href":"([^"]+)"', t):
        u = u.replace("/736x/", "/originals/")
        if u in seen or any(x in u for x in SKIP): continue
        seen.add(u); out.append((u, ""))
    time.sleep(1.5)
    return out

def grab(u):
    try:
        r = requests.get(u, headers=UA, timeout=20)
        im = Image.open(io.BytesIO(r.content)); im.load()
        if im.width < MIN_W: return None
        return im.convert("RGB"), hashlib.md5(r.content).hexdigest()
    except Exception:
        return None

def do_shot(s):
    d = os.path.join(OUT, s["id"]); os.makedirs(d, exist_ok=True)
    seen, saved, log = set(), 0, []
    for qi, q in enumerate(s["img"]):
        try: res = search(q)
        except Exception as e: res = []
        got = 0
        for murl, purl in res:
            if saved >= MAX_PER_SHOT or got >= PER_QUERY: break
            g = grab(murl)
            if not g or g[1] in seen: continue
            seen.add(g[1]); im = g[0]
            if im.width > 2400: im.thumbnail((2400, 2400))
            name = f"{s['id']}_{saved+1:02d}.jpg"
            im.save(os.path.join(d, name), quality=90)
            log.append({"file": name, "query": q, "url": murl, "page": purl, "size": [im.width, im.height]})
            saved += 1; got += 1
    json.dump(log, open(os.path.join(d, "sources.json"), "w"), ensure_ascii=False, indent=1)
    print(s["id"], saved, flush=True)

shots = json.load(open(sys.argv[1]))
only = set(sys.argv[2:])
with ThreadPoolExecutor(3) as ex:
    list(ex.map(do_shot, [s for s in shots if not only or s["id"] in only]))
