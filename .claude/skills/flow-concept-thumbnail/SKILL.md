---
name: "flow-concept-thumbnail"
description: "Writes ready-to-paste Nano Banana 2 prompts for Google Flow that make a faceless YouTube thumbnail for an episode: one witty visual metaphor of the episode's topic in a pastel editorial-collage style (cream paper border, rounded pastel panel, heavy grain, hero on the left, empty right side for the title), plus 3 suggested Arabic question titles the user types on top. Use it when the user gives an episode title or topic and wants a thumbnail without the host's face, or says ثمبنيل من غير وشي، ثمبنيل للحلقة، ثمبنيل فكرة، نفس استايل سياق، برومبت ثمبنيل بالاستايل الجديد. Also makes the same style as a vertical 9:16 Reel / Shorts / TikTok cover when asked (ريل، ريلز، شورتس، كفر الريل، 9:16، بمقاس الريل). When the host should appear in costume, use flow-thumbnail-prompts instead."
---

# Flow Concept Thumbnail (faceless, Nano Banana 2)

The user runs an Egyptian Arabic history, science & culture YouTube channel and generates images themself in **Google Flow with Nano Banana 2**. Your job is NOT to generate images. Give them:
1. a concept (the one picture that explains the episode),
2. prompts to paste into Flow,
3. title suggestions they will type on the image themself.

Talk in short Egyptian Arabic. Write every prompt in English inside its own code block, so it copies in one tap.

The style comes from a set of pastel Arabic explainer thumbnails the user loves. The full breakdown of those references (metaphor patterns, mediums, palettes, measured layout) is in `references/style-bible.md`. Read it before the first concept in a conversation; it is what makes the result look like the references and not like generic AI art.

## Input
An episode title or topic, e.g. «الهرم الأكبر», «دنشواي», «ليه القهوة بتصحّي», «سقوط الأندلس». Optionally a working title, notes, or photos.

If the topic is ambiguous, pick the most likely reading and say which in one line. Ask nothing unless the episode is truly unclear.

**Format:** YouTube 16:9 by default. If the user mentions a Reel, Shorts, TikTok, story, cover, 9:16 or «مقاس الريل», make the Reel version (see «Reel version (9:16)» below). If they ask for both, give the 16:9 first, then the Reel with the same concept and palette, so the two posts look like a set.

## How to build the concept

1. **Turn the episode into one question.** The references are all questions: إزاي / ليه / هل. The question is what the image answers.
2. **Find ONE visual metaphor that makes the question visible at a glance.** This is the most important step: the image is a clever idea, not a scene illustration. Use one of the patterns in the style bible (cutaway / exploded view, object as a place, progression of sizes, tiny culprit under a spotlight, iconic gesture collage, extreme crop with a twist, quiet character with one telling detail). Before choosing, think of 2–3 candidates and pick the one a viewer gets in under a second at phone size.
3. **Pick the medium** (style bible §2): soft 3D clay, vintage collage (B&W photo cut-outs + engraving), flat grainy illustration, or studio still-life photo. History episodes usually work best as vintage collage or flat illustration; objects, buildings and science as 3D clay or still-life.
4. **Pick the palette** (style bible §3): one pastel panel color chosen by mood, a coral/orange warm accent, the subject muted. Never chartreuse in the art, because chartreuse is reserved for the title boxes.
5. **Keep it historically and scientifically honest.** If you are unsure of a fact, go symbolic instead of inventing details.

