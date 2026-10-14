---
name: flow-doc-thumbnail
description: "Writes ready-to-paste Nano Banana 2 prompts for Google Flow that make a cinematic documentary-style YouTube thumbnail, in the look of the big geopolitics / money / crime / science channels the user collected: one hero with one twist (a giant face over a miniature, a cutaway, a loaded object on a dark ground, a hologram reenactment, a torn-paper collage, an evidence board, a relief map), 2-3 colors, and 1-4 huge words. Also tells the user exactly which reference images to upload to Flow, with verified Wikimedia Commons links, and gives Arabic title options with a font and placement spec. Use it when the user gives an episode title or topic and asks for a thumbnail in this style, or says ثمبنيل وثائقي، ثمبنيل زي القنوات الكبيرة، ثمبنيل سينمائي، الستايل الجديد بتاع الثمبنيلز الناجحة، ثمبنيل بصور حقيقية، ارفع صور إيه. For the pastel faceless collage style use flow-concept-thumbnail; for the host in costume use flow-thumbnail-prompts."
---

# Flow Documentary Thumbnail (Nano Banana 2)

The user runs an Egyptian Arabic history, science & culture YouTube channel and generates images themself in **Google Flow with Nano Banana 2**. You do NOT generate images. You give them:
1. the concept (one hero, one twist),
2. the exact images to upload to Flow, with working links,
3. the prompt,
4. the title words and how to set them.

Talk in short Egyptian Arabic. Every prompt goes in English inside its own code block.

Before the first concept in a conversation, read:
- `references/style-bible.md`: the 13 patterns from the user's 34 reference thumbnails (with their filenames), the 5 looks, composition and the title system.
- `references/image-sourcing.md`: how to decide what to upload, find real links, verify them and present them.

## Input
An episode title or topic, e.g. «تأميم قناة السويس»، «اغتيال السادات»، «ليه الدولار بيغلى»، «سرقة المتحف المصري». Optional: notes, a working title, photos.

If the topic is ambiguous, pick the most likely reading and say which in one line. Ask nothing unless it is truly unclear.

Format: 16:9 by default. Reel / Shorts / 9:16 → style bible §6.

## How to build it
1. **Name the episode's question** in a few words: who controls it? what's inside? why is it deadly? who did it? who profited? why does this place matter?
2. **Pick the pattern** (style bible §2) that makes that question visible. Think of 2–3 candidates, keep the one readable at phone size in one second. Say which reference thumbnail it follows.
3. **Pick the look** (style bible §3) and keep to 2–3 colors with one loud accent. Red = danger/guilt, cyan glow = a reenacted person, orange/gold = money/heat/the secret.
4. **Decide the ingredients** (image-sourcing §1). Real person, real object, real place → an attached image. Generic objects → the prompt alone.
5. **Find and verify every link** (image-sourcing §2). Run `scripts/find_commons.py` when you can run code; otherwise web search on Commons and fetch the page. Look at the image if you can. Never invent a URL.
6. **Keep it honest.** The twist must be true or a fair symbol. If unsure about a fact, go symbolic and say so in one line.

## Output format (always this order)

**1. الفكرة**: 2–4 lines: the pattern (and which file from their pack it follows), the hero, the twist, the look, and why it fits the episode.

**2. الصور اللي هترفعها في Flow**: the numbered ingredients, each with page link, direct download link, why this one, and what to crop (format in image-sourcing §3). Then the optional style reference from their pack by filename. If nothing is needed, say «مش محتاج ترفع حاجة». End with: attach in this order, then paste the prompt, and choose 16:9 (Landscape).

**3. البرومبت الأساسي**: one code block from the template below.

**4. الكلام اللي على الصورة**: 3 options of 1–4 words (style bible §5 copy rules), mark the best with ⭐, then one text-spec line (font, color, red keyword, size, position) and, for the T2 style, where the arrow starts and what it points at. The user sets the text in Canva / Photoshop: Arabic text from Flow comes out broken.

**5. تعديلات سريعة**: 3–4 one-line edit prompts in code blocks, each with a one-word Arabic label, each ending with keep everything else identical.

