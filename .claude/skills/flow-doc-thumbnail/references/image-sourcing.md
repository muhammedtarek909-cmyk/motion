# Image sourcing: what the user uploads to Flow, and real links to it

Nano Banana 2 invents faces, buildings, artifacts and maps when it has nothing to copy. For this style that kills the thumbnail: a "Nasser" that isn't Nasser, a wrong Air Force One, a fantasy map. So for every concept, decide which **ingredients** (attached reference images) Flow needs, find each one, verify it, and hand the user working links.

## 1. Decide what is needed
Attach an image only when the thing must be **recognizable or exact**. Max 4 images; put them in this order, because the prompt refers to them by number:

| Order | Ingredient | Needed when | What a good one looks like |
|---|---|---|---|
| 1 | **Real person's face** | a known person is the hero (P1, P9, P10, P12) | face ≥ 400 px tall, eyes open and visible, front or slight three-quarter, neutral or serious expression (or the expression you want), even light, no text or watermark over the face. For P1 frontal and looking at the lens. A clean color or colorized photo beats a grainy group shot. |
| 2 | **Real object, building, artifact, vehicle** | the hero must be the true one (a specific aircraft, the Mona Lisa, a medal, a banknote, a monument, a ship) | clear side or three-quarter view of the whole thing, plain background if possible; flat scans for banknotes, medals, documents and stamps |
| 3 | **Map / geography** | P11, or a miniature of a real place | a relief or satellite image of the exact area (NASA Earth Observatory, Wikimedia relief maps), north up |
| 4 | **Style reference** | the concept follows one of the user's pack thumbnails closely | the matching file from the user's `Downloads` pack, with its text and logo cropped or painted out first |

The host's own photo is NOT part of this style by default. If the user wants to appear in it, follow the host rules of `flow-thumbnail-prompts` (the host's round tortoiseshell glasses always on) and put the host photo as image 1.

Nothing to attach is a valid answer: objects that only need to be "a pill", "a microphone", "a whiskey glass" are generated from the prompt alone.

## 2. Find and verify each link
Never write a URL you have not seen in a search result or fetched yourself. Prefer **Wikimedia Commons** (public domain / CC, big originals, stable URLs).

**A. If you can run code with internet**, use the bundled finder (it retries when Commons rate-limits):
```
python3 scripts/find_commons.py "Gamal Abdel Nasser" --limit 8
python3 scripts/find_commons.py "Suez Canal aerial" --min-width 1500
```
Search in English, with a year or context word when the name is common. It prints the file page, the direct file URL, size, license and the description.

**B. Otherwise** use web search with `site:commons.wikimedia.org <name> <year>` (or `site:commons.wikimedia.org File: <name>`), then fetch the file page and check the description, the resolution and the license.

**C. Check it is the right image.** Read the description; if you can download a small preview (`https://commons.wikimedia.org/wiki/Special:FilePath/<File_name.jpg>?width=500`), look at it. The best-sounding title is often the wrong photo: `File:Gamal_Abdel_Nasser_1955.jpg` is a smiling dinner photo, while `File:Nasser_1961.jpg` is the frontal serious portrait a P1 thumbnail needs. Watch the classic mix-ups (Lord Cromer vs Lord Kitchener, Khedive Ismail vs Khedive Tewfik, King Fuad vs King Farouk) and name the person in the photo's own description.

**D. If nothing verifiable turns up**, don't invent a link. Give a ready search link instead, plus exactly what to pick:
- `https://commons.wikimedia.org/w/index.php?search=<words>&title=Special:MediaSearch&type=image`
- `https://www.google.com/search?tbm=isch&tbs=isz:l&q=<words>` (large images)
- For film/TV stills: the scene and the timestamp to screenshot.

## 3. How to present each ingredient to the user
For each image, one block in Egyptian Arabic:
```
Image 1: جمال عبد الناصر، صورة 1961 (بصّة للكاميرا، جدّي)
- الصفحة: https://commons.wikimedia.org/wiki/File:Nasser_1961.jpg
- التحميل المباشر: https://upload.wikimedia.org/wikipedia/commons/4/43/Nasser_1961.jpg
- ليه دي: وشّه من قدّام وعينه باينة، ودا اللي Flow محتاجه عشان يطلّع الوش الكبير ورا المجسم.
- قبل الرفع: قصّها على الوش والكتاف بس.
```
Then the style reference, if any: `Image 2 (اختياري): من ملف الثمبنيلز بتاعك «maxresdefault (27).jpg» — امسح العلم والكلام منها الأول`.

Close the list with: attach the images in this order before pasting the prompt, and choose 16:9 (Landscape).

## 4. Using a pack thumbnail as a style reference
It locks lighting, grade and composition better than words. Rules:
- Crop or paint out its text, logos, flags and watermark first (Flow copies them otherwise).
- In the prompt write: `Use image N only as a reference for lighting, color grade, camera angle and composition. Do not copy its subject, people, text, logo or flag.`
- Only one style reference per prompt.
- Skip it when the subject is a real person and the reference also has a person: Flow may blend the faces. Describe the look in words instead.

## 5. Rights, in one line when relevant
Commons public-domain and CC images are safe to use as references. Faces of living private people, and other channels' thumbnails, are references only: never reproduce them as the final image.
