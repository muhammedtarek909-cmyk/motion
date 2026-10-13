#!/usr/bin/env python3
"""فحص التكرار لاسكريبتات الحكواتي 2.

الاستخدام:
    python3 scripts/repetition_check.py script.md [--log hakawati-log.md] [--minutes 12]

بيفحص:
  1. العبارات الجاهزة اللي فوق سقفها (CAPS).
  2. الكلمات الشامية.
  3. العبارات المتكررة (3 و4 كلمات).
  4. 3 سطور ورا بعض بيبدأوا بنفس الكلمة.
  5. 3 فقرات ورا بعض خلصوا بسؤال.
  6. جمل طويلة متنقلة بالنص من أمثلة السكيل.
  7. التكرار مع السجل: الهيكل والافتتاحية والختام والبصمات.
  8. عدد الكلمات والمدة.

بيرجع 0 لو عدّى، و1 لو فيه مشاكل لازم تتصلح.
"""
import argparse
import re
import sys
from collections import Counter
from pathlib import Path

# ---------- التطبيع ----------
_TASHKEEL = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]")


def norm(text: str) -> str:
    text = _TASHKEEL.sub("", text)
    text = re.sub(r"[أإآٱ]", "ا", text)
    text = text.replace("ى", "ي").replace("ة", "ه")
    return text


# ---------- السقف: (الاسم، النمط، السقف) ----------
# الأنماط مكتوبة بالشكل الطبيعي وبتتطبّع قبل المطابقة.
CAPS = [
    ("استنى", r"استن[ىي]", 1),
    ("المعترض الصريح (استنى / ثانية واحدة / هتقول لي / حد هيقول)",
     r"استن[ىي]|ثانية واحدة|هتقول ?لي|حد هيقول|هتسأل(ني)?|هتسال(ني)?|بتسأل(ني)?", 2),
    ("لافتة الرجوع (هنرجع / نرجع لورا / نرجع بالزمن)",
     r"(هن|لازم ن|خلينا ن|تعالي ن|ن)رجع (لسنه|لورا|بالزمن|ل?\d|لاول|للبدايه|شويه)|هنسافر بالزمن", 1),
    ("عشان نفهم", r"عشان نفهم", 1),
    ("التلخيص الآلي (أوكي كده / كده عرفنا / فاضل إيه)",
     r"(اوكي|طيب)،? ?كده|كده (عرفنا|فهمنا|خلصنا)|فاضل ايه", 1),
    ("خلّي دي في بالك", r"خلي\w* [^\n]{0,15}في (بالك|دماغك)|افتكر الحته", 1),
    ("بس اللي محدش كان يعرفه", r"(بس|لكن) اللي (محدش|ما حدش|ما كانوش|ماكانوش|ماحدش)", 1),
    ("في فيديو النهارده", r"(في )?فيديو النهارده|النهارده هنعرف|في الفيديو ده هن", 1),
    ("لقب المخاطبة (يا صاحبي / يا عزيزي)", r"يا (صاحبي|عزيزي|صديقي)", 2),
    ("سؤال في محله / عندك حق", r"سؤال في محله|عندك حق|سؤالك (جامد|حلو|منطقي)", 1),
    ("خمّن مين", r"خمن مين", 1),
    ("سمعت صح", r"سمعت صح", 1),
    ("والأغرب / والأخطر", r"والاغرب|والاخطر|والادهي|والاسوا بقي", 2),
    ("تخيل", r"(?<!\w)تخيل(?!\w)", 1),
    ("الحقيقة إن", r"الحقيقه ان|في الحقيقه|والحقيقه", 2),
    ("ببساطة", r"ببساطه", 2),
    ("بالظبط", r"بالظبط", 3),
    ("وبالتالي", r"وبالتالي", 3),
    ("طب ليه / طب إزاي", r"طب (ليه|ازاي|ايه)", 3),
    ("ومن هنا", r"ومن هنا", 1),
    ("حط خط تحت", r"خط تحت", 1),
    ("تهويل (غيّر كل حاجة / للأبد / قلب الحسبة)",
     r"(غير|غيرت|هيغير|هتغير) كل حاجه|للابد|قلب(ت)? الحسبه", 1),
    ("وعود الصدمة (هتصدمك / مش هتصدق)", r"هتصدمك|هتتصدم|مش هتصدق|محدش كان يتخيل", 1),
]

LINE_START_CAPS = [("وهنا (أول السطر)", r"^وهنا\b", 4)]

LEVANTINE = ["يلي", "رح", "هيك", "هون", "بدي", "بدك", "بدهم", "شو", "ليش", "منيح", "لهيك",
             "زلمه", "حدا", "هاد", "هذول", "هسه", "هلق", "شوي", "قديش", "لحتى", "بلش", "نبلش"]
