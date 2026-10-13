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
