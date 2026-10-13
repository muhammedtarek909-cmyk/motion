#!/usr/bin/env python3
"""Side-by-side table of several fingerprints (style_fingerprint.py) + palettes (palette_from_thumbs.py).

Usage: compare_refs.py ANALYSIS_DIR name1 name2 ... [--archival SKILL/references/fingerprint.json] [--out merged.json]
Reads ANALYSIS_DIR/<name>.content.json, <name>.palette.json and <name>/shots.json.
"""
import argparse, json, os

KEYS = ["duration_s", "shots", "shot_dur_median", "shot_dur_mean", "shot_dur_p10", "shot_dur_p25", "shot_dur_p75",
        "shot_dur_p90", "cuts_per_min", "gradual_ratio", "events_per_min", "max_static_s_p90", "camera_moving_ratio",
        "zoom_rate_pct_s_med", "pan_rate_px_s_med", "luma_mean", "luma_light_share", "luma_dark_share", "sat_mean",
        "sharp_med"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("adir"); ap.add_argument("names", nargs="+")
    ap.add_argument("--archival"); ap.add_argument("--out")
    a = ap.parse_args()
    fp = {n: json.load(open(os.path.join(a.adir, f"{n}.content.json"))) for n in a.names}
    cols = dict(fp)
    if a.archival:
        cols["archival"] = json.load(open(a.archival))["halves"]["graphics"]
    print(f"{'metric':24}" + "".join(f"{n:>13}" for n in cols))
    for k in KEYS:
        print(f"{k:24}" + "".join(f"{cols[n].get(k)!s:>13}" for n in cols))
    merged = {"fingerprints": fp, "palettes": {}, "shots": {}}
    for n in a.names:
        p = json.load(open(os.path.join(a.adir, f"{n}.palette.json")))
        s = json.load(open(os.path.join(a.adir, n, "shots.json")))
        merged["palettes"][n] = p; merged["shots"][n] = s["stats"]
        print(f"\n== {n}: light-ground share {p['light_ground_share']} | light runs {p['ground_run_light_s']} | dark runs {p['ground_run_dark_s']}")
        print("  grounds: " + "  ".join(f"{g['hex']} {g['share']:.2f} L{g['luma']} S{g['sat']}" for g in p["grounds"]))
        print("  accents: " + "  ".join(f"{g['hex']} {g['share']:.2f}" for g in p["accents"]))
        print("  shots:   " + json.dumps(s["stats"]))
    if a.out:
        json.dump(merged, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