LEVANTINE_SOFT = ["عم"]  # ممكن تبقى "عم" بمعنى أخو الأب، فدي تحذير بس

STOP = set(norm(w) for w in
           "و في من على ده دي دول اللي ان إن أن كان كانت مش ما لا هو هي هم بس لكن عشان يعني لحد مع عن ل ب".split())

WPM = 160


def spoken_and_header(raw: str):
    """يفصل سطر البناء عن الكلام المنطوق (اللي بين أول --- وتاني ---)."""
    lines = raw.splitlines()
    seps = [i for i, l in enumerate(lines) if l.strip() == "---"]
    if len(seps) >= 2:
        header, body = lines[:seps[0]], lines[seps[0] + 1:seps[1]]
    elif len(seps) == 1:
        header, body = lines[:seps[0]], lines[seps[0] + 1:]
    else:
        header, body = [], lines
    return header, body


def sections(body):
    """يرجع قايمة فقرات، كل فقرة قايمة سطور منطوقة."""
    out, cur = [], []
    for l in body:
        s = l.strip()
        if s.startswith("#"):
            if cur:
                out.append(cur)
            cur = []
            continue
        if not s or s.startswith("[") or s.startswith(">"):
            continue
        cur.append(s)
    if cur:
        out.append(cur)
    return out


def words_of(line: str):
    line = re.sub(r"\([^)]*\)", " ", line)  # أقواس النطق ما بتتعدّش
    return re.findall(r"[\w\u0600-\u06FF]+", norm(line))


def ngrams(ws, n):
    return [" ".join(ws[i:i + n]) for i in range(len(ws) - n + 1)]


def reference_ngrams(skill_dir: Path, n=6):
    """جمل الأمثلة اللي في ملفات السكيل (جوه ``` أو ` `)."""
    grams = set()
    for p in list((skill_dir / "references").glob("*.md")) + [skill_dir / "SKILL.md"]:
        txt = p.read_text(encoding="utf-8")
        chunks = re.findall(r"```(.*?)```", txt, flags=re.S) + re.findall(r"`([^`\n]{20,})`", txt)
        for c in chunks:
            for line in c.splitlines():
                ws = words_of(line)
                grams.update(g for g in ngrams(ws, n) if not all(w in STOP for w in g.split()))
    return grams


def parse_log(path: Path):
    rows = []
    if not path or not path.exists():
        return rows
    for l in path.read_text(encoding="utf-8").splitlines():
        s = l.strip()
        if not s.startswith("|") or re.match(r"^\|[\s:\-|]+\|$", s):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if cells and cells[0] in ("التاريخ", "date"):
            continue
        if len(cells) >= 9:
            rows.append({"date": cells[0], "title": cells[1], "angle": cells[2], "arch": cells[3],
                         "opening": cells[4], "ending": cells[5], "tone": cells[6],
                         "tools": cells[7], "marks": cells[8]})
    return rows


def header_field(header_text: str, key: str):
    m = re.search(key + r"\s*:\s*\[?([^·\]\n]+)", header_text)
    return m.group(1).strip() if m else None