## Fixed layout (bake it into every prompt)
- Cream paper border (#EDE7DB) about 2% of the width, around a large rounded-corner panel.
- **Hero on the LEFT ~55%**, grounded by a flat shadow, a floor plane, or bleeding off the bottom/left edge. It may tuck slightly under the title area.
- **Right ~45% calm:** only the flat panel color or a soft gradient. The title goes at right-center (x ≈ 45–95%, y ≈ 38–68%), the user's own logo top-right (x ≈ 70–95%, y ≈ 8–32%).
- Top-left corner clear (≈ x 4–14%, y 8–24%) for the user's badge or episode number.
- **No text, letters or numbers in the image, ever.** The user types the title.
- Heavy, even, fine film grain over everything, the border included.
- Never copy the reference channel's logo, badge or name.

## Output format (always this order)

**1. الفكرة**: 2–4 Egyptian Arabic lines with the metaphor, the medium, and the panel color, and why it works for this episode.

**2. ترفع إيه في Flow**: usually nothing. Only if a real person, building or artifact must be recognizable, list the images to attach (e.g. "Image 1: a public-domain photo of Saad Zaghloul, from Wikimedia Commons"). Remind them to pick 16:9 (Landscape).

**3. البرومبت الأساسي**: one code block, from the template below.

**4. اقتراحات العنوان**: 3 options, each split into the 2 lines it will sit on, for example:
- «إزاي اتبنى / الهرم الأكبر؟»
Rules: a question, Egyptian or plain colloquial Arabic, 2 lines, ideally 2–3 words and ≤ 14 characters per line, curiosity without lying. Mark the one you'd pick with ⭐. Then add one line with the text spec from the style bible §5 (font, chartreuse box, size, position), so the user can match the look in Canva or Photoshop.

**5. تعديلات سريعة**: 3–4 one-line edit prompts in code blocks, each with a one-word Arabic label. Pick the ones relevant to this concept from the list below, and each must say to keep everything else identical.

## Main prompt template
```
Absolutely no text, letters, numbers, logos or watermarks anywhere in the image.
A 16:9 YouTube thumbnail artwork in a modern Arabic editorial-magazine style.
FRAME: a thin off-white cream paper border (#EDE7DB, about 2% of the width on every side) around one large panel with softly rounded corners. Everything below is inside that panel.
PANEL BACKGROUND: [PANEL COLOR / GRADIENT], flat and calm, [ACCENT: e.g. a soft blurred coral-orange radial glow behind the subject / a flat peach circle and a flat deep-green circle as graphic shapes].
HERO, LEFT 55% of the panel: [THE METAPHOR, one clear idea, concrete objects and their arrangement]. Rendered as [MEDIUM]. [GROUNDING: e.g. standing on a flat charcoal floor plane in slight isometric perspective / soft flat contact shadow / cropped by the bottom edge].
RIGHT 45% of the panel: empty, only the calm background color, no objects, no shadows, no stripes. Top-left corner also empty.
LOOK: limited palette of [2–3 COLORS] plus one warm coral/orange accent, subject slightly desaturated, soft matte light, gentle airbrushed gradients, crisp silhouette, heavy fine risograph film grain over the whole image including the border, slightly vintage print feel. Witty, conceptual, minimal: one idea readable at phone size.
Avoid: text, letters, signs, labels, numbers, flags, logos, UI, extra frames, busy backgrounds, photoreal environments, glossy HDR, neon, lens flare, multiple competing subjects, gore.
```
Fill the brackets with concrete nouns, colors and materials. Vague words like "beautiful" or "interesting" don't help Nano Banana; "a mud-brick pigeon tower, cut in half like a dollhouse" does.

If an image is attached for a real person: in HERO write "the person from image 1, same face and features, as a black-and-white halftone photo cut-out with a thin white edge", and never describe their face from memory.

## Quick edit prompts (pick 3–4 that fit)
- «وسّع مكان العنوان»: `Edit this image. Move the main subject further left and slightly smaller so the right 45% of the panel is completely empty background. Keep everything else identical. No text.`
- «شيل الكلام»: `Edit this image. Remove every letter, word, number and sign-like mark. Keep everything else identical.`
- «الإطار»: `Edit this image. Add a thin off-white cream (#EDE7DB) paper border around the whole image, with the artwork inside a panel with softly rounded corners. Keep the artwork identical.`
- «حبّة أكتر»: `Edit this image. Add heavy fine monochrome film grain evenly over the whole image, like a risograph print. Keep everything else identical.`
- «لون تاني»: `Edit this image. Change only the panel background to [COLOR]; keep the subject, accent, grain and composition identical.`
- «بسّط»: `Edit this image. Remove [SECONDARY ELEMENT] so only the main idea remains. Keep everything else identical.`
- «أدفى»: `Edit this image. Add a soft blurred coral-orange glow behind the main subject. Keep everything else identical.`

## Tips (only when relevant, one line each)
- If Flow writes text anyway: put «Absolutely no text» first and last in the prompt and re-run, or use «شيل الكلام».
- If the rounded frame comes out wrong: generate without the FRAME line and add the border later with «الإطار».
- If Flow refuses a real person: use a silhouette, their hat or tool, or a symbol instead.
- Generate 2–4 variations and choose; the metaphor matters more than any single render.

## Worked example: «الهرم الأكبر»
**الفكرة:** الهرم متقطّع نصّين زي مجسّم مدرسي، ومن جوّه باين رامب حلزوني (دي نظرية من النظريات، فالصورة بتسأل مش بتأكّد) وعمّال صغيرين بيشدّوا حجر، وبعيد عنه حجر واحد ضخم على زلّاقة خشب. ستايل 3D clay مطفي، الخلفية بيج رملي فيه توهّج برتقالي ورا الهرم. الصورة نفسها بتسأل السؤال: «الحجر دا طلع إزاي؟».

```
Absolutely no text, letters, numbers, logos or watermarks anywhere in the image.
A 16:9 YouTube thumbnail artwork in a modern Arabic editorial-magazine style.
FRAME: a thin off-white cream paper border (#EDE7DB, about 2% of the width on every side) around one large panel with softly rounded corners. Everything below is inside that panel.
PANEL BACKGROUND: a flat warm sand-beige backdrop fading to dusty peach at the top, with a soft blurred coral-orange radial glow behind the subject.
HERO, LEFT 55% of the panel: the Great Pyramid of Giza as a sliced cutaway model, the front quarter removed like a school diorama, revealing an internal spiral ramp; tiny workers in white kilts haul one limestone block up the ramp with ropes; one giant limestone block rests on a wooden sledge at the base. Rendered as a soft matte 3D clay render with airbrushed gradients. Seen in slight isometric perspective on a flat sand-colored floor plane with a soft contact shadow, the base cropped by the bottom edge.
RIGHT 45% of the panel: empty, only the calm background color, no objects, no shadows, no stripes. Top-left corner also empty.
LOOK: limited palette of sand beige, limestone white and charcoal plus one warm coral/orange accent, subject slightly desaturated, soft matte light, gentle airbrushed gradients, crisp silhouette, heavy fine risograph film grain over the whole image including the border, slightly vintage print feel. Witty, conceptual, minimal: one idea readable at phone size.
Avoid: text, letters, signs, labels, numbers, flags, logos, UI, extra frames, busy backgrounds, photoreal environments, glossy HDR, neon, lens flare, multiple competing subjects, gore.
```
**العنوان:** ⭐ «إزاي اتبنى / الهرم الأكبر؟» · «مين بنى / الهرم بجد؟» · «الحجر دا / طلع إزاي؟»

## Reel version (9:16)
Same concept, medium, palette, grain and cream frame; only the layout changes to vertical. Phone apps cover parts of a Reel, so the layout keeps everything important inside the safe area: the app UI covers the top ≈ 12%, the caption and buttons cover the bottom ≈ 20%, the like/comment icons sit on the right edge from y ≈ 55% down, and the Instagram profile grid crops the cover to the center 3:4 (y ≈ 12.5–87.5%).

**Reel layout**
- Cream border ≈ 3% of the width, around a panel with rounded corners (radius ≈ 5% of the width).
- **Top ≈ 40% of the panel calm:** only the background color. The title goes here (x ≈ 8–92%, y ≈ 17–37%) and the user's own logo just above it (y ≈ 12–17%).
- **Hero in the lower-middle, centered horizontally,** its focal point at y ≈ 45–72%. It may grow larger and bleed off the bottom edge, but nothing important below y ≈ 80%, and keep the right edge below y ≈ 55% free of key details.
- Tall formats suit vertical metaphors: a tall stack, a hanging object, a falling thing, a tower, a scale, a thread pulled up. If the 16:9 metaphor is wide, rearrange it vertically rather than shrinking it.

**Reel prompt template**
```
Absolutely no text, letters, numbers, logos or watermarks anywhere in the image.
A vertical 9:16 Reel cover artwork in a modern Arabic editorial-magazine style.
FRAME: a thin off-white cream paper border (#EDE7DB, about 3% of the width on every side) around one tall panel with softly rounded corners. Everything below is inside that panel.
PANEL BACKGROUND: [PANEL COLOR / GRADIENT], flat and calm, [ACCENT: e.g. a soft blurred coral-orange radial glow behind the subject].
TOP 40% of the panel: empty, only the calm background color, no objects, no shadows, no stripes.
HERO, centered horizontally in the lower-middle of the panel, its focal point between 45% and 72% of the height: [THE METAPHOR, arranged vertically, concrete objects]. Rendered as [MEDIUM]. [GROUNDING: e.g. standing on a flat floor plane with a soft contact shadow / its base cropped by the bottom edge]. Keep the main details away from the right edge and the bottom 20%.
LOOK: limited palette of [2–3 COLORS] plus one warm coral/orange accent, subject slightly desaturated, soft matte light, gentle airbrushed gradients, crisp silhouette, heavy fine risograph film grain over the whole image including the border, slightly vintage print feel. Witty, conceptual, minimal: one idea readable at phone size.
Avoid: text, letters, signs, labels, numbers, flags, logos, UI, extra frames, busy backgrounds, photoreal environments, glossy HDR, neon, lens flare, multiple competing subjects, gore.
Absolutely no text anywhere.
```
In Flow choose **9:16 (Portrait)**.

**From an existing 16:9 thumbnail** (keeps the exact same look): attach the generated thumbnail as image 1, choose 9:16, and use:
```
Recompose image 1 as a vertical 9:16 Reel cover. Keep the same subject, rendering style, colors, grain and cream paper border with rounded corners. Place the subject centered in the lower-middle, larger, focal point between 45% and 72% of the height; leave the top 40% of the panel as empty calm background. Absolutely no text, letters or numbers.
```

**Reel titles:** same rules, but up to 3 short lines (≤ 12 characters each), because the width is narrower. Give the Reel text spec from the style bible §5b.

**Reel quick edits** (in addition to «شيل الكلام», «حبّة أكتر», «لون تاني»):
- «فضّي فوق»: `Edit this image. Move the main subject lower and slightly smaller so the top 40% of the panel is completely empty background. Keep everything else identical. No text.`
- «كبّر»: `Edit this image. Make the main subject larger and centered, focal point between 45% and 72% of the height, still leaving the top 40% empty. Keep everything else identical. No text.`
- «الإطار»: `Edit this image. Add a thin off-white cream (#EDE7DB) paper border around the whole image, with the artwork inside a tall panel with softly rounded corners. Keep the artwork identical.`

## Rules
- Keep the chat short: the concept, the prompt, the titles, the edits.
- One idea per thumbnail. If two ideas compete, cut one.
- The host's face never appears in this style. If the user wants themself in it, switch to flow-thumbnail-prompts.
- Don't state facts you're unsure of; say so in one line or go symbolic.
