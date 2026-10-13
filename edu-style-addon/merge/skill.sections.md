<!-- Four snippets for SKILL.md, separated by lines of "=====". tools/merge_into_skill.py reads this file. -->
===== description-sentence
 Edu mode for physics/chemistry: a scene explaining a phenomenon, experiment, equation or the atom becomes a flat diagram (particles, field lines, arrows, equations).
===== description-trigger
، فيديو تعليمي فيزياء أو كيمياء، ستايل تعليمي
===== read-first
2b. `references/edu-style.md` — the edu mode (science diagrams): whenever the script explains a phenomenon, an
   experiment, an equation or what happens inside the atom / molecule. Science scripts: always.
===== pipeline
**4b · Edu sentences (`edu-style.md` §1).** Mark every covered sentence **archival** or **edu**: edu = it explains
a phenomenon / mechanism, describes an experiment, states or uses an equation, or is about the inside of the atom /
molecule / material. Everything else (people, places, dates, the story of a discovery, consequences) stays archival.
Consecutive edu sentences form a stretch; each idea in it is one `edu` scene of 6–24 s (`plan-schema.md` → Edu scenes)
whose `items` are born on the onsets of the words that name them. `PLAN.md` gets the column "mode".

===== non-negotiable
- Edu mode is per scene: phenomenon / experiment / equation / inside-the-atom sentences only. One colour template
  for the whole video: edu scenes sit on the archival paper + grid (or the style's charcoal) and use its ink, red,
  yellow and teal; real field lines, one birth per content word, grounds change by a hard cut. Enter an edu stretch with `cream`, leave it with `tear` (or `cut` to footage / camera).
