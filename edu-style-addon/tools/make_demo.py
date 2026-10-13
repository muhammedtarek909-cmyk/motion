#!/usr/bin/env python3
"""Assemble the sample scene into a HyperFrames project (edu-style-addon/demo/), ready for check + render.

demo/ is a build folder (git-ignored): the add-on's own files + the skill's shared templates and assets, so the
sample runs against the SAME rtl.css / motion-primitives.js / fonts / textures / SFX a real project gets.

Usage:  python tools/make_demo.py --skill <path to the installed reference-motion-style skill> [--out demo]
then:   npx hyperframes check edu-style-addon/demo
        npx hyperframes render edu-style-addon/demo -o edu-style-addon/preview.mp4 --quality looks
"""
import argparse, json, os, shutil

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True); ap.add_argument("--out", default=os.path.join(HERE, "demo"))
    a = ap.parse_args()
    out = os.path.abspath(a.out); os.makedirs(out, exist_ok=True)
    for sub in ("textures", "sfx"):
        dst = os.path.join(out, "assets", sub); os.makedirs(dst, exist_ok=True)
        for f in os.listdir(os.path.join(a.skill, "assets", sub)):
            shutil.copy2(os.path.join(a.skill, "assets", sub, f), os.path.join(dst, f))
    os.makedirs(os.path.join(out, "fonts"), exist_ok=True)
    for f in os.listdir(os.path.join(a.skill, "assets", "fonts")):
        shutil.copy2(os.path.join(a.skill, "assets", "fonts", f), os.path.join(out, "fonts", f))
    for f in ("rtl.css", "motion-primitives.js"):
        shutil.copy2(os.path.join(a.skill, "templates", f), os.path.join(out, f))
    for f in ("edu.css", "edu-primitives.js"):
        src = os.path.join(a.skill, "templates", f)                       # merged skill: take its copy
        shutil.copy2(src if os.path.exists(src) and not os.path.exists(os.path.join(HERE, f)) else os.path.join(HERE, f), os.path.join(out, f))
    shutil.copy2(os.path.join(HERE, "edu-scene-template.html"), os.path.join(out, "index.html"))
    json.dump({"id": "edu-demo", "name": "edu-demo"}, open(os.path.join(out, "meta.json"), "w"))
    print("demo project:", out)


if __name__ == "__main__":
    main()
