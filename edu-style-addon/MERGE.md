# Merging the edu mode into `reference-motion-style`

The add-on is merged into a **copy** of the installed skill (never in place), then zipped for
claude.ai → Settings → Skills (replace the old `reference-motion-style`).

## One command
```bash
python edu-style-addon/tools/merge_into_skill.py --skill "<installed reference-motion-style folder>" --zip
#   -> edu-style-addon/build/reference-motion-style/      the merged copy
#   -> edu-style-addon/build/reference-motion-style.zip   upload this
```
The script finds every insertion point **by content**, so it still works if the skill changed since this was
written. A step whose anchor is gone prints `MANUAL` with what to do (the steps below, in words) and the others
go on; re-running is safe (marked blocks are replaced, one-line edits are skipped when already present).
Exit code 0 = nothing left to do by hand.

## What it does (do these by hand for any step reported `MANUAL`)

**1 · New files**
| From the add-on | Into the skill |
|---|---|
| `edu-style.md` | `references/edu-style.md` |
| `data/edu_refs_measured.json`, `data/edu_element_births.json` | `references/data/` |
| `edu-scene-template.html` (without its two `edu.css` / `edu-primitives.js` tags) | `templates/edu-scene-template.html` |
| `tools/palette_from_thumbs.py`, `measure_growth.py`, `frame_colors.py`, `compare_refs.py`, `shot_table.py` | `scripts/` |

**2 · `templates/rtl.css` and `templates/motion-primitives.js`** — the whole of `edu.css` / `edu-primitives.js`
is appended at the **end** of the file between `/* >>> EDU ADD-ON */` and `/* <<< EDU ADD-ON */`. These two files
are what `build_composition.py` already copies into every project and what `base-composition.html` already loads,
so nothing else has to learn about new files. The primitives stay numbered after the skill's last one:
**P35–P46** (the skill's own list ends at P34; if it has grown, renumber the table in `edu-style.md` §5 and the
`EDU_LOG` names in the builder block — the code itself does not depend on the numbers).

**3 · `SKILL.md`** (snippets: `merge/skill.sections.md`)
- *description* — after "…timed to his voice." add the edu sentence, and at the end of the Arabic triggers add
  `فيديو تعليمي فيزياء أو كيمياء`. claude.ai refuses descriptions over **1024 characters** and the current one is
  1023, so the script shortens four phrases of the existing text without dropping a trigger (list in the script:
  the on-camera clause, "never processes the sound", the YouTube clause, "and pills" / "and a boom" /
  "drifting camera"). Read the result once; reword freely as long as it stays ≤ 1024.
- *Read first* — after entry 2 (`storytelling-rules.md`) add entry **2b** `references/edu-style.md`.
- *Pipeline* — before step 5 add step **4b · Edu sentences** (mark each covered sentence archival / edu).
- *Non-negotiables* — one bullet: edu is per scene, one colour template, hard cuts between grounds.

**4 · Reference files** (snippets: `merge/references.sections.md`; each goes in as one marked section)
| File | Section | Where |
|---|---|---|
| `storytelling-rules.md` | "Science sentences → edu scenes" (sentence role → items → ground) | before "Asset choice per role" |
| `motion-primitives.md` | "Edu mode (P35–P46)" | end of file |
| `transitions.md` | "Archival ↔ edu handoff" (`cream` in, `tear` out, cuts inside) | end of file |
| `plan-schema.md` | "Edu scenes" (`"type": "edu"`, `ground`, `items`) | before "Overlays" |
| `style-bible.md` | "F. EDU MODE" | before "Do-not-overfit list" |

**5 · `scripts/build_composition.py`** — paste `merge/build_composition.b_edu.py` (the `EDU_LOG` table and
`b_edu`) just before `BUILDERS = {`, and add `BUILDERS["edu"] = b_edu` right after that table. `b_edu` only writes
the two mount points (`#ID-edu` in the camera, `#ID-eduhud` in the HUD), hands the plan's `items` to
`RMS.edu.scene`, sets the drift, places SFX through the existing rules and logs the primitives for QA. It needs
nothing from the rest of the builder but `c.js`, `c.hud`, `c.at`, `c.sfx`, `c.mlog`, `c.warns`, `F`.

**6 · `scripts/qa_score.py`** — six one-line edits so the edu share of a video is judged against the edu
reference (`edu-style.md` §6) instead of the archival one, exactly the way on-camera time already is: an `ed`
share next to `oc`, its own shot-length targets, a slower cut band, a lower events floor, and edu frames left out
of the colour comparison. If any of the six anchors has changed the script patches **none** and says so; then
score edu-heavy videos by hand against §6.

## After merging — check it once
```bash
python build/reference-motion-style/scripts/build_composition.py <project>/plan.json   # a plan with an "edu" scene
npx hyperframes check <project>          # 0 errors
```
`examples/edu-demo-plan.json` is such a plan (archival → `cream` → edu dark → cut → edu paper → `tear` →
archival); copy it as `plan.json` into an empty folder with `fonts/` from the skill's `assets/fonts/`.

## Working on the add-on itself
```bash
python edu-style-addon/tools/make_demo.py --skill "<installed skill>"     # -> edu-style-addon/demo/
npx hyperframes check edu-style-addon/demo
npx hyperframes render edu-style-addon/demo -o edu-style-addon/preview.mp4 --quality looks --fps 30
```
`demo/` and `build/` are git-ignored build folders.
