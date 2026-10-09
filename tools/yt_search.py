"""YouTube candidates per shot via yt-dlp search (metadata only, no download)."""
import json, subprocess, sys
shots = json.load(open(sys.argv[1])); out = {}
for s in shots:
    res = []
    for q in s.get("yt", []):
        p = subprocess.run(["yt-dlp", "--flat-playlist", "-j", f"ytsearch6:{q}"], capture_output=True, text=True, timeout=120)
        for line in p.stdout.splitlines():
            d = json.loads(line)
            res.append({"query": q, "title": d.get("title"), "url": f"https://www.youtube.com/watch?v={d['id']}",
                        "channel": d.get("channel") or d.get("uploader"), "duration": d.get("duration")})
    if res:
        out[s["id"]] = res; print(s["id"], len(res), flush=True)
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
