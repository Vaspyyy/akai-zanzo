# Art direction (all artwork)

## Style block (paste into every image prompt)

> Black-and-white Japanese seinen manga page, late-1990s street-racing manga style. Confident ink linework with varied line weight, grey screentone shading and dot patterns, heavy solid blacks for night scenes, dramatic speed lines and focus lines during motion. Realistic adult proportions, not chibi, not moe. Gritty urban mood. Cars drawn with technical precision and correct proportions. No color at all: pure black ink, white paper and grey screentone only.

## Pages

- **Portrait page, 2:3 aspect** (e.g. 1024x1536), white page margins and white gutters between panels, panel borders in black ink.
- **Reading order is right-to-left** (Japanese manga): the first panel is top-right, then moves left, then down. Prompts describe each panel by position.
- **English lettering:** dialogue in white oval speech balloons with tails pointing to the speaker, black uppercase comic lettering (clean manga scanlation style). Inner thoughts / narration in rectangular caption boxes. Sound effects as big hand-drawn English letters integrated into the art. All text exactly as written in the script; no extra text, no Japanese characters, no watermark, no page numbers.
- A double-page spread is one landscape image (3:2).

## Consistency rules

- Always attach the relevant reference sheets and tell the model to match faces, hair, outfit and car details exactly.
- Red Roadster: right-hand drive, black soft top up, pop-up headlights (state per panel), silver 7-spoke 14" wheels, no wing, no stickers.
- Silvia S13: white, fixed slim headlights (no pop-ups), big rear wing, black wheels.
- 1995 only: no phones, no modern cars, no LED lights, no modern signage.
- **Chapter 1: the Roadster's driver is never recognizable.** Cabin in deep shadow / windshield glare; at most gloved hands and a dark silhouette. Image models tend to put the protagonist's face in the driver seat, so say this explicitly in every prompt that shows the car moving.
- **Safety filter:** a lone, distressed figure gripping a bridge railing at night can be refused as "self-harm". On bridge scenes, put Dai safely on the walkway (tall fences), and spell out the emotion (awe, excitement) rather than "trembling, staring into the distance".
- **Reference pages leak objects.** A location reference that contains the red Roadster (e.g. ch1 p17) makes the model copy the car into the new page. When the Roadster must NOT be there, say so explicitly ("no small roadster or sports car anywhere").
- **Speaker swaps.** With two characters in adjacent panels, the model can hand each one the other's line. Put ONLY one named character in each single-speaker panel, describe them by unmistakable traits (old/young, hair), and check every balloon's owner on review.
- **Never use a two-character reference sheet.** `kubo-station-uniform.png` (Kubo + Dai on one sheet) made the model swap their faces on 8 pages. Use the split sheets `character-sheets/kubo.png` and `character-sheets/dai-uniform.png`, pass only the sheets for characters on that page, and spell out each character's unmistakable traits (age, hair, how the shirt is worn).
- **Approved neighbour pages make good references.** For scenes that span pages (e.g. ch2 p20-27), pass an approved page from the same scene so lighting, faces and setting carry over.
- **Right-hand drive in side views.** "Right-hand drive" alone doesn't stick. In a side view with the driver at the near window, state the direction: the car's FRONT points to the RIGHT edge of the panel (so we see its right/driver side, like a face turned right shows its right cheek). Front pointing LEFT shows the passenger (left) side, with the driver on the far side. Corrected 2026-11-15: chapters 1-3 used the reversed rule, so some of their side views show a mirror-image car; accepted, don't redraw.
- **Keep the camera on one side across pages (180-degree rule).** Each page is drawn in isolation, so the model may jump to the opposite end of a car or room between pages, which reads as the car "turning around". When a scene continues, pass the previous page as a reference and say "seen from the SAME side as the previous page's last panel". Review consecutive pages side by side, not only one at a time.
- **The model copies car poses from its references.** Given the full car sheet, it pastes the sheet's flat side view; given a previous page with a car shot, it pastes that car again, so one copy snowballs through a chapter (ch3 p15, p18 and p26 had the same side view, front left, pop-ups up, spray behind). So: give every exterior car shot an explicit, different camera angle (`camera:` on the car's cast entry: height, side, which flank, where the nose points); attach an angle-specific crop of the car sheet instead of the whole sheet (`view: front34`, `rear`, `interior` in `production/cast.yaml`); and never pass a page that contains a similar car shot as a reference: use the location plate and approved interior pages for continuity. To redraw one panel, blank it to flat grey in a copy of the page and use that copy as the edit source, then paste the new panel back into the approved page. `production/az lint` warns about car shots without `camera:` and about car pages that pass another car page as a reference. Before approving, check that no two car shots in a chapter share a pose.
- **Caption-only panels get stray balloons.** The model adds empty speech balloons to panels that only have captions (ch4 p01, p18, p29). The builder now says "NO speech balloons in this panel" for those; check for them on review and edit them out.
- **Shifting on air reads as punching.** "Left hand on an invisible lever" came out as a fist thrust forward. Spell it out: the hand low beside the hip at console height, fingers curled round a small knob, and which side of the image it is on when the person faces the camera (ch4 p01-p04).
- **Vary shot sizes; keep the protagonist in key beats.** Don't repeat the same flat side view panel after panel. Emotional beats want close-ups and over-the-shoulder shots that keep Dai in frame.

## Production tools

Page prompts are now built from YAML page specs instead of hand-written briefs: `production/az run -c N -p 1-6` builds each prompt from `production/cast.yaml`, `production/locations.yaml` and `production/templates/prompt.md` (which apply the rules above automatically), runs the Codex image jobs, saves the pages, logs provenance and makes contact sheets. Empty location plates live in `artwork/locations/`. New chapters can use `lettering: empty` (empty balloons, then a lettering pass in Anime Ace). See `production/README.md`.