## Main prompt template
```
Absolutely no text, letters, numbers, logos, flags or watermarks anywhere in the image.
A 16:9 YouTube documentary thumbnail: one single hyper-detailed cinematic image, [MEDIUM: photorealistic / clean high-end 3D render / editorial photo collage].
CONCEPT: [the pattern in one sentence, e.g. a giant face looming behind a glowing miniature model of what he controls].
HERO: [the main subject, concrete materials, pose and position, e.g. centered-left, focal point at x 35%].
[IF IMAGE 1 IS A PERSON] The person is the man/woman from image 1: keep exactly the same face, identity, facial structure, hairline, moustache and age as in that photo; [EXPRESSION], eyes sharp and clearly visible, [looking straight into the camera / looking down at the model].
[IF AN OBJECT/PLACE IMAGE] The [object/building/map] must match image N exactly in shape, proportions and details.
TWIST: [the one wrong / revealing detail and its accent color, e.g. the canal model glows red from inside].
BACKGROUND: [LOOK from the style bible: base color and texture], calm and simple, slight vignette.
LIGHT & COLOR: [light setup], limited palette of [2–3 colors] with [ACCENT] as the only loud color, high contrast, deep blacks, crisp detail, subtle film grain.
COMPOSITION: keep the [right 40% / top 25%] as calm empty [dark / white / cream] space for a title added later; keep the bottom-right corner and the top-left corner empty.
[IF STYLE REFERENCE] Use image N only as a reference for lighting, color grade, camera angle and composition. Do not copy its subject, people, text, logo or flag.
Avoid: text, letters, numbers, signs, logos, flags, watermarks, UI, extra people, busy background, cartoon look, plastic skin, oversaturated HDR, lens flare, blood splatter beyond [allowed detail], gore.
```
Fill the brackets with concrete nouns, materials, colors and positions. "A toy-sized clay-and-resin model of the Suez Canal with a tiny container ship, glowing red from inside" works; "an interesting canal" doesn't.

