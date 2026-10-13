#!/usr/bin/env python3
"""Measure how a flat-graphics element is born: the curve of its "ink" inside a region of interest.

measure_motion.py bbox needs a clean reference frame of the same region; flat explainer graphics rarely have
one (the element replaces another).  Here the reference is the GROUND COLOUR instead: every pixel of the ROI
that differs from the ground by more than --thr counts as ink.  Per frame: ink area, bbox width / height / centre.
Each curve is trimmed to its active span and fitted to the GSAP ease families with the skill's own fitter
(scripts/measure_motion.py: describe / fit), so numbers are comparable with motion-primitives.md.

  area    line-draws, type-ons, fills, lists building up (steps = stagger)
  width / height   growing discs, bars, arrows, magnets

Usage:
  measure_growth.py VIDEO START END --roi x,y,w,h --skill SKILL_DIR [--thr 40] [--ground auto|#rrggbb] [--series]
START/END are frame numbers of the source video; ROI in full-resolution pixels.
"""
import argparse, json, os, subprocess, sys
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("start", type=int); ap.add_argument("end", type=int)
    ap.add_argument("--roi", required=True); ap.add_argument("--skill", required=True)
    ap.add_argument("--thr", type=int, default=40); ap.add_argument("--ground", default="auto")
    ap.add_argument("--series", action="store_true", help="also print the per-frame ink area (to read staggers)")
    ap.add_argument("--label", default=""); ap.add_argument("--brief", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, os.path.join(a.skill, "scripts"))
    from measure_motion import describe                                   # the skill's fitter

    st = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                             "stream=width,height,r_frame_rate", "-of", "json", a.video]))["streams"][0]
    W, H = st["width"], st["height"]; num, den = map(int, st["r_frame_rate"].split("/")); fps = num / den
    x, y, w, h = [int(v) for v in a.roi.split(",")]
    n = a.end - a.start + 1
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{a.start / fps:.4f}", "-i", a.video,
                                   "-vf", f"crop={w}:{h}:{x}:{y}", "-frames:v", str(n), "-f", "rawvideo",
                                   "-pix_fmt", "rgb24", "-"])
    fr = np.frombuffer(raw, np.uint8)[: (len(raw) // (w * h * 3)) * w * h * 3].reshape(-1, h, w, 3).astype(np.int16)
    if a.ground == "auto":                                                 # median of the ROI border, first frame
        b = fr[0]; ring = np.concatenate([b[:4].reshape(-1, 3), b[-4:].reshape(-1, 3), b[:, :4].reshape(-1, 3), b[:, -4:].reshape(-1, 3)])
        g = np.median(ring, axis=0)
    else:
        g = np.array([int(a.ground[i:i + 2], 16) for i in (1, 3, 5)], float)
    area, bw, bh, cx, cy = [], [], [], [], []
    for f in fr:
        m = np.abs(f - g).sum(-1) > a.thr
        ys, xs = np.where(m)
        area.append(float(m.sum()))
        if len(xs) < 12:
            bw.append(0.0); bh.append(0.0); cx.append(np.nan); cy.append(np.nan); continue
        x0, x1 = np.percentile(xs, [1, 99]); y0, y1 = np.percentile(ys, [1, 99])
        bw.append(float(x1 - x0)); bh.append(float(y1 - y0)); cx.append(float((x0 + x1) / 2 + x)); cy.append(float((y0 + y1) / 2 + y))
    res = {"label": a.label, "fps": fps, "window": [a.start, a.end], "roi": [x, y, w, h],
           "ground": "#%02x%02x%02x" % tuple(int(v) for v in g)}
    for key, curve in (("area", area), ("width", bw), ("height", bh)):
        c = np.array(curve, float)
        if np.ptp(c) < 1e-6:
            continue
        d = describe(c, fps, a.start, key)
        d["frames_at_30fps"] = round(d["seconds"] * 30, 1)
        d["from"] = round(float(c[max(0, d["start_frame"] - a.start)]), 1); d["to"] = round(float(c[min(len(c) - 1, d["end_frame"] - a.start)]), 1)
        res[key] = d
    if a.series:
        mx = max(area) or 1
        res["area_series_pct"] = [int(round(v / mx * 100)) for v in area]
    if a.brief:                                                            # one line per curve
        print(f"# {a.label}  f{a.start}-{a.end} @{fps:.3f} fps  ground {res['ground']}")
        for key in ("area", "width", "height"):
            if key in res:
                d = res[key]; bf = d["best_fit"]
                print(f"  {key:6} f{d['start_frame']}-{d['end_frame']}  {d['frames']} f = {d['seconds']} s = {d['frames_at_30fps']} f@30"
                      f"  {d['from']} -> {d['to']}  overshoot {d['overshoot_pct']} %  peak-v at {d['peak_velocity_at_pct']} %"
                      f"  fit {bf[0]['ease']} ({bf[0]['rmse']}), {bf[1]['ease']} ({bf[1]['rmse']})")
        if a.series:
            print("  area %: " + " ".join(str(v) for v in res["area_series_pct"]))
        return
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
