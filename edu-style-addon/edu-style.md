# Edu mode — the science-explainer look, per scene

A second way of *drawing* inside the same skill, for the moments when the script stops telling a story and
starts **explaining how something works**: flat two-tone bodies, thin field and orbit lines that draw
themselves, arrows born from the bodies, equations built one term at a time. Everything else in the video stays
archival (maps, photo cards, chapter cards). Timing still belongs to the voice: every birth is on the word that
names the thing.

**One colour template (owner, 13 Oct 2026).** The edu mode takes its *shapes and timings* from the edu
reference and its *colours and mood* from the archival style: the same halftone paper and grid, the same ink,
red, yellow and teal set, the same constant drift, the same grain. A video that mixes the two must read as one
piece. Only a drawn object that needs a colour of its own (a blue south pole, a green gas) may leave the template.

Reference for shapes and timings: one TED-Ed film about magnetism (`refs/magnets.mp4`, 23.976 fps, analysed
7–334 s). Two other TED-Ed films (maglev trains, data centres) were measured for rhythm only — illustrated
scenes by other studios, not buildable from code, not part of this look. Numbers:
`references/data/edu_refs_measured.json`, `references/data/edu_element_births.json` (the reference's own
palette is recorded there but **not used**). Frame numbers below are source frames; durations are 30 fps.

## 1 · When a scene is edu (decide per sentence)
| The sentence… | Mode |
|---|---|
| explains a **phenomenon / mechanism** (why, how: attraction, pressure, heat flow, bonding, a reaction) | **edu** |
| describes an **experiment or its set-up** (what was put where, what was measured, what happened) | **edu** |
| states or uses an **equation / law / proportion** ("doubles", "inversely", "squared") | **edu** |
| is about what happens **inside the atom / molecule / material** (particles, charges, spins, orbits, bonds) | **edu** |
| names a **person, place, date, institution, book, discovery story, consequence for society** | archival (unchanged) |
| is the owner **on camera** (eligible sentence) | on camera (unchanged) |

- Mixed sentence ("in 1785 Coulomb measured the force between two charges"): split on the word where the
  explanation starts — archival for who / when, edu from "the force…". If the two halves are under 2 s each,
  keep the whole sentence in the mode of its main clause.
- A scientist **named in passing** inside an explanation gets the archival treatment in place: a `side`-style
  photo card on the same paper with a name pill (P32 look), not a new illustrated character.
- An edu **stretch** = consecutive edu sentences. Never an edu shot shorter than 5 s; never switch modes twice
  inside one sentence.
- Not edu: timelines, lists of names, maps, "what this means for us" — even inside a science video.

