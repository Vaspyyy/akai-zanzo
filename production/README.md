# Production tools

Scripts that turn a page spec into finished manga pages:
**spec (YAML) → prompt builder → `codex exec` image jobs → saved page → lettering → contact sheet**.

Everything runs from the repo root with `production/az`.

```sh
production/az lint    -c 3                  # check chapter-003.yaml against cast/locations
production/az prompt  -c 3 -p 4             # print the image prompt + reference list for page 4
production/az run     -c 3 -p 1-6,9         # generate pages 1-6 and 9 (4 in parallel)
production/az run     -c 3 -p 2 --dry-run   # same as prompt; add --full for the whole codex brief
production/az letter  -c test-pages         # (re)letter empty-balloon pages from the spec
production/az contact -c 2 -p 20-28         # contact sheets of existing pages
production/az run     -c plates -p classroom   # (re)make a location plate
```

`-c` takes a chapter number (`production/chapter-NNN.yaml`) or a spec name
(`plates`, `test-pages` → `production/<name>.yaml`); `--spec FILE` takes any file.
`-p` takes numbers, ranges and ids (`1-6,9`, `harbor-station-night`), default all.

## Files

| Path | What |
| --- | --- |
| `cast.yaml` | Characters and cars: traits, a one-line "tell" to tell people apart, outfits with their sheet. |
| `locations.yaml` | Places: description, clean plate, approved source pages, guards. |
| `templates/prompt.md` | **All prompt wording** in named sections. Edit wording here, not in Python. |
| `chapter-NNN.yaml` | One spec per chapter. `chapter-002.yaml` is the worked example. |
| `plates.yaml` | Specs for the empty location plates in `artwork/locations/`. |
| `test-pages.yaml` | Two test pages for the lettering pass (`artwork/pages/test/`). |
| `aztools/` | The code: `spec.py` (load + lint), `build.py` (prompt builder), `runner.py` (codex jobs, provenance), `letter.py` (lettering), `contact.py`. |
| `fonts/fetch-fonts.sh` | Downloads the lettering font (gitignored, see below). |
| `logs/provenance.jsonl` | One JSON line per job: prompt, refs requested, refs image_gen really got, model, effort, tier, time, calls, warnings. Committed. |
| `runs/` | Per-batch work folders: codex brief, events, stderr, agent reply, contact sheets, lettering debug overlays. Gitignored. |

## Page spec format

```yaml
chapter: 3                  # numeric chapter -> output artwork/pages/chapter-003/
title: Some title
lettering: empty            # ai (the image model letters) | empty (empty balloons + letterer); per page too
output_dir: artwork/pages/test   # only needed when there is no numeric chapter
defaults:                   # merged into every page
  orientation: portrait

pages:
  - page: 4                 # -> page-04.png; "8-9" -> page-08-09.png (use orientation: landscape)
    title: Cold shoulder    # for humans only
    location: harbor-station-night   # id from locations.yaml (plate is attached automatically)
    time: about 2 AM        # default: the location's default_time
    weather: heavy rain
    continue_from: 3        # or "previous": attach page 3 and keep the camera on the same side
    driver_hidden: true     # Roadster's driver must stay unrecognizable (chapter 1 rule)
    lettering: ai           # override the chapter default
    refs:                   # extra references, in addition to the automatic ones
      - {path: artwork/pages/chapter-002/page-20.png, use: "Akane's face as revealed"}
    notes: ["free-text rule added to the RULES block"]
    guards: ["another rule line"]
    panels:                 # in READING ORDER (right to left, top to bottom)
      - pos: top-right      # top-right, top-left, middle, "top, wide", "bottom, large", ...
        shot: close-up      # optional
        location: harbor-road-night   # optional per-panel location (adds its plate)
        action: Dai walks toward the driver's window.
        cast:               # only these people/cars are in the panel
          - dai:station     # id[:outfit]
          - {id: roadster, state: headlights_down, facing: left}
          - {id: akane, hidden: true, note: "only her gloved fingers"}
        dialogue:           # each line tied to ONE speaker, in reading order
          - dai: "ARE YOU HIRING?"
          - kubo: {text: "HAH.", style: small, at: "top left, above Kubo"}
          - {speaker: kubo, text: "...", offpanel: true, box: [610, 90, 230, 170]}
        captions: ["10:00 PM.", {text: "THE END.", style: small, at: "bottom corner"}]
        sfx: ["KA-CHAK", {text: "kachan", note: small}]
        notes: ["extra line for this panel"]

  - page: 27
    edit:                   # redraw an existing page, change only X
      change: "In panels 2-4 the car's FRONT must point LEFT; remove the second car in panel 4."
      keep: "the KA-CHAK headlight panel and all dialogue"
      # source: defaults to the current page file (attached as reference 1)
    panels: [...]           # still describe the page; the edit text says what to change
```