def same_kind(a: str, b: str) -> bool:
    """مقارنة النوع: بالكود (أ، ب، ط… أو رقم) لو الاتنين فيهم كود، وإلا بأول كلمتين."""
    code = re.compile(r"^\(?([\u0621-\u064A0-9\u0660-\u0669]{1,2})[\.\)]\s*")
    a, b = norm(a or "").strip(), norm(b or "").strip()
    if not a or not b:
        return False
    ka, kb = code.match(a), code.match(b)
    if ka and kb:
        return ka.group(1) == kb.group(1)
    a, b = code.sub("", a), code.sub("", b)
    return a.split()[:2] == b.split()[:2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("--log", default=None)
    ap.add_argument("--minutes", type=float, default=None)
    args = ap.parse_args()

    raw = Path(args.script).read_text(encoding="utf-8")
    header, body = spoken_and_header(raw)
    secs = sections(body)
    lines = [l for s in secs for l in s]
    text_n = norm("\n".join(re.sub(r"\([^)]*\)", " ", l) for l in lines))

    errors, warns = [], []

    # 1. السقف
    for name, pat, cap in CAPS:
        n = len(re.findall(norm(pat), text_n))
        if n > cap:
            errors.append(f"«{name}»: {n} مرات، والسقف {cap}.")
    for name, pat, cap in LINE_START_CAPS:
        n = sum(1 for l in lines if re.search(norm(pat), norm(l)))
        if n > cap:
            errors.append(f"«{name}»: {n} مرات، والسقف {cap}.")

    # 2. الشامي
    all_words = [w for l in lines for w in words_of(l)]
    wc = Counter(all_words)
    lev = [f"{w} ({wc[norm(w)]})" for w in LEVANTINE if wc[norm(w)]]
    if lev:
        errors.append("كلمات شامية: " + "، ".join(lev))
    soft = [w for w in LEVANTINE_SOFT if wc[w]]
    if soft:
        warns.append("اتأكد إن «عم» مش «عم بيعمل» الشامية: " + str(wc["عم"]) + " مرات.")

    # 3. عبارات متكررة
    rep = []
    for n, limit in ((4, 3), (3, 4)):
        c = Counter(g for l in lines for g in ngrams(words_of(l), n)
                    if sum(w not in STOP for w in g.split()) >= 2)
        rep += [f"«{g}» ×{k}" for g, k in c.most_common() if k >= limit]
    if rep:
        errors.append("عبارات متكررة: " + "، ".join(rep[:12]))

    # 4. بدايات السطور
    starts = [(words_of(l) or [""])[0] for l in lines]
    runs = set()
    for i in range(len(starts) - 2):
        w = starts[i]
        if w and not w.isdigit() and starts[i + 1] == w and starts[i + 2] == w:
            runs.add(w)
    if runs:
        errors.append("3 سطور ورا بعض بيبدأوا بنفس الكلمة: " + "، ".join(f"«{w}»" for w in runs)
                      + " (لو ده تكرار مقصود مرة في الفيديو، تجاهل التحذير)")
    top = Counter(w for w in starts if w).most_common(3)
    if lines and top and top[0][1] / len(lines) > 0.18:
        warns.append(f"«{top[0][0]}» بتبدأ {top[0][1]} سطر من {len(lines)}. نوّع بدايات السطور.")

    # 5. نهايات الفقرات
    endings = [s[-1].rstrip().endswith(("؟", "?")) for s in secs]
    for i in range(len(endings) - 2):
        if endings[i] and endings[i + 1] and endings[i + 2]:
            errors.append(f"3 فقرات ورا بعض خلصوا بسؤال (من الفقرة {i + 1}). خلّي واحدة تخلص بصورة أو بجملة قاطعة.")
            break

    # 6. النقل من أمثلة السكيل
    skill_dir = Path(__file__).resolve().parent.parent
    refs = reference_ngrams(skill_dir)
    copied = sorted({g for l in lines for g in ngrams(words_of(l), 6) if g in refs})
    if copied:
        errors.append("جمل متنقلة من أمثلة السكيل: " + "، ".join(f"«{g}»" for g in copied[:6]))

    # 7. السجل
    log_rows = parse_log(Path(args.log)) if args.log else []
    if log_rows:
        htext = "\n".join(header)
        arch = header_field(htext, "الهيكل")
        opening = header_field(htext, "الافتتاحية")
        ending = header_field(htext, "الختام")
        if arch and any(same_kind(arch, r["arch"]) for r in log_rows[-2:]):
            errors.append(f"الهيكل «{arch}» اتعمل في آخر اسكريبتين. اختار هيكل تاني.")
        if opening and any(same_kind(opening, r["opening"]) for r in log_rows[-3:]):
            errors.append(f"الافتتاحية «{opening}» اتعملت في آخر 3 اسكريبتات.")
        if ending and any(same_kind(ending, r["ending"]) for r in log_rows[-3:]):
            errors.append(f"الختام «{ending}» اتعمل في آخر 3 اسكريبتات.")
        if not (arch and opening and ending):
            warns.append("سطر **البناء** ناقص (الهيكل / الافتتاحية / الختام)، فمقارنة السجل اتعملت جزئيًا.")
        marks = []
        for r in log_rows[-5:]:
            marks += [m.strip() for m in re.findall(r"«([^»]{4,})»", r["marks"])]
        reused = [f"«{m}»" for m in marks if norm(m) in text_n]
        if reused:
            errors.append("بصمات من اسكريبتات قبل كده اتعادت: " + "، ".join(reused[:6]))
    elif args.log:
        warns.append("السجل فاضي أو مش موجود. ده أول اسكريبت هيتسجل.")

    # 8. المدة
    total = len(all_words)
    mins = total / WPM
    if args.minutes:
        lo, hi = args.minutes * WPM * 0.9, args.minutes * WPM * 1.1
        if not lo <= total <= hi:
            errors.append(f"عدد الكلمات {total} برّه المدى ({int(lo)}–{int(hi)}) لـ {args.minutes:g} دقيقة.")

    print(f"عدد الكلمات المنطوقة: {total} ≈ {mins:.1f} دقيقة · الفقرات: {len(secs)} · السطور: {len(lines)}")
    for w in warns:
        print("⚠️ " + w)
    for e in errors:
        print("❌ " + e)
    if errors:
        print(f"\nالنتيجة: {len(errors)} مشكلة لازم تتصلح قبل التسليم.")
        return 1
    print("\nالنتيجة: عدّى ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
