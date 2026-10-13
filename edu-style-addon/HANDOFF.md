# Edu (TED-Ed-like) style add-on for `reference-motion-style`

Goal: add an educational physics/chemistry look (TED-Ed-like) to the owner's `reference-motion-style` skill as a
**per-scene mode**. A scene whose sentence explains a phenomenon, an experiment, an equation or what happens inside the
atom is built in this look. Every other scene stays in the archival style.

## Inputs
- Reference videos in `refs/` (local only; too big for git, see `.gitignore`).
- The installed `reference-motion-style` skill (synced from claude.ai). Do not edit it in place.

## Steps
1. Analyse `refs/*` with the skill's own scripts (`analyze_reference.py`, `style_fingerprint.py`, `contact_sheet.py`,
   `measure_motion.py`) so palette, easing, speeds and shot length are measured, not guessed.
2. Build the add-on in this folder:
   - `edu-style.md`: rules (palette, line/shape language, characters, molecules/force arrows, morph, line-draw,
     equation build-up, timing numbers from step 1, when a scene uses this mode).
   - `edu-primitives.js`: new primitives numbered after the last one in the skill (P30), seek-safe GSAP.
   - `edu-scene-template.html`: a sample scene, passing `npm run check`, rendered to `preview.mp4`.
   - `MERGE.md`: exact merge steps into `SKILL.md` (triggers, read-order entry), `storytelling-rules.md`
     (sentence role → edu scene), `motion-primitives.md/js`, `transitions.md` (archival ↔ edu handoff).
     Write it to work even if the skill changed since.
3. Merge into a copy of the skill and zip it for upload at claude.ai → Settings → Skills (replacing the old one).

## Status — done on 13 Oct 2026
- Step 1: the three references were analysed with the skill's scripts; `data/edu_refs_measured.json`,
  `data/edu_element_births.json`. Shapes and timings come from the magnetism film only.
- Step 2: `edu-style.md`, `edu.css`, `edu-primitives.js` (P35–P46 — the skill's list ends at P34, not P30),
  `edu-scene-template.html` → `preview.mp4`; `preview-mixed.mp4` = archival → edu → archival through the merged builder.
- Owner decision: **one colour template** — edu scenes use the archival paper, ink, red, yellow and teal; the
  reference's cream / navy / violet palette is not used.
- Step 3: `MERGE.md` + `tools/merge_into_skill.py` (15 steps, 0 manual on the skill as installed that day). The
  merged zip was handed to the owner together with a backup zip of the skill as it was before.