Plates (`plates.yaml`) use `id:` instead of `page:`, `kind: plate`, a `location` and a `description`.

### What the builder adds automatically

- The style block, page format (portrait / landscape / plate) and the lettering mode text.
- Cast traits and sheets for **only** the characters and cars on the page; the right sheet per outfit.
- Per panel: "In this panel: ONLY X (tell)", and "Only X speaks in this panel; Y says nothing" when one of two people talks.
- Balloon order and placement hints; in empty mode a size hint per balloon ("roomy enough for about N words").
- Roadster on the page: right-hand-drive rules and "front points LEFT in side views". Not on the page: "NO small roadster or sports car anywhere".
- `driver_hidden`, `continue_from` (same camera side), location guards, the 1995 rule, English-only / no watermark.
- A self-check list the codex agent must go through before saving (faces, speakers, car side, empty balloons); it may redraw once (`--attempts`).
- Warnings: missing plate (falls back to a source page that contains people/cars), more than 5 refs (image_gen rejects the call), missing files.
- `lint` warns about panels with two on-panel speakers (speaker-swap risk).

## Runner

For each page `run` builds the prompt, writes the codex brief to `runs/<batch>/<page>/prompt.txt` and starts:

```sh
codex exec -m gpt-6.1-terra -c model_reasoning_effort="medium" -c service_tier="default" \
  --skip-git-repo-check -C <repo> --json -o runs/<batch>/<page>/last.txt -   # brief on stdin
```

The brief tells the agent to call its built-in `image_gen` tool with the reference paths in
`referenced_image_paths` (no `-i` needed), run the self-check, and copy the result to the job folder.
The runner then reads the codex session log (`~/.codex/sessions/.../rollout-*<thread>.jsonl`) to record which
references `image_gen` really received and how many images it made, and:

- saves the page to `artwork/pages/chapter-NNN/page-NN.png` (empty mode: `page-NN.art.png`, then letters it into `page-NN.png`);
- keeps the previous file as `page-NN.prev.png` / `page-NN.art.prev.png`;
- appends a JSON line to `logs/provenance.jsonl` and a row to `artwork/PROVENANCE.md` ("generated, not reviewed": edit the status after review);
- writes contact sheets (3 pages side by side, 640 px tall) to `runs/<batch>/contact-NN.jpg`.

Pages with `continue_from` a page in the same batch wait for it (waves). `-j` sets parallel jobs (default 4, max 6).
Each job takes about 1.5 to 3 minutes; each `image_gen` call is one generation on the Codex subscription.

## Lettering pass (`lettering: empty`)

The image model draws empty white balloons (ovals with tails) and empty caption boxes, plus the SFX.
`letter.py` then:

1. finds the page margin + gutters (white area touching the edge) and the panels they enclose;
2. finds enclosed white regions that are flat white inside with a dark outline, and classifies them as
   balloon (fits an ellipse once the tail is stripped) or caption (rectangle); balloons that cross a panel
   border are recovered from the gutter;
3. orders panels right-to-left/top-to-bottom (XY cut) and balloons inside a panel right-to-left, higher first when stacked;
4. gives the spec's dialogue to balloons and captions to boxes, panel by panel (page-wide if the panel
   count differs, with a warning);
5. sets the text uppercase in Anime Ace 2.0 BB (captions italic, `style: bold` bold, `style: small` smaller),
   wrapped to the real shape and auto-sized.

It prints a report per line (box, size, lines) and saves a debug overlay to `runs/.../<page>.letter-debug.jpg`
(blue = panels, green = balloons, orange = captions with their speaker, red = unused candidates).
When detection fails, give the line a manual box: `box: [x, y, w, h]` in art pixels (the report lists unused
candidates you can copy). Re-run `production/az letter -c N -p P` after editing the spec; it never calls the image model.

**Known limits:** the speaker is assigned by reading order, not by the tail direction, so the spec order must
match the balloon positions (first speaker = right-most / top balloon; the prompt asks for this).
Balloons drawn too small for their text get small type (reported as small sizes / OVERFLOW).
Jagged "shout" balloons and borderless panels are detected less reliably.
Chapters 1 and 2 have AI lettering and are never re-lettered.

### Font

`production/fonts/fetch-fonts.sh` downloads **Anime Ace 2.0 BB** (Nate Piekos / Blambot) into
`production/fonts/anime-ace-2/` with its license text. It is free for independent comics and non-profit use,
but may not be redistributed, so the font files are gitignored: run the script once per machine.

## Location plates

`artwork/locations/*.png` are empty reference backgrounds (no people, no vehicles) made with
`production/az run -c plates`. The builder attaches a page's plate instead of an old page, which stops
cars and people from older pages leaking into new ones. When a plate is missing, the builder falls back to
the location's first source page and warns.

## Build

`./tools-build.sh 002` packs only `page-NN.png` / `page-NN-MM.png` and ignores `.art.png`, `.prev.png`
and any other extra files.
