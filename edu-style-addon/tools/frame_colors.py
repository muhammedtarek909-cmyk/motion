#!/usr/bin/env python3
"""Exact colours of named elements: median colour of small boxes on full-resolution frames.

Usage: frame_colors.py VIDEO SPEC.json
SPEC: [{"frame": 1618, "name": "title red", "box": [x, y, w, h]}, ...]   (full-res pixels)
For text / thin strokes the box median is the ground, so the colour reported is the median of the pixels
that differ most from the box's own border (the "ink").
"""
import json, subprocess, sys
import numpy as np


def main():
    video, spec = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8-sig"))
    st = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                             "stream=width,height,r_frame_rate", "-of", "json", video]))["streams"][0]
    W, H = st["width"], st["height"]; num, den = map(int, st["r_frame_rate"].split("/")); fps = num / den
    cache = {}
    for s in spec:
        f = s["frame"]
        if f not in cache:
            raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{f / fps:.4f}", "-i", video, "-frames:v", "1",
                                           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
            cache[f] = np.frombuffer(raw[: W * H * 3], np.uint8).reshape(H, W, 3).astype(np.int16)
        x, y, w, h = s["box"]; b = cache[f][y:y + h, x:x + w]
        ring = np.concatenate([b[:2].reshape(-1, 3), b[-2:].reshape(-1, 3), b[:, :2].reshape(-1, 3), b[:, -2:].reshape(-1, 3)])
        g = np.median(ring, axis=0)
        d = np.abs(b - g).sum(-1).ravel(); px = b.reshape(-1, 3)
        ink = px[d >= max(60, np.percentile(d, 92))] if s.get("ink", True) else px
        c = np.median(ink if len(ink) else px, axis=0)
        print(f"f{f:<5} {s['name']:28} #{int(c[0]):02x}{int(c[1]):02x}{int(c[2]):02x}   ground #{int(g[0]):02x}{int(g[1]):02x}{int(g[2]):02x}")


if __name__ == "__main__":
    main()
