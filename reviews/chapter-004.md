# Chapter 4 review

Build: `./tools-build.sh 004` -> `build/akai-zanzo-ch004.{cbz,pdf}` (30 pages), copied to the documents folder.
Script: `scripts/chapter-004.md` (adapts light novel Vol. 1 Ch. 1, "Practicing"). Spec: `production/chapter-004.yaml`.

Drawn on 2026-11-15 in one session: 40 image generations in all.
- 5 references: Nobu Kawamata's sheet (`character-sheets/nobu.png`, new `kind: sheet` in `production/sheets.yaml`),
  the harbor station and harbor road night plates redrawn DRY, a bookstore plate, and a dawn plate of the
  overpass curve with the newer guardrail section.
- 30 pages, then 5 redraws or edits (below).

Every page was reviewed on its own, then in consecutive pairs and as overview sheets
(`production/runs/contact-chapter-004/ch4-overview-{01-10,11-20,21-30}.jpg`, read right to left).

## Redrawn or edited
- **p01** (whole page, 2nd take): the 1st take drew two stray empty balloons in a caption-only panel, and Dai's
  "shifting" hand read as a punch. The spec now spells out the left hand (low by the hip, curled round a knob, on
  the image's right when he faces us), and the builder tells panels with captions but no dialogue: no balloons.
- **p02** (bottom panel only): the "Other hand" beat didn't read. A whole-page 2nd take was no better. The 3rd job
  edited a copy with the bottom panel blanked grey: Sota now holds up his RIGHT hand and Dai looks at it. The top
  three panels are the 1st take's pixels.
- **p18, p29** (edits): two stray empty balloons each (bottom panel / top panel), removed.
- p03, p04 and p30 were held back until p02 was fixed, because they continue from it.

## Lettering
- The letterer now **grows balloons drawn too small** for phone-readable type: it paints a bigger white balloon over
  the drawn one, inside its panel, with the tail toward the original tail tip (`grow: false` on a page turns it off).
  It also keeps the per-page size cap at 24 px or more. Result: every line is 21-29 px; the end caption is 22 px
  (`style: small`, on purpose).
- Hand placed: p28 (only one panel detected, so manual boxes), p30 (caption order), p22 (Mom's long line split
  over two balloons, every word kept), p25 (Kubo's explanation moved off his face), p02 (text kept clear of Sota's
  hair), p07, p24.
- All speakers checked against the art: right-to-left order, one speaker per panel, tails on the speaker.

## Checks
- **Akane and the Roadster are not in the chapter.** The only exterior car shot is the 180SX (p27, eye-level front
  three-quarter on the driver's flank, nose to the lower right, pop-ups down); p27's top panel is just two far
  headlights, and p08's GT-R is a printed magazine cover. No car pose repeats.
- **Dry nights:** p24-p28 are dry with the new plates; the station keeps one camera side (pumps left, office right).
- **Left hand:** p01-p04 and p30 show the shifting with the left hand except where noted.
- Classroom: Nobu sits behind Dai on every page; Nobu matches his sheet throughout and never looks like Dai.

## Kept nits
- p18, p19 (receipt close-ups): the long division shows unrelated numbers instead of 280,000 - 18,787.
- p19: the last panel shows the torn receipt, not the folding.
- p23: in the close-up of the open sneaker a foot is inside it.
- p30: the arm Dai raises reads as his right hand.
- p21-p23: night outside the window at dinner (fine for about 7 p.m., a little early for August).
- p17: the owner's two close-ups have nearly the same pose (reads as a comic repeat).
- Unscripted CRUNCH / RUSTLE / BUZZZ / FSSSH sound effects on p26-p28, and p09 BAM, p12 HA HA HA.
- p02 bottom: Dai's long balloon is 20 px, the smallest line in the chapter.
