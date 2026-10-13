#!/usr/bin/env python3
"""Compact per-shot table + transition list from build_shot_map.py output (shots.json).

Usage: shot_table.py ANALYSIS_DIR [--range START_S:END_S] [--min 0.5]
"""
import argparse, json, os


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("adir"); ap.add_argument("--range"); ap.add_argument("--min", type=float, default=0.5)
    a = ap.parse_args()
    sm = json.load(open(os.path.join(a.adir, "shots.json")))
    fps = sm["stats"]["fps"]
    t0, t1 = 0.0, 1e9
    if a.range:
        s, e = a.range.split(":"); t0, t1 = float(s), float(e)
    shots = sm.get("shots", [])
    if shots:
        print("keys:", sorted(shots[0].keys()))
    print(f"{'#':>3} {'start':>8} {'dur':>6} {'begins':8} {'zoom%':>7} {'pan px':>8} {'ev':>3}  luma sat")
    for i, s in enumerate(shots):
        st = s.get("start_s", s.get("start", s.get("start_frame", 0) / fps))
        du = s.get("dur_s", s.get("duration_s", s.get("duration", 0)))
        if st < t0 or st > t1 or du < a.min:
            continue
        cam = s.get("camera", {})
        zoom = cam.get("zoom_pct", s.get("zoom_total_pct", s.get("zoom_pct", 0))); px = cam.get("pan_x_px", s.get("pan_x_px", 0)); py = cam.get("pan_y_px", s.get("pan_y_px", 0))
        ev = s.get("events", [])
        print(f"{i:>3} {st:8.2f} {du:6.2f} {str(s.get('begins_with', s.get('in', '')))[:8]:8} {zoom:7.1f} {px:5.0f},{py:<5.0f} {len(ev) if isinstance(ev, list) else ev:>3}  "
              f"{s.get('luma', s.get('luma_mean', 0)):.0f} {s.get('sat', s.get('sat_mean', 0)):.0f}")
    gr = sm.get("gradual_transitions", sm.get("gradual", []))
    if isinstance(gr, list) and gr:
        print("gradual keys:", sorted(gr[0].keys()))
        spans = [g.get("span", g.get("frames", 0)) for g in gr]
        print("gradual spans (frames):", sorted(spans))


if __name__ == "__main__":
    main()