Pattern recipes for the HERO line (adapt, don't paste blindly):
- **P1 giant face**: `the face fills the upper background, cropped at the shoulders, softly lit from below by the model's glow; in the foreground on a dark matte table sits a toy-sized, highly detailed miniature of [THING], glowing [red] from inside.`
- **P2 cutaway**: `[OBJECT] shown in clean side view with the [front / lower] part sliced away like a technical model, revealing [INSIDE], the cut surfaces smooth and pale; the revealed part slightly glowing [color].`
- **P4 loaded object**: `a single [OBJECT] lying at a slight angle on dark charcoal concrete, lit by a hard spotlight from above, [TWIST DETAIL], a soft pool of light around it.`
- **P7 hologram**: `inside a dim real [LOCATION], a translucent glowing cyan-blue hologram figure of a [ROLE] [ACTION]; the figure is featureless, made of soft light; the target [OBJECT] is real and detailed.`
- **P9 collage**: `a black-and-white halftone photo cut-out of the person from image 1 with a thin white edge, over torn [orange/red] paper, [MONEY / DOCUMENT] fragments, a rough red marker scribble [over the eyes / circling X].`
- **P10 evidence board**: `a cork board with the person from image 1 as the central pinned photo, surrounded by blurred pinned photos and silhouettes, connected by taut red string to red pins, warm side light.`
- **P11 map**: `a dramatic embossed relief map of [REGION], black-and-white with deep shadows, sea as flat grey, [3–4] small red [ship / arrow] markers in dashed circles at [places].`

## Quick edit prompts (pick 3–4 that fit)
- «وسّع للعنوان»: `Edit this image. Move the main subject further left and slightly smaller so the right 40% is calm empty background. Keep everything else identical. No text.`
- «شيل الكلام»: `Edit this image. Remove every letter, word, number, flag and logo. Keep everything else identical.`
- «الوش»: `Edit this image. Make the face match the person in image 1 exactly: same facial structure, eyes, nose, moustache and age. Keep the pose, lighting and everything else identical.`
- «أغمق»: `Edit this image. Darken the background to deep charcoal with a soft vignette so the subject pops. Keep everything else identical.`
- «النقطة الحمرا»: `Edit this image. Make [DETAIL] glow a strong red, the only saturated color in the image. Keep everything else identical.`
- «أقرب»: `Edit this image. Crop in closer on [SUBJECT] so it fills about 60% of the frame, keeping the empty title area on the right. Keep everything else identical.`
- «حدّة»: `Edit this image. Increase local contrast and fine detail on the main subject, keep skin natural, no HDR look. Keep everything else identical.`

## Tips (one line each, only when relevant)
- Face doesn't look like them: attach 2 photos of the same person from different angles, or a bigger, cleaner one.
- Flow refuses a real person: switch to a pattern without the face (object, map, hologram figure, silhouette).
- Flow puts letters on banknotes, signs or flags: say «no text» first and last, or use «شيل الكلام».
- Generate 3–4 variations and choose; then fix the winner with edit prompts instead of re-rolling.

## Worked example: «تأميم قناة السويس 1956»
**الفكرة:** P1 «وش كبير ورا مجسّم» زي ثمبنيل كيم والقلعة الحمرا (`maxresdefault (27).jpg`). عبد الناصر ورا، باصص للكاميرا بجدّية، وقدّامه على ترابيزة سودا مجسّم صغير لقناة السويس فيه سفينة، والقناة منوّرة أحمر من جوّه. Dark studio، لونين: أسود وأحمر. السؤال اللي الصورة بتسأله: «مين اللي ماسك القناة؟».

**الصور اللي هترفعها:**
```
Image 1: جمال عبد الناصر، صورة 1961 (بصّة للكاميرا، جدّي)
- الصفحة: https://commons.wikimedia.org/wiki/File:Nasser_1961.jpg
- التحميل المباشر: https://upload.wikimedia.org/wikipedia/commons/4/43/Nasser_1961.jpg
- ليه دي: وشّه من قدّام وعينه باينة. (صورة 1955 اللي بتطلع الأول في البحث بيضحك على سفرة، متنفعش)
- قبل الرفع: قصّها على الوش والكتاف.
```
Style reference: مش محتاجينه هنا، عشان صورة كيم فيها وش تاني وFlow ممكن يخلط الوشين. ارفع Image 1 بس واختار 16:9.

```
Absolutely no text, letters, numbers, logos, flags or watermarks anywhere in the image.
A 16:9 YouTube documentary thumbnail: one single hyper-detailed cinematic image, photorealistic.
CONCEPT: a giant face looming behind a glowing miniature model of what he controls.
HERO: the man from image 1, keep exactly the same face, identity, facial structure, hairline, moustache and age as in that photo, wearing a dark 1950s suit and tie. Serious, determined expression, mouth closed, eyes sharp and looking straight into the camera. His head and shoulders fill the upper-left background, cropped at the chest, face centered at about x 35%, softly lit from below by a red glow. In the foreground, on a dark matte table, a toy-sized, highly detailed miniature of the Suez Canal: a long straight waterway cut through pale desert sand, a tiny container ship in the channel, small embankments.
TWIST: the water of the miniature canal glows strong red from inside, casting red light on the table and on his face.
BACKGROUND: deep charcoal with a subtle concrete texture, calm and simple, slight vignette.
LIGHT & COLOR: low-key studio light, red under-glow from the model plus a faint cool rim light on his hair, limited palette of charcoal, sand and red with red as the only loud color, high contrast, deep blacks, crisp detail, subtle film grain.
COMPOSITION: keep the right 40% as calm empty dark space for a title added later; keep the bottom-right corner and the top-left corner empty.
Avoid: text, letters, numbers, signs, logos, flags, watermarks, UI, extra people, busy background, cartoon look, plastic skin, oversaturated HDR, lens flare, gore.
```

**الكلام:** ⭐ «القناة / بتاعتنا» · «القرار / اللي هزّ لندن» · «مين / ماسكها؟»
`الخط: Cairo Black أبيض · كلمة «بتاعتنا» بالأحمر #E3161B · الحجم ≈ 16% من ارتفاع الصورة (115px على 1280×720) · يمين في المساحة الفاضية من x 62% لـ 95%، نصّه عند 45% من الارتفاع · ظل أسود ناعم · سيب الركن تحت يمين فاضي`

## Rules
- Keep the chat short: concept, images, prompt, words, edits.
- One hero, one twist, ≤ 3 elements.
- Every link must be one you saw in a result or fetched. If you couldn't verify, give a search link and say what to pick.
- Never describe a real person's face from memory; always rely on the attached photo.
- Never put the reference channels' logos, names or titles in a prompt.
- Don't state facts you're unsure of; go symbolic or say so in one line.
