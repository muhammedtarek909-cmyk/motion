"""Write SHOT_LIST.md for an episode: script line -> collected images -> YouTube picks."""
import json, os, sys, glob
ep = sys.argv[1]; notes = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
shots = json.load(open(f"{ep}/shots.json"))
out = [f"# قايمة اللقطات — {os.path.basename(ep)}\n",
       "كل مشهد: الجملة من الاسكريبت ← الصور اللي اتجمعت في `images/<رقم المشهد>/` (مصدر كل صورة في `sources.json` جوه نفس الفولدر).",
       "لينكات يوتيوب في `YOUTUBE_LINKS.md`. ⚠️ = مالقيتش صورة حقيقية مناسبة → نولّدها بالـ AI بالستايل.\n"]
sec = None
for s in shots:
    if s["sec"] != sec:
        sec = s["sec"]; out.append(f"\n## القسم {sec}\n\n| مشهد | الجملة | الصور | ملاحظة |\n|---|---|---|---|")
    fs = sorted(os.path.basename(f) for f in glob.glob(f"{ep}/images/{s['id']}/*.jpg"))
    note = notes.get(s["id"], "")
    if not fs: note = "⚠️ " + (note or "ولّد بالـ AI")
    out.append(f"| {s['id']} | {s['line']} | {len(fs)} صورة | {note} |")
open(f"{ep}/SHOT_LIST.md", "w").write("\n".join(out) + "\n")
