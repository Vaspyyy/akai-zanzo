# Prompt template

Edit the wording here; the builder (`production/aztools/build.py`) only fills
the `{placeholders}` and decides which sections to use. Each section starts with
a line `## name`. Text above the first section (this intro) is ignored.
Placeholders that are not known stay as they are, so typos show up in
`production/az prompt`.

## job
Act as the image sub-agent for this task. Generate ONE image with your built-in image generation tool (`image_gen`) and save it as a PNG at exactly:
{staging_path}

Pass these reference images to `image_gen` in `referenced_image_paths`, in exactly this order (look at each one with view_image first):
{ref_list}

Send the IMAGE PROMPT below to `image_gen` verbatim. After it finishes, look at the result and go through the SELF-CHECK. If any check fails, call `image_gen` again with the same prompt plus one short sentence at the start naming the fix (at most {max_attempts} `image_gen` calls in total), then keep the best result. Copy the chosen PNG from ~/.codex/generated_images/ to the path above. Do not create, edit or delete any other file, and do not run other tools on the repository.

Reply in this format:
SOURCE: <path you copied from>
SIZE: <width>x<height>
CALLS: <number of image_gen calls>
CHECK: <one line per self-check item: PASS or FAIL + a few words>

IMAGE PROMPT:
<<<
{image_prompt}
>>>

SELF-CHECK:
{self_check}

## style
Black-and-white Japanese seinen manga, late-1990s street-racing manga style. Confident ink linework with varied line weight, grey screentone shading and dot patterns, heavy solid blacks for night scenes, dramatic speed lines and focus lines during motion. Realistic adult proportions, not chibi, not moe. Gritty urban mood. Cars drawn with technical precision and correct proportions. No color at all: pure black ink, white paper and grey screentone only.

## format-portrait
A single manga PAGE, portrait 2:3 (1024x1536). White page margins, black panel borders, white gutters between panels. Japanese reading order: right to left, top to bottom; the first panel is at the top right.

## format-landscape
A double-page manga SPREAD as one landscape 3:2 image (1536x1024). White page margins, black panel borders, white gutters between panels. Japanese reading order: right to left, top to bottom; the first panel is at the top right.

## format-plate
A single wide landscape 3:2 illustration (1536x1024), NOT a comic page: one full-bleed image with no panels, no borders, no text. It is a background reference plate for a manga, drawn in the same style as the reference pages.

## lettering-ai
Speech balloons are white ovals with a tail pointing at the speaker, with black uppercase comic lettering (clean manga scanlation style). Narration and inner thoughts go in white rectangular caption boxes with a thin black border. Sound effects are big hand-drawn English letters integrated into the art. All text exactly as written below, English only: no other text, no Japanese characters, no signs with readable words, no page number, no watermark, no signature.

## lettering-empty
LETTERING IS ADDED LATER BY HAND, SO DRAW NO DIALOGUE TEXT. Draw every speech balloon as a large, EMPTY, pure-white oval with a clean black outline and a short tail pointing at the speaker, and every caption as an EMPTY pure-white rectangle with a thin black border. Leave the inside of every balloon and caption box completely blank: no letters, no lines, no dots. Each balloon and caption sits fully INSIDE its panel, does not touch the panel border and does not overlap another balloon. Make each balloon roomy enough for its line (the size hints below). Draw exactly the balloons and captions listed, no extra ones. Sound effects ARE drawn: big hand-drawn English letters integrated into the art, exactly as written. Otherwise English only: no Japanese characters, no signs with readable words, no page number, no watermark, no signature.

## lettering-plate
No text of any kind: no lettering, no signs with readable words, no captions, no watermark, no signature.

## references
REFERENCE IMAGES (in order):
{ref_legend}

## setting
SETTING: Japan, 1995 (no phones, no modern cars, no LED lights, no modern signage). Location: {location_name}. {location_description} Time: {time}.{weather}

## cast-intro
CHARACTERS ON THIS PAGE (only these; match their reference sheets exactly, faces, hair and clothes):

## cast-character
- {name}: {traits} Wears: {outfit}. Reference: {ref_index}.

## cast-car
- {name}: {traits} Reference: {ref_index}.{rules}

## panels-intro
PANELS ({panel_count}, in reading order):

## rules-intro
RULES:

## self-check-page
- The page has {panel_count} panels in the described positions, read right to left.
- Every character's face, hair and clothes match their reference sheet; nobody has another character's face.
- Each speech balloon belongs to the character named for it (its tail points at that character), and single-speaker panels contain only that speaker's balloons.
- English only; no Japanese characters, no watermark, no page number, no extra text.

## self-check-ai
- Every line of dialogue, caption and sound effect is spelled exactly as written and appears exactly once.

## self-check-empty
- Every speech balloon and caption box is completely EMPTY (pure white inside, no letters) and lies fully inside its panel; the number of balloons per panel matches the list.

## self-check-roadster
- The red Roadster is right-hand drive; in side views showing the driver, its FRONT points to the RIGHT edge of the panel. Only one Roadster per panel.

## self-check-no-car
- There is NO small roadster or sports car anywhere on the page.

## self-check-plate
- There are NO people, NO human figures or silhouettes and NO vehicles of any kind anywhere in the image (no cars, trucks, bikes, forklifts).
- No text, no panels, no borders; one single full-bleed illustration in landscape orientation.
- The location matches the reference pages (same architecture, same props, same mood).

## edit
EDIT MODE: Reference 1 is the current version of this page. Redraw it, keeping everything the same (layout, art style, faces, all lettering) EXCEPT: {change}{keep}
