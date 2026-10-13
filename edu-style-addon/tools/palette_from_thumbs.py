#!/usr/bin/env python3
"""Palette + ground statistics of a reference from analyze_reference.py output (thumbs.npy + frames.npz).

The skill's fingerprint gives luma / saturation means; this adds what the edu style needs on top:
  grounds   the dominant frame-background colours, time-weighted (the colour of the frame border ring,
            clustered) -> which grounds exist and how much screen time each gets
  accents   the most frequent saturated colours that are NOT a ground (k-means in Lab on a pixel sample)
  ground_runs  how long the film stays on one ground before switching (s)

Usage: palette_from_thumbs.py ANALYSIS_DIR OUT.json [--range START_S:END_S] [--k 10]
Requires numpy + opencv (the skill's venv).
"""
import argparse, json, os
import numpy as np
import cv2


def hexs(rgb):
    return "#%02x%02x%02x" % tuple(int(round(float(v))) for v in rgb)


def kmeans_lab(rgb, k, seed=7):
    lab = cv2.cvtColor(rgb.reshape(-1, 1, 3).astype(np.uint8), cv2.COLOR_RGB2LAB).reshape(-1, 3).astype(np.float32)
    cv2.setRNGSeed(seed)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 60, 0.2)
    _, lab_idx, cen = cv2.kmeans(lab, k, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    lab_idx = lab_idx.ravel()
    out = []
    for i in range(k):
        m = lab_idx == i
        if not m.any():
            continue
        out.append((float(m.mean()), np.median(rgb[m], axis=0)))
    out.sort(key=lambda t: -t[0])
    return out, lab_idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("adir"); ap.add_argument("out")
    ap.add_argument("--range"); ap.add_argument("--k", type=int, default=10)
    a = ap.parse_args()
    meta = json.load(open(os.path.join(a.adir, "meta.json")))
    fps = meta["fps"]
    th = np.load(os.path.join(a.adir, "thumbs.npy"), mmap_mode="r")      # [N, h, w, 3] RGB
    n = th.shape[0]
    f0, f1 = 0, n
    if a.range:
        s, e = a.range.split(":"); f0, f1 = int(float(s) * fps), min(n, int(float(e) * fps))
    idx = np.arange(f0, f1, 6)                                           # 4 samples / s at 24 fps
    fr = np.asarray(th[idx]).astype(np.uint8)
    h, w = fr.shape[1:3]

    # ---- grounds: the border ring of every sampled frame -> one colour per frame -> clusters
    b = max(2, h // 12)
    ring = np.concatenate([fr[:, :b].reshape(len(idx), -1, 3), fr[:, -b:].reshape(len(idx), -1, 3),
                           fr[:, :, :b].reshape(len(idx), -1, 3), fr[:, :, -b:].reshape(len(idx), -1, 3)], axis=1)
    g = np.median(ring, axis=1)
    gk, gidx = kmeans_lab(g, min(6, a.k))
    grounds = []
    for share, rgb in gk:
        hsv = cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_RGB2HSV)[0, 0]
        grounds.append({"hex": hexs(rgb), "share": round(share, 3), "luma": int(0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]),
                        "sat": int(hsv[1])})
    # light / dark ground split and how long the film stays on one side
    gl = 0.299 * g[:, 0] + 0.587 * g[:, 1] + 0.114 * g[:, 2]
    light = gl > 128
    runs = []; start = 0
    for i in range(1, len(light) + 1):
        if i == len(light) or light[i] != light[start]:
            runs.append((bool(light[start]), (i - start) * 6 / fps)); start = i
    runs = [r for r in runs if r[1] >= 1.0]
    ld = [r[1] for r in runs if r[0]]; dd = [r[1] for r in runs if not r[0]]

    # ---- accents: saturated pixels away from the frame's own ground
    rs = np.random.RandomState(7)
    px = fr[:, ::3, ::3].reshape(len(idx), -1, 3)
    gg = np.repeat(g[:, None, :], px.shape[1], axis=1)
    dist = np.abs(px.astype(np.int16) - gg.astype(np.int16)).sum(-1)
    px = px[dist > 60]
    hsv = cv2.cvtColor(px.reshape(-1, 1, 3), cv2.COLOR_RGB2HSV).reshape(-1, 3)
    px = px[(hsv[:, 1] > 110) & (hsv[:, 2] > 90)]
    if len(px) > 200000:
        px = px[rs.choice(len(px), 200000, replace=False)]
    ak, _ = kmeans_lab(px, a.k)
    accents = [{"hex": hexs(rgb), "share": round(share, 3)} for share, rgb in ak]

    res = {"range": a.range, "frames_sampled": int(len(idx)),
           "grounds": grounds,
           "light_ground_share": round(float(light.mean()), 3),
           "ground_run_light_s": {"n": len(ld), "median": round(float(np.median(ld)), 1) if ld else None,
                                  "max": round(max(ld), 1) if ld else None},
           "ground_run_dark_s": {"n": len(dd), "median": round(float(np.median(dd)), 1) if dd else None,
                                 "max": round(max(dd), 1) if dd else None},
           "accents": accents}
    json.dump(res, open(a.out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