## 2 · Palette = the archival tokens (`rtl.css :root`)
| Role | Token | Hex |
|---|---|---|
| light ground | `--paper` + `paper.png` + the 72 px grid | `#ececec` |
| dark ground (inside matter) | `--tc-charcoal` (as `--edu-dark`) + faint grid | `#1c1b1a` |
| "big idea" ground | paper + pale-teal bloom (`--teal-light`) | `#c3e6e7` on `#ececec` |
| text on paper / on dark | `--ink` / white, `--sticker-white` for titles | `#2f2f2f` / `#ffffff`, `#eae9e4` |
| warm body and its label (+, proton, north, hot, reactant A) | `--red` (label on paper: `--edu-red-ink`, body a shade deeper so a white symbol passes 3 : 1) | `#d1615e` (`#b94a47`, `#c9524f`) |
| cool body and its label (−, electron, south pole label, cold, reactant B) | teal set | `#339791`, `#2b4f4b`, on dark `#c3e6e7` |
| the noun in question, key word of a note, the force arrow | on paper `--edu-red-ink` / `--route-red`; on dark `--yellow-text` | `#b94a47` / `#e84c4c`; `#f3e24a` |
| lines (field, orbit, bond) | deep teal on paper, pale teal on dark | `#2b4f4b`, `#c3e6e7` |
| neutral body (neutron, unnamed atom) | paper whites | `#f4f3ee → #9a978d` |
| nucleus disc, dark bodies | `--pill-black` | `#403e3d` |
| name pill / year | the archival carriers `.pill-red`, `.pill-black`, `.year-badge` | as in the style |
| icons in list rows | one colour: deep teal on paper, pale teal on dark (the style's line-icon rule) | `#2b4f4b`, `#c3e6e7` |

Outside the template, only when the object needs it: the south end of a bar magnet `#3f78ae` (north is `--red`),
element colours of a molecule (`blue`, `green`, `gold` tones in `RMS.edu.TONES`). Keep them muted like these;
never the reference's neon violet / magenta / navy.

## 3 · Grounds
- **Paper = what we can see** (the object, the experiment, the law on the board); **dark = what we cannot**
  (inside the atom, a field at particle scale). Go dark on the word that takes us inside, back to paper on the
  word that returns to the object or the law.
- The paper ground *is* the archival paper (same texture, same grid), so an archival paper scene and an edu
  scene share a background; only the drawing changes.
- Ground changes inside an edu stretch are **hard cuts** (reference: 1 frame, f4450–4451).
- Reference stay on one ground: light runs median 12.5 s, dark 23.4 s. Don't flip faster than ~5 s.

## 4 · Shape language
- **Bodies** (particles, charges, atoms of a molecule): flat circles, two-stop diagonal gradient, halftone
  lower half, a symbol inside (`p+ e- n + − H O`; white on red / teal / dark, ink on light bodies).
  Sizes: particle Ø 114 px, featured Ø 150–225, nucleus Ø 96–150, electron on a shell Ø 38–46, big idea Ø 600+.
- **Lines**: 2–2.5 px, round caps, one colour per ground. Orbits are full circles; field lines are the *real*
  field lines of the sources (`RMS.edu.fieldPaths` integrates them), never decorative swirls.
- **Arrows**: straight, 9–13 px shaft, solid head; ink on paper / white on dark; the force the sentence is
  about: route-red on paper, yellow on dark. One arrow per quantity — when it changes, the same arrow changes length.
- **Bar magnet**: rectangle 3 : 8 (default 200 × 520 px), north red on top, pole letters white.
- **Molecules** (extension, not in the reference): the same bodies joined by 7 px lines; double bond = two
  lines 14 px apart; real bond angles.
- **Never**: 3-D, glows, drop shadows on bodies, emoji, stock icons, charts with axes (a proportion is shown by
  the bodies themselves: closer, longer arrow), cartoon characters.

## 5 · Primitives P35–P46 (`RMS.edu.*`, numbers in `RMS.edu.SPEC`)
| # | Name | Motion (30 fps) | Evidence (source frames) |
|---|---|---|---|
| P35 | EDU_GROUND | paper / dark / bloom, all from the archival tokens; change = hard cut on a word onset | f4450–4451 |
| P36 | BODY_POP | small body: scale 0 → 1, **10 f back.out(1.7)**; big disc (Ø > 300) and magnet: **32 f sine.out**, no overshoot | f1657–1683 (26 f@24, sine.out rmse .05) |
| P37 | ATOM_BUILD | halftone cloud appears (10 f), then **closes over 93 f power2.in**; at 55 % of that the nucleus swells (32 f sine.out), shells **line-draw 24 f power1.inOut, 8 f apart**, electrons pop at the end of each shell and keep turning linearly (9 s per turn, outer shells slower, alternate direction) | f1190–1264 (74 f@24, power2/3.in) |
| P38 | FIELD_LINES | every line draws from its source; inner lines lead; the family takes **4.2 s, power1.out** | f2048–2160 (4.7 s), f4540–4638 (4.1 s, power1.out rmse .11) |
| P39 | ARROW | born from the body's edge along its own axis: **9 f back.out(3)** (the only overshoot in the mode: 26–36 %); `arrowScale` for a changing quantity; `arrowsAlign`: 28 f power2.inOut, 5 f stagger | f3981–3988 (7 f@24); grid f4300–4420 (observed) |
| P40 | MORPH | outline → outline (both sampled at 72 points): **32 f sine.inOut** | same span as P36 big |
| P41 | EQUATION | LTR; one term per spoken symbol: y +18 → 0 + fade, **10 f power2.out**; fraction = bar (8 f) → top (+3 f) → bottom (+9 f); key term: red (yellow on dark) + underline drawn 18 f; result: frame closes 10 f | built from the list-row measurement |
| P42 | LABEL / LIST_ROW | label beside its body: y +12 → 0, 8 f power2.out; list row (icon + word): y +14 → 0, **10 f power2.out**, each row **on its own word** | f1559, f1593 (1 f jump + 7 f settle; rows 34 f apart) |
| P43 | EDU_TITLE | typed linear, on twos, **21 letters / s**; Arabic: a stepped clip opens the line from the right, 2 letters per step (letters stay joined) | f1462–1486 |
| P44 | MOLECULE | atoms pop (P36) on their names; bonds line-draw 12 f once both ends exist | extension |
| P45 | MOVE / OUT | body glides 28 f power2.inOut; exits = 6 f fade, or simply the next cut | — |
| P46 | EDU_DRIFT | = P14: the whole diagram scales linearly **0.83 %/s**, never still (the reference's 1.63 %/s is not used: one camera for the whole video) | style constant A2 |

Not reproduced on purpose: the reference's palette (§2), its faster camera, and its animated **letter-spacing**
(f1843–1994) — Arabic is never tracked. Its per-letter typing becomes the stepped clip (P43).

## 6 · Rhythm (edu stretches only; the rest of the video keeps the archival numbers)
| Metric | Edu reference | Other two TED-Ed films | Archival graphics |
|---|---|---|---|
| shot length median (p25 – p75) | **9.9 s** (5.8 – 23.6) | 4.8 / 9.2 s | 2.1 s |
| boundaries / min | **6.8** | 8.8 / 4.4 | 15.1 |
| share of gradual boundaries | **13.5 %** | 40 % / 67 % | 33.7 % |
| in-shot events / min (detector) | **11.2** | 13.9 / 11.4 | 21.2 |
| camera moving | 78 % | 85 % / 96 % | 87 % |

Rules that follow:
- **One edu scene per idea, 6–24 s.** The picture changes by *adding to the diagram*, not by cutting: a new
  body, line, arrow, label or term on every content word — aim for one birth every 2–4 s, never more than
  6 s without one.
- 4–9 boundaries per minute inside an edu stretch; cuts land on word onsets like everywhere else.
- ≤ 3 text elements on screen besides symbols inside bodies (title, one label pair or one note, the equation).
- A diagram that took 10 s to build is not thrown away after 2 s: hold it at least one more sentence.

## 7 · Type
The user's Arabic font everywhere (`RMS Display`), sizes in `rtl.css` (edu block): title 96 px bold ink, sub
52 px red, body labels 60 / 44 px, notes 54 px, list rows 44 px. Equations: `RMS Text`, 104–150 px, always LTR
and isolated; mini-markup `x^2`, `q_1`, `x^{-2}`. Greek letters and arrows are not in the bundled font — supply
a Latin / maths font as `plan.fonts.latin`, or spell the quantity. Symbols inside bodies are Latin (`e-`, `p+`,
`H`, `O`); pole letters may be Arabic (`poles: ["ش", "ج"]`).

## 8 · Sound
No music (owner rule). Texture sounds only, through the builder's budget: body pop → `pop`, list row / arrow /
equation term → `tick`, field lines → `scribble`, cloud → `shimmer`. The reference's sound was not analysed
(no stem separation on this machine); these follow `sound-design.md`.

## 9 · Formats
Positions are **% of the frame**, sizes are px of the 1080 short side, so a diagram keeps its scale in 9:16.
Recompose per item with `"9x16": {"x": …, "y": …}`: stack what was side by side, keep the title in the top
zone and the equation / note above the caption zone (`vertical-layout.md`).

## 10 · Plan: the `edu` scene type
```jsonc
{"id": "s21", "type": "edu", "start": 96.40, "end": 104.40, "out": "cut",
 "ground": "dark",                              // paper (default) | dark | bloom
 "items": [                                     // drawn in this order; every "t" = VO second of the word
   {"kind": "particle", "id": "plus", "x": 33, "y": 54, "d": 200, "tone": "plus", "sym": "+", "t": 96.8,
    "label": {"text": "شحنة موجبة", "tone": "warm", "dy": 172, "small": true}},
   {"kind": "particle", "id": "minus", "x": 67, "y": 54, "d": 200, "tone": "minus", "sym": "-", "t": 97.5},
   {"kind": "field", "sources": ["plus", "minus"], "n": 18, "t": 98.4},
   {"kind": "arrow", "id": "f1", "from": "plus", "angle": 0, "len": 140, "color": "#f3e24a", "t": 100.9},
   {"kind": "scale", "target": "f1", "to": 1.4, "t": 102.6},
   {"kind": "note", "text": "كلما *اقتربت* الشحنتان زادت القوة", "x": 50, "y": 86, "t": 102.5}
 ]}
```
| kind | fields |
|---|---|
| `title` | `text`, `sub`, `sub_t` |
| `label` / `note` | `text` (`*word*` = highlighted in a note), `x`,`y` or `of` (body id) + `dx`,`dy`, `tone` warm / cool / key, `small`, `out` |
| `pill` / `year` | `text`, `x`,`y`, `tone` red / black — the archival `.pill-red` / `.pill-black` / `.year-badge` |
| `particle` | `id`, `x`,`y`, `d`, `tone` (plus, minus, proton, electron, neutron, nucleus, red, teal, blue, light, dark, green, gold or `[top, mid, bottom]`), `sym`, `ring` (spin), `label` |
| `atom` | `id`, `x`,`y`, `nucleus` `{d, balls: ["proton","neutron",…]}` or `{d, tone, sym}`, `shells: [{r, electrons, ed, period, phase}]`, `cloud` false / `cloud_r`, `reveal` (the word that names the model) |
| `magnet` | `id`, `x`,`y`, `w`,`h`, `poles` |
| `field` | `sources` (body ids, a magnet id, or `{x,y,q}`), `n` lines per unit charge, `w`, `dur`, `out` |
| `arrow` | `id`, `from` (body) or `x`,`y`, `angle` (deg, 0 = right, 90 = down), `len`, `w`, `color`, `label`, `out` |
| `molecule` | `id`, `x`,`y`, `atoms: [{el, x, y, d, tone}]` (px from the centre), `bonds: [[i, j, order]]`, `atom_times` |
| `equation` | `id`, `x`,`y`, `size`, `terms: [{s, t} or {frac: [top, bottom], t}]`, `highlight: [{term, part: "num"/"den", t}]`, `box` (time) |
| `list` | `x`,`y`, `rows: [{icon: bolt / mass / magnet / spin / heat / drop / wave / dot, text, t}]` |
| `move` / `scale` / `align` / `out` | `target` (`targets` + `angle` for align), `to`, `t`, `dur` |

A field is computed once from where its sources stand: fade it (`out`) before moving a source.
Hand-authoring (anything the items cannot say): `templates/edu-scene-template.html`.

## 11 · QA
`npx hyperframes check` + snapshots as for every scene; look at one frame per birth. In `qa_score.py` the edu
share is judged against the numbers of §6 (shot length 5.8 / 9.9 / 23.6 s, slower cut band, 11 events/min) and
left out of the colour comparison, the way on-camera time is.

## 12 · Do not overfit
Take the grammar, not the film: never rebuild the reference's magnets-and-spins sequence, its titles, its
portraits or its colours. Shapes, line weights and timings are the style; the diagrams come from the script and
the palette from the archival template.
