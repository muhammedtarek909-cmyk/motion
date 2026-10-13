<!-- Sections for the skill's reference files, separated by lines of "===== <file>". tools/merge_into_skill.py reads this file. -->
===== storytelling-rules.md
## Science sentences → edu scenes (edu mode, `edu-style.md`)
Checked **before** the role table above: a sentence that explains *how something works* is an `edu` scene, whatever
its topic. Each row is one scene (6–24 s); the items are born on their words.
| Narration role (cues) | `edu` items | Ground |
|---|---|---|
| **What a thing is made of** ("inside the atom…", "a molecule of water is…") | `atom` (cloud → model on the word that names it) or `molecule`; a `label` pair on the two named parts | dark (inside) |
| **Two things act on each other** (attract, repel, push, pull, collide) | two `particle`s on their names → `field` on "field / force between" → `arrow`s on the verb; a `key` `label` for the verb's noun | dark |
| **A quantity changes when another does** ("the closer… the stronger", "doubles", "inversely") | the same diagram: `scale` the arrow / `move` the body on the changing word + a `note` with the key word highlighted | same as the scene before |
| **An experiment and its result** ("he placed…, and saw…") | the apparatus as bodies and lines on paper; the result as an `arrow`, a `move` or a `label` on "saw / found" | cream |
| **A law, formula or definition** | `title` (the law's name) + `equation` built term by term as it is read; `highlight` on the term the next sentence talks about; `box` on the last word | paper |
| **Listed properties of one thing** (mass, charge, spin…) | the body + `list` rows, one per property, each on its own word | the body's ground |
| **A magnet / field of an object** | `magnet` (or the object as a body) + `field` from it | paper |
| **Naming the big idea** ("this is called…") | one large `particle` (d ≥ 600, tone `nucleus`) with the name as a `key` `label` in it | bloom (once per stretch) |
| **A scientist named in passing inside the explanation** | archival photo card + `pill` (+ `year`) on the same paper, beside the diagram | paper |
Not edu (use the table above): who discovered it and when, where it happened, what it led to, the owner's opinion.

===== motion-primitives.md
---
# Edu mode (P35–P46) — full table and evidence in `edu-style.md` §5
Implementation: the edu block at the end of `templates/motion-primitives.js` (`RMS.edu.*`, numbers in `RMS.edu.SPEC`);
hand-authoring contract: `templates/edu-scene-template.html`. Measured on the edu reference (23.976 fps) and converted
to 30 fps frames.

- **P35 EDU_GROUND** — the archival paper + 72 px grid / charcoal `#1c1b1a` / paper with a pale-teal bloom (one colour template for the whole video); change = hard cut.
- **P36 BODY_POP** — small body scale 0 → 1, 10 f back.out(1.7); disc Ø > 300 and magnet: 32 f sine.out (f1657–1683).
- **P37 ATOM_BUILD** — halftone cloud closes in 93 f power2.in (f1190–1264); nucleus 32 f sine.out; shells line-draw
  24 f power1.inOut, 8 f apart; electrons pop, then turn linearly (9 s per turn).
- **P38 FIELD_LINES** — real field lines of the sources, drawn from the source, inner first; 4.2 s power1.out (f2048–2160, f4540–4638).
- **P39 ARROW** — grows from the body along its axis, 9 f back.out(3), overshoot 26–36 % (f3981–3988); scale / align 28 f power2.inOut.
- **P40 MORPH** — outline → outline through 72 matched points, 32 f sine.inOut.
- **P41 EQUATION** — LTR; term y +18 → 0 + fade, 10 f power2.out, one per spoken symbol; fraction bar → top → bottom;
  key term in red (yellow on dark) + underlined (18 f); result framed (10 f).
- **P42 LABEL / LIST_ROW** — label 8 f power2.out beside its body; row (icon + word) 10 f power2.out on its own word (f1559, f1593).
- **P43 EDU_TITLE** — typed linear on twos, 21 letters / s (f1462–1486); Arabic: stepped clip from the right, never per letter.
- **P44 MOLECULE** — atoms pop on their names, bonds line-draw 12 f (extension).
- **P45 MOVE / OUT** — glide 28 f power2.inOut; exit 6 f fade or the next cut.
- **P46 EDU_DRIFT** — = P14: the diagram scales linearly 0.83 %/s (the style constant; the edu reference's 1.63 %/s is not used).

===== transitions.md
## Archival ↔ edu handoff (edu mode, `edu-style.md`)
The two looks never dissolve into each other; the handoff is one of the existing wipes, chosen by what is on each side.
These rows are checked **first**, before the decision table above.

| Boundary | Transition | Why |
|---|---|---|
| archival graphics (paper, card, map, collage) → **edu** | `cream` (P06, 17 f) | the light leak hides the change of drawing; the paper underneath is the same on both sides |
| footage / on camera → **edu** | `cut` on the first explaining word | footage sections only cut |
| **edu → edu** (new idea or paper ↔ dark) | `cut` | measured: ground changes are 1-frame cuts; 86.5 % of the edu reference's boundaries are cuts |
| **edu** → archival graphics | `tear` (P05), paper comes back over the diagram | the tear belongs to the paper side |
| **edu** → footage / on camera | `cut` | — |
| **edu** → chapter card | the chapter's `diamond` / `shard` as always | chapters are always wiped + boomed |

- No `prism`, `iris` or `dip` on an edu boundary. Never a wipe *inside* an edu stretch.
- A stretch shorter than 12 s gets `cut` on both sides (a wipe in and a wipe out 10 s apart reads as noise).
- The gradual-share target (0.23–0.40) is counted on the archival boundaries; edu ↔ edu cuts are outside it.

===== plan-schema.md
## Edu scenes (`"type": "edu"`, edu mode — `edu-style.md` §10)
```jsonc
{"id": "s21", "type": "edu", "start": 96.40, "end": 104.40, "out": "cut", "ground": "paper" | "dark" | "bloom",
 "items": [{"kind": "particle", "id": "plus", "x": 33, "y": 54, "d": 200, "tone": "plus", "sym": "+", "t": 96.8}, …]}
```
`items` are drawn in order; `x`,`y` are % of the frame, sizes px of the 1080 short side, every `t` an absolute VO
second (a word onset). Per-format override on any item: `"9x16": {"x": …, "y": …}`. `camera`: `s0`,`s1` (default
1 → 1 + 0.83 %/s). Kinds: `title` · `label` / `note` / `year` / `pill` · `particle` · `atom` · `magnet` · `field` ·
`arrow` · `molecule` · `equation` · `list` · `move` / `scale` / `align` / `out` — fields in `edu-style.md` §10.
The builder prints an `EDU WARNING` for an item timed outside its scene, more than 6 s without a new element, or an
edu scene under 5 s — fix them in the plan.

===== style-bible.md
## F. EDU MODE (owner addition — per scene, `edu-style.md`)
| # | Rule |
|---|---|
| F1 | A sentence that explains a phenomenon, an experiment, an equation or the inside of the atom is an `edu` scene; everything else keeps sections A–E |
| F2 | One colour template: the edu ground is the archival paper + grid (what we see) or the style's charcoal `#1c1b1a` (inside matter); grounds change by a hard cut |
| F3 | Type and lines use the archival tokens: ink, red (warm body), the teal set (cool body, lines, icons), yellow on dark for the key word and the force; only a drawn object that needs it leaves the palette |
| F4 | Bodies are flat two-tone circles with a halftone half; lines 2–2.5 px; field lines are the real ones; one arrow per quantity |
| F5 | One scene per idea, 6–24 s; the picture changes by adding to the diagram on each content word (≤ 6 s without a birth), not by cutting |
| F6 | The only overshoot is the arrow (9 f back.out(3)); big bodies swell 32 f sine.out; titles are typed on twos; equations build term by term, LTR |
| F7 | A1 (30 fps), A13 (births and cuts on word onsets), A15 (the user's Arabic font, RTL on text only), the no-music rule and the dwell / credit rules still hold |
