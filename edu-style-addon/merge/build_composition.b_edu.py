# >>> EDU ADD-ON (edu-style-addon/MERGE.md) — builder for the `edu` scene type
EDU_LOG = {   # item kind -> (motion-log primitive, SFX rule of the existing table or None, frames)
    "title": ("P43_edu_title", None, 30), "particle": ("P36_body_pop", "node", 10), "magnet": ("P36_body_pop", "node", 32),
    "atom": ("P37_atom_build", "glass_in", 93), "field": ("P38_field_lines", "mark", 126), "arrow": ("P39_arrow", "pill", 9),
    "align": ("P39_arrows_align", None, 28), "scale": ("P39_arrow_scale", None, 28), "equation": ("P41_equation", "pill", 10),
    "list": ("P42_list_row", "pill", 10), "label": ("P42_label", None, 8), "note": ("P42_label", None, 8),
    "year": ("P42_label", "year", 8), "pill": ("P42_label", "pill", 8), "molecule": ("P44_molecule", "node", 10),
    "move": ("P45_move", None, 28), "out": ("P45_out", None, 6),
}


def b_edu(c, sid, sc):
    """EDU MODE (references/edu-style.md): a science diagram on the style's paper / charcoal / bloom ground. The plan's `items`
    go to RMS.edu.scene untouched (it builds the SVG at load time); here: the mount points, per-format overrides,
    the excerpt time shift for nested times, the camera, SFX and the motion log."""
    shift = sc.get("_shift", 0.0)
    items = []
    for it in sc.get("items", []) or []:
        it = json.loads(json.dumps(it))                       # deep copy: the plan is never edited
        if c.fmt in it:
            it.update(it.pop(c.fmt))
        it.pop("9x16", None); it.pop("16x9", None)
        if shift:                                             # top-level t / out were shifted by build(); nested times here
            for k in ("reveal", "box", "sub_t"):
                if it.get(k) is not None:
                    it[k] += shift
            if "atom_times" in it:
                it["atom_times"] = [x + shift for x in it["atom_times"]]
            for coll in ("terms", "rows", "highlight"):
                for sub in it.get(coll, []) or []:
                    if isinstance(sub, dict) and sub.get("t") is not None:
                        sub["t"] += shift
            if isinstance(it.get("label"), dict) and it["label"].get("t") is not None:
                it["label"]["t"] += shift
        items.append(it)
    spec = {"ground": sc.get("ground", "paper"), "start": round(sc["start"], 3), "end": round(sc["_end_vis"], 3), "items": items}
    c.hud.setdefault(sid, []).append(f'<div id="{sid}-eduhud"></div>')
    c.js.append(f'RMS.edu.scene(tl, "{sid}", {json.dumps(spec, ensure_ascii=False).replace("</", "<" + chr(92) + "/")});')
    dur = sc["_end_vis"] - sc["_start_vis"]
    cam = sc.get("camera") or {}
    s0 = cam.get("s0", 1.0); s1 = cam.get("s1", s0 + 0.0083 * dur)                  # P46 = P14: the style's 0.83 %/s linear drift
    c.js.append(f'RMS.drift(tl, "#{sid}-cam", {c.at(sc["_start_vis"])}, {dur:.3f}, {{s0: {s0}, s1: {s1:.4f}, '
                f'x0: {cam.get("x0", 0)}, x1: {cam.get("x1", 0)}, y0: {cam.get("y0", 0)}, y1: {cam.get("y1", 0)}}});')
    c.mlog("P46_edu_drift", sc["_start_vis"], dur, sid)
    last = None
    for it in items:
        prim, rule, fr = EDU_LOG.get(it.get("kind"), (None, None, 0))
        if not prim:
            c.warns.append(f'EDU WARNING {sid}: unknown item kind "{it.get("kind")}"'); continue
        t = it.get("t", sc["start"])
        if not (sc["start"] - 1e-6 <= t <= sc["end"] + 1e-6):
            c.warns.append(f'EDU WARNING {sid}: item {it.get("id", it.get("kind"))} is timed at {t:.2f}s, outside the scene')
        c.mlog(prim, t, F(fr), sid)
        if rule:
            c.sfx(rule, t, sid)
        if it.get("kind") not in ("move", "scale", "align", "out"):
            if last is not None and t - last > 6.0:
                c.warns.append(f"EDU WARNING {sid}: {t - last:.1f}s without a new element before {t:.2f}s (edu-style.md §6: at most 6 s)")
            last = t if last is None else max(last, t)
    if dur < 5.0:
        c.warns.append(f"EDU WARNING {sid}: edu scene of {dur:.1f}s (edu-style.md §1: at least 5 s)")
    return f'<div id="{sid}-edu"></div>', ""


# <<< EDU ADD-ON
