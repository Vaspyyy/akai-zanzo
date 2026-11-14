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
- **Right-hand drive in side views.** "Right-hand drive" alone doesn't stick. In a side view with the driver at the near window, state the direction: the car's FRONT points to the LEFT edge of the panel (so we see its right/driver side).
