#!/usr/bin/env python3
"""Merge the edu add-on into a COPY of the reference-motion-style skill (never the installed one) and zip it.

  python tools/merge_into_skill.py --skill <installed skill dir> [--out build/reference-motion-style] [--zip]

Every step looks for its anchor by content, so it still works if the skill changed since; a step whose anchor is
gone prints MANUAL with what to do by hand (MERGE.md has the same steps in words) and the rest goes on.
Re-running is safe: marked blocks are replaced, one-line edits are skipped when already there.
"""
import argparse, os, re, shutil, sys, zipfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = "EDU ADD-ON"
report = []


def say(status, step, note=""):
    report.append((status, step, note)); print(f"  {status:7} {step}" + (f" — {note}" if note else ""))


def read(p):
    return open(p, encoding="utf-8").read()


def write(p, s):
    open(p, "w", encoding="utf-8", newline="\n").write(s)


def sections(path):
    out, key = {}, None
    for line in read(path).splitlines():
        if line.startswith("===== "):
            key = line[6:].strip(); out[key] = []
        elif key:
            out[key].append(line)
    return {k: "\n".join(v).strip("\n") for k, v in out.items()}


def block(text, body, open_c, close_c, where=None):
    """put a marked block into text: replace the old one, else insert before `where` (regex, line start), else append."""
    start, end = f"{open_c} >>> {MARK} {close_c}", f"{open_c} <<< {MARK} {close_c}"
    blk = f"{start}\n{body}\n{end}\n"
    pat = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.S)
    if pat.search(text):
        return pat.sub(lambda m: blk, text, count=1), "replaced"
    if where:
        m = re.search(where, text, re.M)
        if m:
            return text[: m.start()] + blk + "\n" + text[m.start():], "inserted"
    return text.rstrip("\n") + "\n\n" + blk, "appended"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True); ap.add_argument("--out", default=os.path.join(HERE, "build", "reference-motion-style"))
    ap.add_argument("--zip", action="store_true")
    a = ap.parse_args()
    src, out = os.path.abspath(a.skill), os.path.abspath(a.out)
    if os.path.commonpath([src, out]) == src:
        sys.exit("--out must not be inside the installed skill")
    if os.path.exists(out):
        shutil.rmtree(out)
    shutil.copytree(src, out, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store", "*.pyc"))
    print("copy of the skill:", out)
    S = sections(os.path.join(HERE, "merge", "skill.sections.md"))
    R = sections(os.path.join(HERE, "merge", "references.sections.md"))
    ref = lambda f: os.path.join(out, "references", f)

    # 1 ---- new files
    shutil.copy2(os.path.join(HERE, "edu-style.md"), ref("edu-style.md"))
    os.makedirs(ref("data"), exist_ok=True)
    for f in os.listdir(os.path.join(HERE, "data")):
        shutil.copy2(os.path.join(HERE, "data", f), os.path.join(ref("data"), f))
    for f in ("palette_from_thumbs.py", "measure_growth.py", "frame_colors.py", "compare_refs.py", "shot_table.py"):
        shutil.copy2(os.path.join(HERE, "tools", f), os.path.join(out, "scripts", f))
    tpl = read(os.path.join(HERE, "edu-scene-template.html"))
    tpl = tpl.replace('    <link rel="stylesheet" href="edu.css" />\n', "").replace('    <script src="edu-primitives.js"></script>\n', "")
    tpl = tpl.replace("To use as a project: tools/make_demo.py copies this file to demo/index.html next to rtl.css,\n  motion-primitives.js, fonts/ and assets/ from the skill, then `npx hyperframes check demo`.",
                      "To try it: copy this file as index.html into a folder with rtl.css, motion-primitives.js (templates/),\n  fonts/ (assets/fonts) and assets/{textures,sfx}, then `npx hyperframes check`.")
    write(os.path.join(out, "templates", "edu-scene-template.html"), tpl)
    say("OK", "new files", "references/edu-style.md, references/data/edu_*.json, scripts/ (5 measuring tools), templates/edu-scene-template.html")

    # 2 ---- templates: the edu blocks go to the END of the two files every project already gets
    p = os.path.join(out, "templates", "rtl.css")
    t, how = block(read(p), read(os.path.join(HERE, "edu.css")).strip("\n"), "/*", "*/"); write(p, t); say("OK", "templates/rtl.css", f"edu block {how}")
    p = os.path.join(out, "templates", "motion-primitives.js")
    t, how = block(read(p), read(os.path.join(HERE, "edu-primitives.js")).strip("\n"), "/*", "*/"); write(p, t); say("OK", "templates/motion-primitives.js", f"edu block {how}")

    # 3 ---- SKILL.md
    p = os.path.join(out, "SKILL.md"); t = read(p)
    m = re.search(r'^description:\s*"(.*)"\s*$', t, re.M)
    if not m:
        say("MANUAL", "SKILL.md description", "no one-line quoted description found: add the edu sentence + Arabic trigger by hand (≤ 1024 chars)")
    elif "Edu mode" in m.group(1):
        say("SKIP", "SKILL.md description", "already mentions the edu mode")
    else:
        d = m.group(1)
        anchor = "timed to his voice."
        d = d.replace(anchor, anchor + S["description-sentence"].rstrip(), 1) if anchor in d else d.rstrip() + S["description-sentence"].rstrip()
        d = d.rstrip(); d = (d[:-1] if d.endswith(".") else d) + S["description-trigger"].strip() + "."
        squeeze = [  # same meaning, fewer characters — applied only while the claude.ai limit (1024) is exceeded
            ("then it shows him where he says the line well looking into the lens, covers what he reads with the montage, writes key phrases in a lower corner and flies photo cards in beside him",
             "he is shown where he looks into the lens, what he reads is covered, with key phrases and photo cards beside him"),
            (" (cuts only, never processes the sound)", " (cuts only)"),
            ("lists YouTube videos to download and cuts shots from them", "lists YouTube videos to cut shots from"),
            ("vintage maps with routes and pills", "vintage maps with routes"),
            ("with wipes and a boom", "with wipes"), (", drifting camera", ""), ("، ستايل تعليمي", ""),
            (" (particles, field lines, arrows, equations)", ""),
            ("he is shown where he looks into the lens, what he reads is covered, with key phrases and photo cards beside him",
             "he is shown when he looks into the lens and covered when he reads, with key phrases and photo cards"),
            (" (cuts only)", ""),
        ]
        for long, short in squeeze:
            if len(d) <= 1024:
                break
            d = d.replace(long, short)
        if len(d) > 1024:
            say("MANUAL", "SKILL.md description", f"would be {len(d)} chars (limit 1024): shorten it by hand and add the edu sentence + trigger")
        else:
            t = t[: m.start(1)] + d + t[m.end(1):]; say("OK", "SKILL.md description", f"{len(d)} chars (limit 1024)")
    if "references/edu-style.md" in t.split("## Environment")[0]:
        say("SKIP", "SKILL.md read-first", "already listed")
    else:
        m = re.search(r"^2\. `references/storytelling-rules\.md`[^\n]*\n", t, re.M) or re.search(r"^1\. `references/style-bible\.md`[^\n]*\n", t, re.M)
        if m:
            t = t[: m.end()] + S["read-first"] + "\n" + t[m.end():]; say("OK", "SKILL.md read-first", "entry 2b added")
        else:
            say("MANUAL", "SKILL.md read-first", "add `references/edu-style.md` to the read-first list")
    if "**4b · Edu sentences" in t:
        say("SKIP", "SKILL.md pipeline", "step 4b already there")
    else:
        m = re.search(r"^\*\*5 · ", t, re.M)
        if m:
            t = t[: m.start()] + S["pipeline"] + "\n\n" + t[m.start():]; say("OK", "SKILL.md pipeline", "step 4b added before step 5")
        else:
            say("MANUAL", "SKILL.md pipeline", "add step 4b (merge/skill.sections.md) after the semantic breakdown step")
    if "Edu mode is per scene" in t:
        say("SKIP", "SKILL.md non-negotiables", "already there")
    else:
        m = re.search(r"^## Non-negotiables\n(?:.*\n)*?(?=^## |\Z)", t, re.M)
        if m:
            sec = m.group(0).rstrip("\n") + "\n" + S["non-negotiable"] + "\n\n"
            t = t[: m.start()] + sec + t[m.end():]; say("OK", "SKILL.md non-negotiables", "one bullet added")
        else:
            say("MANUAL", "SKILL.md non-negotiables", "add the edu bullet (merge/skill.sections.md)")
    write(p, t)

    # 4 ---- reference files: one marked section each
    for f, where in (("storytelling-rules.md", r"^## Asset choice per role"), ("motion-primitives.md", None), ("transitions.md", None),
                     ("plan-schema.md", r"^## Overlays"), ("style-bible.md", r"^## Do-not-overfit list")):
        p = ref(f)
        if not os.path.exists(p):
            say("MANUAL", f"references/{f}", "file not found: add the section from merge/references.sections.md where it fits"); continue
        t, how = block(read(p), R[f], "<!--", "-->", where); write(p, t); say("OK", f"references/{f}", f"edu section {how}")

    # 5 ---- builder: the `edu` scene type
    p = os.path.join(out, "scripts", "build_composition.py"); t = read(p)
    body = read(os.path.join(HERE, "merge", "build_composition.b_edu.py")).strip("\n")
    pat = re.compile(r"# >>> EDU ADD-ON.*?# <<< EDU ADD-ON\n", re.S)
    if pat.search(t):
        t = pat.sub(lambda m_: body + "\n", t, count=1); say("OK", "build_composition.py b_edu", "replaced")
    else:
        m = re.search(r"^BUILDERS = \{", t, re.M)
        if m:
            t = t[: m.start()] + body + "\n\n\n" + t[m.start():]; say("OK", "build_composition.py b_edu", "inserted before BUILDERS")
        else:
            say("MANUAL", "build_composition.py b_edu", "no `BUILDERS = {` found: paste merge/build_composition.b_edu.py next to the other b_* builders")
    if 'BUILDERS["edu"] = b_edu' in t:
        say("SKIP", "build_composition.py register", "already registered")
    else:
        m = re.search(r"^BUILDERS = \{.*?\}\n", t, re.M | re.S)
        if m:
            t = t[: m.end()] + 'BUILDERS["edu"] = b_edu          # EDU ADD-ON\n' + t[m.end():]; say("OK", "build_composition.py register", 'BUILDERS["edu"]')
        else:
            say("MANUAL", "build_composition.py register", 'add  "edu": b_edu  to the builders table')
    write(p, t)

    # 6 ---- QA: the edu share is judged against the edu reference, like on-camera time against the owner's rules
    p = os.path.join(out, "scripts", "qa_score.py")
    if os.path.exists(p):
        t = read(p)
        if "EDU ADD-ON" in t:
            say("SKIP", "qa_score.py", "already patched")
        else:
            edits = [
                ('    oc_warn = [e for e in ev if e["kind"] in ("oncam_warning", "jump_cut_warning")]\n',
                 '    oc_warn = [e for e in ev if e["kind"] in ("oncam_warning", "jump_cut_warning")]\n'
                 '    # EDU ADD-ON: the reference has no science diagrams either; the edu share `ed` is judged against the edu\n'
                 '    # reference (references/edu-style.md §6): shots 5.8 / 9.9 / 23.6 s, 4-9 boundaries/min, 11 events/min, own grounds.\n'
                 '    edu = [s for s in scenes if s["type"] == "edu"]\n'
                 '    ed = sum(s["end"] - s["start"] for s in edu) / ttime\n'),
                ('    tgt = lambda k: (1 - oc) * HOLD * mix(k) + oc * OC[k]\n',
                 '    ED = {"shot_dur_median": 9.9, "shot_dur_p25": 5.8, "shot_dur_p75": 23.6}\n'
                 '    tgt = lambda k: (1 - oc - ed) * HOLD * mix(k) + oc * OC[k] + ed * ED[k]\n'),
                ('    c_lo, c_hi = 9.5 - 4.5 * oc, 16.5 - 4.5 * oc\n', '    c_lo, c_hi = 9.5 - 4.5 * oc - 5.5 * ed, 16.5 - 4.5 * oc - 7.5 * ed\n'),
                ('    e_lo = 16 - 8 * oc ', '    e_lo = 16 - 8 * oc - 5 * ed '),
                ('    for s_ in oncam:\n        keep[', '    for s_ in oncam + edu:\n        keep['),
                ('g2 = gtime / max(1e-9, ttime * (1 - oc));', 'g2 = gtime / max(1e-9, ttime * (1 - oc - ed));'),
            ]
            missing = [old.strip()[:48] for old, _ in edits if old not in t]
            if missing:
                say("MANUAL", "qa_score.py", "anchors changed (" + " | ".join(missing) + "): score edu-heavy videos by hand against edu-style.md §6")
            else:
                for old, new in edits:
                    t = t.replace(old, new, 1)
                write(p, t); say("OK", "qa_score.py", "edu share: own shot-length / cut / event targets, left out of the colour comparison")

    # 7 ---- self-check + zip
    skill_md = read(os.path.join(out, "SKILL.md"))
    d = re.search(r'^description:\s*"(.*)"\s*$', skill_md, re.M)
    print(f"\ndescription: {len(d.group(1)) if d else '?'} chars · SKILL.md {len(skill_md.splitlines())} lines")
    manual = [r for r in report if r[0] == "MANUAL"]
    print(f"{len(report) - len(manual)} steps done, {len(manual)} need a hand" + ("" if not manual else ": " + "; ".join(r[1] for r in manual)))
    if a.zip:
        z = out.rstrip("/\\") + ".zip"
        if os.path.exists(z):
            os.remove(z)
        with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(out):
                for f in sorted(files):
                    full = os.path.join(root, f)
                    zf.write(full, os.path.join(os.path.basename(out), os.path.relpath(full, out)).replace(os.sep, "/"))
        print(f"zip: {z} ({os.path.getsize(z) / 1e6:.1f} MB)")
    return 1 if manual else 0


if __name__ == "__main__":
    sys.exit(main())
